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

from __future__ import with_statement # for use with daemon below

import sys
import subprocess
import re
import os
import optparse
import psycopg2 as postgres
import time
import datetime

sys.path.append("../../pylib")

import daemon # see PEP 3143 for documentation
import daemon.pidlockfile
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

def stamp():
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def my_readline(p):
    line = p.stdout.readline().strip()
    if line != '':
        print stamp() + "     " + line
    return line

(options, args) = parser.parse_args()
def do_binplan(p, outfile, end_min, start_min, station_text_id):
    print stamp(), "making route", outfile, end_min, start_min, station_text_id
    time.sleep(10)
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

def do_main_program():
    print stamp(), "isodaemon.py started"
    db = postgres.connect(
            host=mysociety.config.get('COL_DB_HOST'),
            port=mysociety.config.get('COL_DB_PORT'),
            database=mysociety.config.get('COL_DB_NAME'),
            user=mysociety.config.get('COL_DB_USER'),
            password=mysociety.config.get('COL_DB_PASS')
    ).cursor()

    print stamp(), "loading timetable data into fastplan-coopt"
    p = subprocess.Popen(['./fastplan-coopt', fastindex], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    line = my_readline(p)
    assert re.match('loading took', line)

    while True:
        db.execute("begin")

        # find something to do - we start with the map that was queued longest ago.
        offset = 0
        while True:
            try:
                db.execute("""select id, state, target_station_id, target_latest, target_earliest, target_date from map where 
                              state = 'new' order by created limit 1 offset %s for update nowait""", str(offset))
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
            print stamp(), "nothing to do, sleeping 5 seconds"
            time.sleep(5)
            continue

        (id, state, target_station_id, target_latest, target_earliest, target_date) = row

        # see if another instance of daemon got it
        if state != 'new':
            print stamp(), "somebody else is already working on map ", id
            db.execute("rollback")
            continue

        # XXX check target_date here is same as whatever fastindex timetable file we're using

        (route_finding_time_taken, output_time_taken) = do_binplan(p, tmpwork + "/%d.iso" % int(id), target_latest, target_earliest, target_station_id)

        db.execute("update map set state = 'complete' where id = %s", str(id))
        db.execute("commit")

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

with context:
    do_main_program()
#    i = 1
#    while True:
#        i = i + 1
#        sys.stdout.write("we are there " + repr(i) + "\n")
#        sys.stderr.write("error " + repr(i) + "\n")
#        sys.stdout.flush()



