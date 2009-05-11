#!/usr/bin/python
"""
Put house price data into database.

Copyright (c) 2009 UK Citizens Online Democracy. All rights reserved.
Email: francis@mysociety.org; WWW: http://www.mysociety.org/

$Id: populate-houseprices.py,v 1.1 2009-05-11 15:57:52 francis Exp $
"""
import os
import sys
import math
import csv
import datetime
import re

sys.path.append("../../pylib")
import mysociety.config
mysociety.config.set_file("../conf/general")
import mysociety.mapit
from mysociety.rabx import RABXException

sys.path.append("../pylib")
import coldb
db = coldb.get_cursor()

import geoconvert

#print >> vrtfile, '<OGRVRTDataSource>'
#print >> vrtfile, '    <OGRVRTLayer name="housingprices">'
#print >> vrtfile, '        <SrcDataSource>%s</SrcDataSource>' % csvfilename
#print >> vrtfile, '        <GeometryType>wkbPoint</GeometryType>'
#print >> vrtfile, '        <GeometryField encoding="PointFromColumns" x="Easting" y="Northing" z="Amount"/>'
#print >> vrtfile, '        <LayerSRS>%s</LayerSRS>' % GYM.srs.replace('"', '&quot;')
#print >> vrtfile, '    </OGRVRTLayer>'
#print >> vrtfile, '</OGRVRTDataSource>'

src = open('/library/landregistry/uk-20080101-20090331/ew_010108-310309_inc_addresses.txt', 'r')
input = csv.reader(src)

#print >> csvfile, 'Easting,Northing,Rating'

min_date = datetime.date(2008, 1, 1)

date_pat = re.compile(r'(\d\d\d\d)-(\d+)-(\d+) ')
location_pat = re.compile(r'\blocation="(-?\d+\.\d+),(-?\d+\.\d+)"')
postcodes = {}

db.execute('''begin''')
db.execute('''delete from house_price''')

for row in input:
    amount, date, postcode, type_of_house, new_build, tenure = row[:6]
    if new_build == 'Y':
        new_build = True
    else:
        assert new_build == 'N'
        new_build = False
    address = (" ".join(row[6:9]) + ", " + ", ".join(row[9:])).replace(", , ", ", ").replace("  ", " ")
    date_match = date_pat.match(date)
    
    if date_match:
        date = datetime.date(*[int(i) for i in date_match.groups()])
        
        if date < min_date:
            continue

        if postcode not in postcodes:
            try:
                result = mysociety.mapit.get_location(postcode)
            except RABXException, e:
                if e.value == mysociety.mapit.POSTCODE_NOT_FOUND:
                    continue
                if e.value == mysociety.mapit.BAD_POSTCODE and postcode=='UNKNOWN':
                    continue
                raise
            postcodes[postcode] = result['wgs84_lat'], result['wgs84_lon']
                
        if postcode not in postcodes:
            # still?
            continue
        
        lat, lon = postcodes[postcode]
        x, y = geoconvert.wgs84_to_national_grid(lat, lon)
        #output.writerow((x, y, amount))
        #db.execute("""insert into """, % (minimum_zoom, id))

        db.execute('''insert into house_price (position_osgb, transaction_date, amount, type_of_house, new_build, tenure, address)
                      values (
                            SetSRID(MakePoint(%s, %s), 27700), %s, %s, %s, %s, %s, %s
                        )''', (x, y, date, amount, type_of_house, new_build, tenure, address))
        db.execute('''commit''')


        print >> sys.stderr, date, postcode, amount, lat, lon, x, y, address

db.execute('''commit''')


