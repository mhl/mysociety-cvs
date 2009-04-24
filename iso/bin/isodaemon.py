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
import time
import datetime
import traceback
import socket
import signal

os.chdir(sys.path[0])
sys.path.append("../../pylib")
import daemon # see PEP 3143 for documentation
#import daemon.pidlockfile
import mysociety.config

sys.path.append("../pylib")
import coldb

mysociety.config.set_file("../conf/general")
mysociety.config.load_default()
pidfile = mysociety.config.get('ISODAEMON_PIDFILE')
fastindex = mysociety.config.get('ISODAEMON_FASTINDEX')
logfile = mysociety.config.get('ISODAEMON_LOGFILE')
tmpwork = mysociety.config.get('TMPWORK')
concurr = int(mysociety.config.get('ISODAEMON_CONCURRENT_JOBS'))
sleep_db_poll = 2.0

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

#######################################################################################
# Helper functions

def server_and_pid():
    return socket.gethostname() + ":" + str(os.getpid())

# Used at the start of each logfile line
def stamp():
    return server_and_pid() + " " + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# Write something to logfile
def log(str):
    print stamp(), str
    sys.stdout.flush()

# Reads data from coopted C++ process, prints and returns it.
# Checks the line begins with check_regexp, and returns (line, match)
def my_readline(p, check_regexp = None):
    line = "DEBUG:"
    while re.match("DEBUG:", line):
        line = p.stdout.readline().strip()
        if line == '':
            raise Exception("unexpected EOF from C++ process")
        log("     " + line)

    if check_regexp:
        m = re.match(check_regexp, line)
        if not m:
            raise Exception("expected: " + check_regexp + " got:" + line)
        return (line, m)
    else:
        return line

#######################################################################################

# Runs a route calculation
def do_binplan(p, outfile, end_min, start_min, station_text_id):
    log("making route %s %d %d %s" % (outfile, end_min, start_min, station_text_id))
    outfile_routes = outfile + ".routes"
    outfile_new = outfile + ".new"
    outfile_routes_new = outfile_routes + ".new"

    # for debugging daemon code
    if options.excess_sleep: 
        log("excess sleeping for 10 seconds for debugging")
        time.sleep(10)

    # cause C++ program to do route finding
    p.stdin.write("binplan %s %s %d %d %s\n" % (outfile_new, outfile_routes_new, end_min, start_min, station_text_id))
    line = my_readline(p, 'target location')

    # wait for it to finish
    (line, match) = my_readline(p, 'route finding took: ([0-9.]+) secs')
    route_finding_time_taken = match.groups()[0]

    # also shows binary time taken
    (line, match) = my_readline(p, 'binary output took: ([0-9.]+) secs')
    output_time_taken = match.groups()[0]

    # move file into place
    if os.path.exists(outfile):
        os.remove(outfile)
    os.rename(outfile_new, outfile)
    if os.path.exists(outfile_routes):
        os.remove(outfile_routes)
    print outfile_routes_new
    os.rename(outfile_routes_new, outfile_routes)

    # return times
    log("made route " + outfile)
    return (float(route_finding_time_taken), float(output_time_taken))

# Core code of one isodaemon process. Checks database for map making work to do and does it.
def check_for_new_maps_to_make(p, db):
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
            break
        except postgres.OperationalError:
            # if someone else has the item locked, i.e. they are working on it, then we
            # try and find a different one to work on
            db.execute("rollback")
            offset = offset + 1
            log("somebody else had the item, trying offset " + str(offset))
            continue

    # if there's nothing more to do, give up
    if row == None:
        db.execute("rollback")
        # wait a bit, so don't thrash the database
        time.sleep(sleep_db_poll)
        return

    (id, state, target_station_text_id, target_latest, target_earliest, target_date) = row
    # XXX check target_date here is same as whatever fastindex timetable file we're using

    # see if another instance of daemon got it *just* before us
    if state != 'new':
        log("somebody else is already working on map " + str(id))
        db.execute("rollback")
        return

    # recording in the database that we are working on this
    db.execute("update map set state = 'working', working_server = %(server)s, working_start = now() where id = %(id)s", 
            dict(id=id, server=server_and_pid()))
    db.execute("commit")

    try:
        # actually perform the route finding
        db.execute("begin")
        outfile = os.path.join(tmpwork, "%d.iso" % int(id))
        #if child_number == 1: # for debugging
        #        raise Exception("testbroken")

        (route_finding_time_taken, output_time_taken) = \
            do_binplan(p, outfile, target_latest, target_earliest, target_station_text_id)

        # mark that we've done
        db.execute("update map set state = 'complete', working_took = %(took)s where id = %(id)s", dict(id=id, took=route_finding_time_taken))
        db.execute("commit")
    except (SystemExit, KeyboardInterrupt, AbortIsoException):
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

