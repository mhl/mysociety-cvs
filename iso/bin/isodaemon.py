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

sys.path.append("../../pylib")

import daemon # see PEP 3143 for documentation
import daemon.pidlockfile
import mysociety.config

mysociety.config.set_file("../conf/general")
pidfile = mysociety.config.get('ISODAEMON_PIDFILE')
fastindex = mysociety.config.get('ISODAEMON_FASTINDEX')
logfile = mysociety.config.get('ISODAEMON_LOGFILE')

parser = optparse.OptionParser()

parser.set_usage('''
isodaemon.py is a Daemon for generating travel times by public transport
to places in the UK. It requires ../conf/general file for configuration.

--d
''')
parser.add_option('--nodetach', action='store_true', dest="nodetach", help='Stops it detaching from the terminal')
parser.add_option('--nolog', action='store_true', dest="nolog", help='Log to stdout/stderr instead of the logfile')

(options, args) = parser.parse_args()
def do_plan(p, end_min, start_min, e, n):
    p.stdin.write("plan %d %d %d %d\n" % (end_min, start_min, e, n))
    line = p.stdout.readline()
    assert re.match('target location', line)
    while True:
        line = p.stdout.readline()
        if line == '': # EOF
            break
        match = re.match('route finding took: ([0-9.]+) secs', line)
        if match:
            break
        #print line
    time_taken = match.groups()[0]
    return time_taken

def do_main_program():
    while True:
        print "do_main_program"
        pass
    p = subprocess.Popen(['./fastplan-coopt', fastindex], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    line = p.stdout.readline()
    assert re.match('loading took', line)

    while True:
        time_taken = do_plan(p, 540, 0, 450445, 207017)
        print "done route in", time_taken

logout = open(logfile, 'w')

# XXX no locking that I like yet :)
#ourlockfile = daemon.pidlockfile.PIDLockFile
#ourlockfile.path = pidfile
#    pidfile=lockfile.FileLock(pidfile), 

context = daemon.DaemonContext(
    stdout=logout, stderr=logout,
    detach_process=(not options.nodetach)
)
with context:
    i = 1
    while True:
        i = i + 1
        sys.stdout.write("we are there " + repr(i) + "\n")
        sys.stderr.write("error " + repr(i) + "\n")
        sys.stdout.flush()



