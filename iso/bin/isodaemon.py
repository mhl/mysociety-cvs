#!/usr/bin/python2.4
#
# isodaemon.py:
# Daemon to generate coordinates for isochrone maps in the background
# Coopts the fastplan-coopt C++ program to do the work quickly.
#
# Copyright (c) 2009 UK Citizens Online Democracy. All rights reserved.
# Email: francis@mysociety.org; WWW: http://www.mysociety.org/
#

# Pipe read timeouts
# Trapping all exceptions / errors and logging to syslog and resuming 

# from __future__ import with_statement # for use with daemon below in Python 2.5

import sys
import subprocess
import re
import os
import optparse
import psycopg2 as postgres
import time
import datetime
import traceback
import socket

os.chdir(sys.path[0])
sys.path.append("../../pylib")

import daemon # see PEP 3143 for documentation
#import daemon.pidlockfile
import mysociety.config

mysociety.config.set_file("../conf/general")
pidfile = mysociety.config.get('ISODAEMON_PIDFILE')
fastindex = mysociety.config.get('ISODAEMON_FASTINDEX')
logfile = mysociety.config.get('ISODAEMON_LOGFILE')
tmpwork = mysociety.config.get('TMPWORK')

parser = optparse.OptionParser()

parser.set_usage('''
isodaemon.py is a Daemon for generating travel times by public transport
to places in the UK. It requires ../conf/general file for configuration.

Run with --help for options.
''')
parser.add_option('--nodetach', action='store_true', dest="nodetach", help='Stops it detaching from the terminal')
parser.add_option('--nolog', action='store_true', dest="nolog", help='Log to stdout instead of the logfile')
parser.add_option('--cooptdebug', action='store_true', dest="cooptdebug", help='Use debug version of fastplan-coopt library')
parser.add_option('--excesssleep', action='store_true', dest="excess_sleep", help='Pointlessly wait extra 15 seconds when making map, to help testing')

(options, args) = parser.parse_args()

fastplan_bin = "./fastplan-coopt"
if options.cooptdebug:
    fastplan_bin = "./fastplan-coopt-debug"

# Used at the start of each logfile line
def stamp():
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# Write something to logfile
def log(str):
    print stamp(), str
    sys.stdout.flush()

# Reads data from coopted C++ process, prints and returns it
def my_readline(p):
    line = p.stdout.readline().strip()
    if line != '':
        log("     " + line)
    return line

# Runs a route calculation
def do_binplan(p, outfile, end_min, start_min, station_text_id):
    log("making route %s %d %d %s" % (outfile, end_min, start_min, station_text_id))
    if options.excess_sleep: # for debugging daemon code
        time.sleep(15)
    outfile_new = outfile + ".new"

    # cause C++ program to do route finding
    p.stdin.write("binplan %s %d %d %s\n" % (outfile_new, end_min, start_min, station_text_id))
    line = my_readline(p)
    assert re.match('target location', line)

    # wait for it to finish
    route_finding_time_taken = None
    while True:
        line = my_readline(p)
        if line == '': # EOF
            break

        # have finished if we get a time taken
        match = re.match('route finding took: ([0-9.]+) secs', line)
        route_finding_time_taken = match.groups()[0]
        if match:
            break

    # also shows binary time taken
    line = my_readline(p)
    match = re.match('binary output took: ([0-9.]+) secs', line)
    output_time_taken = match.groups()[0]

    # move file into place
    if os.path.exists(outfile):
        os.remove(outfile)
    os.rename(outfile_new, outfile)

    # return times
    log("made route " + outfile)
    return (float(route_finding_time_taken), float(output_time_taken))

