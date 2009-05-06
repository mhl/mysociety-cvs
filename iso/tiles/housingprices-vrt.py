import re
import sys
import csv
import urllib
import datetime
import pyproj

if __name__ == '__main__':

    GYM = pyproj.Proj(proj='merc', a=6378137, b=6378137, lat_ts=0.0, lon_0=0.0, x_0=0.0, y_0=0, k=1.0, units='m', nadgrids=None, no_defs=True)
    
    try:
        csvfilename, vrtfilename = sys.argv[1:]
        csvfile, vrtfile = open(csvfilename, 'w'), open(vrtfilename, 'w')

    except ValueError:
        print >> sys.stderr, 'Usage: scenicness-vrt.py <csv output file> <vrt output file>'

    else:
        print >> vrtfile, '<OGRVRTDataSource>'
        print >> vrtfile, '    <OGRVRTLayer name="change me">'
        print >> vrtfile, '        <SrcDataSource>%s</SrcDataSource>' % csvfilename
        print >> vrtfile, '        <GeometryType>wkbPoint</GeometryType>'
        print >> vrtfile, '        <GeometryField encoding="PointFromColumns" x="Easting" y="Northing" z="Amount"/>'
        print >> vrtfile, '        <LayerSRS>%s</LayerSRS>' % GYM.srs.replace('"', '&quot;')
        print >> vrtfile, '    </OGRVRTLayer>'
        print >> vrtfile, '</OGRVRTDataSource>'
        vrtfile.close()

        src = open('ppi2317715_incl_addressesXTN.csv', 'r')
        input = csv.reader(src)
        output = csv.writer(csvfile)
        
        print >> csvfile, 'Easting,Northing,Rating'
        
        min_date = datetime.date(2008, 1, 1)
        date_pat = re.compile(r'^(\d+)/(\d+)/(\d\d\d\d)$')
        location_pat = re.compile(r'\blocation="(-?\d+\.\d+),(-?\d+\.\d+)"')
        postcodes, failed_postcodes = {}, {}
        
        for row in input:
            try:
                amount, date, postcode = row[:3]
                date_match = date_pat.match(date)
                
                if date_match:
                    date = datetime.date(*[int(date_match.group(i)) for i in (3, 2, 1)])
                    
                    if date < min_date:
                        continue
    
                    if postcode in failed_postcodes:
                        continue
                    
                    if postcode not in postcodes:
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