# Talking to multiple C++ processes
p2cread = [None] * (concurr + 1)
p2cwrite = [None] * (concurr + 1)
c2pread = [None] * (concurr + 1)
c2pwrite = [None] * (concurr + 1)
child_number = 0 # parent process, contains number 1,2,3,4... for daemon children
# Class for holding file handles to talk to C++ processes
class FastPlanPipe:
    def __init__(self, i):
        self.index = i
        self.stdout = os.fdopen(c2pread[self.index], 'rb', 0) # bufsize = 0
        self.stdin = os.fdopen(p2cwrite[self.index], 'wb', 0) # bufsize = 0
        #log("closing other end for index " + str(self.index))
        os.close(p2cread[self.index])
        os.close(c2pwrite[self.index])
    def _close_one(self, i):
        #log("closing all for index " + str(i))
        os.close(p2cread[i])
        os.close(p2cwrite[i])
        os.close(c2pread[i])
        os.close(c2pwrite[i])
    def close_other_pipes(self):
        for i in range(1, concurr + 1):
            if i != self.index:
                self._close_one(i)
    def close_pipes(self):
        #log("closing stdout/stdin for index " + str(self.index))
        self.stdout.close()
        self.stdin.close()

# Main loop getting map data
def do_main_loop():
    log("isodaemon.py started main loop")
    # load in timetable data once only
    log("loading timetable data into fastplan-coopt")

    # Create a pipe for each instance of the C++ child. We must make these
    # before forking off the C++ child, so it has the file handles to swap to
    # when it forks (after loading initial timetables).
    for i in range(concurr + 1):
        (p2cread[i], p2cwrite[i]) = os.pipe()
        (c2pread[i], c2pwrite[i]) = os.pipe()
    
    # Create pipe to talk to C++ program. This is similar code to
    # subprocess.Popen, only we do it ourselves so we can get the other end of
    # the pipe to fork later, and talk separately to each instance.
    pid = os.fork()
    if pid == 0:
        # C++ fastplan child... duplicate stream handlers over standard
        # stdout/stdin/sterr file descriptor numbers. We use the handles for
        # the 0th pipe here.
        os.dup2(p2cread[0], 0)
        os.dup2(c2pwrite[0], 1)
        os.dup2(c2pwrite[0], 2)
        # launch the planner
        args = [fastplan_bin, fastindex]
        os.execvp(fastplan_bin, args)
        raise Exception("execvp didn't work")

    # Parent, make object for talking to C++ process
    p = FastPlanPipe(0)

    # Wait for timetables to load
    line = my_readline(p, 'loading took')

    # Now fork as many times as concurrent jobs required
    global child_number
    for i in range(1, concurr + 1):
        # Tell the C++ planner to fork
        log("forking fastplan instance number " + str(i) + " fds %d %d %d" % (p2cread[i], c2pwrite[i], c2pwrite[i]))
        p.stdin.write("fork %d %d %d\n" % (p2cread[i], c2pwrite[i], c2pwrite[i]))
        line = my_readline(p, 'done fork')
        # Fork the parent Python process
        log("forking isodaemon instance number " + str(i))
        pid = os.fork()
        if pid == 0:
            # Python child number we are now on
            child_number = i
            # Make the object talk to appropriate C++ planner instance
            p.close_pipes()
            p = FastPlanPipe(i)
            p.close_other_pipes()
            # Wait a fraction of db poll time (so daemons poll at different
            # times to start with)
            time.sleep(float(child_number) * sleep_db_poll / float(concurr))
            break
        # parent, loop round to make next child

    try:
        # parent?
        if child_number == 0:
            # now children are started, we don't need their pipe handles
            p.close_other_pipes()
            # sleep until a SIGUSR1 happens, which will throw AbortIsoException
            # (see below)
            log("parent, waiting for signal")
            while 1:
                time.sleep(60)

        # check communication with C++ planner is working
        log("child started number " + str(child_number))
        p.stdin.write("info\n")
        my_readline(p, 'fastplan-coopt:')

        # connect to the database
        db = coldb.get_cursor()

        # loop, checking database for new maps to make
        while True:
            check_for_new_maps_to_make(p, db)
    finally:
        p.close_pipes()

# Convert a SIGUSR1 into a special exception type, for handling in do_main_loop below
class AbortIsoException(Exception):
    pass
def sigusr1_handler(signum, frame):
    assert signum == signal.SIGUSR1
    # traceback.print_stack(frame)
    raise AbortIsoException()
signal.signal(signal.SIGUSR1, sigusr1_handler)

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
        except (SystemExit, KeyboardInterrupt):
            # when stopped with SIGINT or with keyboard, stop every process
            traceback.print_exc()
            log("daemon_main: terminating process group on SystemExit/KeyboardInterrupt")
            os.killpg(os.getpgrp(), signal.SIGINT)
            break
        except AbortIsoException: 
            # if we're a child, then exit
            if child_number != 0:
                log("daemon_main: child terminating itself on AbortIsoException")
                break
            # wait for 10 seconds to stop repeated errors overwhelming things,
            # then restart all processes
            log("daemon_main: parent, sleeping 10 seconds and restarting main loop")
            time.sleep(10)
        except:
            # normal exception, some unexpected error
            traceback.print_exc()
            log("daemon_main: terminating process group")
            # tell all the other processes to exit / the main parent process to cause a restart
            signal.signal(signal.SIGUSR1, signal.SIG_DFL)
            os.killpg(os.getpgrp(), signal.SIGUSR1)
            break

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


