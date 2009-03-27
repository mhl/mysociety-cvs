#!/usr/bin/python
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

# Reads data from coopted C++ process, prints and returns it
def my_readline(p):
    line = p.stdout.readline().strip()
    if line != '':
        print stamp() + "     " + line
    return line

# Runs a route calculation
def do_binplan(p, outfile, end_min, start_min, station_text_id):
    print stamp(), "making route", outfile, end_min, start_min, station_text_id
    if options.excess_sleep:
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
    print stamp(), "made route", outfile
    return (float(route_finding_time_taken), float(output_time_taken))

# Main loop getting map data
def do_main_loop():
    # initialisation
    print stamp(), "isodaemon.py started main loop"
    db = postgres.connect(
            host=mysociety.config.get('COL_DB_HOST'),
            port=mysociety.config.get('COL_DB_PORT'),
            database=mysociety.config.get('COL_DB_NAME'),
            user=mysociety.config.get('COL_DB_USER'),
            password=mysociety.config.get('COL_DB_PASS')
    ).cursor()

    # load in timetable data once only
    print stamp(), "loading timetable data into fastplan-coopt"
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
                print stamp(), "somebody else had the item, trying offset " + str(offset)
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
            print stamp(), "somebody else is already working on map ", id
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
    while True:
        try:
            do_main_loop()
        except: 
            # display error, then wait for 10 seconds to stop repeated errors
            # overwhelming things.
            traceback.print_exc()
            time.sleep(10)

if options.nolog:
    logout = sys.stdout
else:
    logout = open(logfile, 'w')

# XXX no locking that I like yet :)
#ourlockfile = daemon.pidlockfile.PIDLockFile
#ourlockfile.path = pidfile
#    pidfile=lockfile.FileLock(pidfile), 

context = daemon.DaemonContext(
    stdout=logout, stderr=logout,
    detach_process=(not options.nodetach),
    working_directory=os.path.abspath(os.path.dirname(sys.argv[0]))
)

# Could use with here, but don't have it in Python 2.4
#context.__enter__()
#try:
daemon_main()
#finally:
#    context.__exit__()

