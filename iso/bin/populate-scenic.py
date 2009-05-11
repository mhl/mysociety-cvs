#!/usr/bin/python
"""
Put house price data into database.

Copyright (c) 2009 UK Citizens Online Democracy. All rights reserved.
Email: francis@mysociety.org; WWW: http://www.mysociety.org/

$Id: populate-scenic.py,v 1.2 2009-05-11 22:23:44 francis Exp $
"""
import os
import sys
sys.path.append('/home/matthew/lib/python')
import math
import csv
import datetime
import re
import urllib

sys.path.append("../../pylib")
import mysociety.config
mysociety.config.set_file("../conf/general")
import mysociety.mapit
from mysociety.rabx import RABXException

sys.path.append("../pylib")
import coldb
db = coldb.get_cursor()

import geoconvert

src = urllib.urlopen('http://scenic.mysociety.org/votes.tsv')
input = csv.reader(src, dialect='excel-tab')

#print >> csvfile, 'Easting,Northing,Rating'

db.execute('''begin''')
db.execute('''delete from scenic''')

for row in input:
    id, lat, lon, rating = row

    x, y = geoconvert.wgs84_to_national_grid(lat, lon)
    merc_x, merc_y = geoconvert.bng2gym(x, y)

    db.execute('''insert into scenic (position_osgb, position_merc, rating)
                  values (
                        SetSRID(MakePoint(%s, %s), 27700), 
                        SetSRID(MakePoint(%s, %s), 900913), 
                        %s
                    )''', (x, y, merc_x, merc_y, rating))

db.execute('''commit''')