# Main loop getting map data
def do_main_loop():
    # initialisation
    log("isodaemon.py started main loop")
    db = postgres.connect(
            host=mysociety.config.get('COL_DB_HOST'),
            port=mysociety.config.get('COL_DB_PORT'),
            database=mysociety.config.get('COL_DB_NAME'),
            user=mysociety.config.get('COL_DB_USER'),
            password=mysociety.config.get('COL_DB_PASS')
    ).cursor()

    # load in timetable data once only
    log("loading timetable data into fastplan-coopt")
    p = subprocess.Popen([fastplan_bin, fastindex], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    line = my_readline(p)
    assert re.match('loading took', line)

    # loop, checking database for new maps to make
    while True:
        # find something to do - we start with the map that was queued longest ago.
        offset = 0
        while True:
            try:
                db.execute("begin")
                # we get the row "for update" to lock it, and "nowait" so we
                # get an exception if someone else already has it, rather than
                # pointlessly waiting for them
                db.execute("""select id, state, (select text_id from station where id = target_station_id), 
                                target_latest, target_earliest, target_date from map where 
                                state = 'new' order by created limit 1 offset %s for update nowait""" % offset)
                row = db.fetchone()
            except postgres.OperationalError:
                # if someone else has the item locked, i.e. they are working on it, then we
                # try and find a different one to work on
                db.execute("rollback")
                offset = offset + 1
                log("somebody else had the item, trying offset " + str(offset))
                continue
            break

        # if there's nothing more to do, give up
        if row == None:
            db.execute("rollback")
            # wait a bit, so don't thrash the database
            time.sleep(5)
            continue

        (id, state, target_station_text_id, target_latest, target_earliest, target_date) = row
        # XXX check target_date here is same as whatever fastindex timetable file we're using

        # see if another instance of daemon got it
        if state != 'new':
            log("somebody else is already working on map " + str(id))
            db.execute("rollback")
            continue
    
        # recording in the database that we are working on this
        server = socket.gethostname() + ":" + str(os.getpid())
        db.execute("update map set state = 'working', working_server = %(server)s, working_start = now() where id = %(id)s", 
                dict(id=id, server=server))
        db.execute("commit")

        try:
            # actually perform the route finding
            db.execute("begin")
            outfile = os.path.join(tmpwork, "%d.iso" % int(id))
            (route_finding_time_taken, output_time_taken) = \
                do_binplan(p, outfile, target_latest, target_earliest, target_station_text_id)

            # mark that we've done
            db.execute("update map set state = 'complete', working_took = %(took)s where id = %(id)s", dict(id=id, took=route_finding_time_taken))
            db.execute("commit")
        except SystemExit:
            # daemon was explicitly stopped, don't mark map as error
            db.execute("rollback")
            db.execute("begin")
            db.execute("update map set state = 'new' where id = %(id)s", dict(id=id))
            db.execute("commit")
            raise
        except:
            # record there was an error, so we can find out easily
            # if the recording error doesn't work, then presumably it was a database error
            db.execute("rollback")
            db.execute("begin")
            db.execute("update map set state = 'error' where id = %(id)s", dict(id=id))
            db.execute("commit")
            raise

# Call main loop, catching any exceptions to prevent exit and restarting loop.
# Keep this function as simple as possible, so it is unlikely to raise an
# exception.
def daemon_main():
    # write pidfile
    pidout = open(pidfile, 'w')
    pidout.write(str(os.getpid()))
    pidout.close()

    # loop, catching errors 
    while True:
        try:
            do_main_loop()
        except SystemExit:
            traceback.print_exc()
            log("daemon_main: terminating")
            break
        except: 
            # display error, then wait for 10 seconds to stop repeated errors
            # overwhelming things.
            traceback.print_exc()
            log("daemon_main: restarting main loop")
            time.sleep(10)

    # remove pidfile
    if os.path.exists(pidfile):
        os.remove(pidfile)

# Open log file
if options.nolog:
    logout = sys.stdout
else:
    logout = open(logfile, 'a')

# XXX no locking that I like yet :) we do need something nice using lockf of
# fcntl to prevent starting the daemon twice.
# XXX see also pidfile writing part in daemon_main
#ourlockfile = daemon.pidlockfile.PIDLockFile
#ourlockfile.path = pidfile
#    pidfile=lockfile.FileLock(pidfile), 

context = daemon.DaemonContext(
    stdout=logout, stderr=logout,
    detach_process=(not options.nodetach),
    working_directory=os.path.abspath(os.path.dirname(sys.argv[0]))
)

# Could use "with" here, but we don't have it in Python 2.4 - when all servers
# are upgraded to etch/lenny can change this.
context.__enter__()
try:
    daemon_main()
finally:
    context.__exit__(None, None, None)


