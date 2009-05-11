#!/usr/bin/python
#
# Code to convert Land Registry CSV data into data for tile server

# Set to True to use MaPit for postcode lookup, False for Stamen
USE_MAPIT = False

import re
import sys
sys.path.append('/home/matthew/lib/python') # XXX For pyproj, won't affect anything
if USE_MAPIT:
    sys.path.append('../../pylib')
import csv
import urllib
import datetime
import pyproj
if USE_MAPIT:
    import mysociety.mapit
    from mysociety.rabx import RABXException
    mysociety.config.set_file('../conf/general')

if __name__ == '__main__':

    GYM = pyproj.Proj(proj='merc', a=6378137, b=6378137, lat_ts=0.0, lon_0=0.0, x_0=0.0, y_0=0, k=1.0, units='m', nadgrids=None, no_defs=True)
    
    try:
        csvfilename, vrtfilename = sys.argv[1:]
        csvfile, vrtfile = open(csvfilename, 'w'), open(vrtfilename, 'w')

    except ValueError:
        print >> sys.stderr, 'Usage: scenicness-vrt.py <csv output file> <vrt output file>'

    else:
        print >> vrtfile, '<OGRVRTDataSource>'
        print >> vrtfile, '    <OGRVRTLayer name="housingprices">'
        print >> vrtfile, '        <SrcDataSource>%s</SrcDataSource>' % csvfilename
        print >> vrtfile, '        <GeometryType>wkbPoint</GeometryType>'
        print >> vrtfile, '        <GeometryField encoding="PointFromColumns" x="Easting" y="Northing" z="Amount"/>'
        print >> vrtfile, '        <LayerSRS>%s</LayerSRS>' % GYM.srs.replace('"', '&quot;')
        print >> vrtfile, '    </OGRVRTLayer>'
        print >> vrtfile, '</OGRVRTDataSource>'
        vrtfile.close()

        src = open('/library/landregistry/uk-20080101-20090331/ew_010108-310309_inc_addresses.txt', 'r')
        input = csv.reader(src)
        output = csv.writer(csvfile)
        
        print >> csvfile, 'Easting,Northing,Amount'
        
        min_date = datetime.date(2008, 1, 1)

        date_pat = re.compile(r'(\d\d\d\d)-(\d+)-(\d+) ')
        location_pat = re.compile(r'\blocation="(-?\d+\.\d+),(-?\d+\.\d+)"')
        postcodes, failed_postcodes = {}, {}
        
        for row in input:
            try:
                amount, date, postcode = row[:3]
                date_match = date_pat.match(date)
                
                if date_match:
                    date = datetime.date(*[int(i) for i in date_match.groups()])
                    
                    if date < min_date:
                        continue
    
                    if postcode in failed_postcodes:
                        continue
                    
                    if postcode not in postcodes:
                        if USE_MAPIT:
                            try:
                                result = mysociety.mapit.get_location(postcode)
                            except RABXException, e:
                                if e.value == mysociety.mapit.POSTCODE_NOT_FOUND:
                                    continue
                                if e.value == mysociety.mapit.BAD_POSTCODE and postcode=='UNKNOWN':
                                    continue
                                raise
                            postcodes[postcode] = result['wgs84_lat'], result['wgs84_lon']
                        else:
                            places_xml = urllib.urlopen('http://locog.stamen.com/~migurski/data/www/places.php?format=xml&q=' + urllib.quote_plus(postcode)).read()
                            places_match = location_pat.search(places_xml)
    
                            if places_match:
                                latitude, longitude = [float(places_match.group(i)) for i in (1, 2)]
                                postcodes[postcode] = latitude, longitude
    
                            else:
                                failed_postcodes[postcode] = True
                            
                    if postcode not in postcodes:
                        # still?
                        continue
                    
                    lat, lon = postcodes[postcode]
                    x, y = GYM(lon, lat)
                    output.writerow((x, y, amount))
    
                    print >> sys.stderr, date, postcode, amount, lat, lon
            except KeyboardInterrupt:
                raise

            except:
                pass
