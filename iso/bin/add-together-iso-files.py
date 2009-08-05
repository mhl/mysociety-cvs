#!/usr/bin/python2.5
#
# add-together-iso-files.py:
# Take several .iso binary files which contain travel times to every station in the UK,
# and combine them into one file with the average time.
#
# Copyright (c) 2009 UK Citizens Online Democracy. All rights reserved.
# Email: francis@mysociety.org; WWW: http://www.mysociety.org/
#
import sys
import re
import os
import optparse
import time
import datetime
import traceback
import psycopg2
import struct

os.chdir(sys.path[0])
sys.path.append("../../pylib")
import mysociety.config

sys.path.append("../pylib")
import coldb

mysociety.config.set_file("../conf/general")
mysociety.config.load_default()
tmpwork = mysociety.config.get('TMPWORK')
db = coldb.get_cursor()

parser = optparse.OptionParser()

parser.set_usage('''
First parameter is output .iso file name, other parameters are file names of .iso files to average together to make the output one. All are looked for in the tmpwork directory.
e.g. ./add-together-iso-files.py moo 1439 1440
''')
(options, args) = parser.parse_args()

dest_file = tmpwork + "/" + args[0] + ".iso"
print "writing to " + dest_file
read_files = [tmpwork + "/" + id + ".iso" for id in args[1:] ]
read_handles = [open(f, 'rb') for f in read_files]
print "reading from " + str(read_files)

# get number of stations
db.execute("""SELECT max(id) FROM station""")
row = db.fetchone()
max_station_id = row[0]

# average together the times for each station
dest_handle = open(dest_file, 'w')
for id in range(0, max_station_id + 1):
    tot = 0
    c = 0
    valid = True
    for handle in read_handles:
        # the .iso file is just a list of shorts, containing times in minutes, 
        # in order of location id, so we can just seek by location id
        handle.seek(id * 2)
        tim_bytes = handle.read(2)
        if len(tim_bytes) != 2:
            raise Exception("failed to unpack x:%s y:%s station id:%s" % (repr(x), repr(y), repr(id)))
        tim = struct.unpack("h", tim_bytes)[0]
        tot = tot + tim
        c = c + 1
        if tim < 0: # if a place wasn't accessible, i.e. distance was MINUTES_NULL
            valid = False
    if valid:
        tot = tot / c
    else:
        tot = -1

    out_bytes = struct.pack("=h", tot)
    assert len(out_bytes) == 2
    dest_handle.seek(id * 2)
    dest_handle.write(out_bytes)


