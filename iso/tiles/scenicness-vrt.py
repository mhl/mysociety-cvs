import sys
import urllib
import csv

if __name__ == '__main__':

    try:
        csvfilename, vrtfilename = sys.argv[1:]
        csvfile, vrtfile = open(csvfilename, 'w'), open(vrtfilename, 'w')

    except ValueError:
        print >> sys.stderr, 'Usage: scenicness-vrt.py <csv output file> <vrt output file>'

    else:
        print >> vrtfile, '<?xml version="1.0"?>'
        print >> vrtfile, '<OGRVRTDataSource>'
        print >> vrtfile, '    <OGRVRTLayer name="scenic">'
        print >> vrtfile, '        <SrcDataSource>%s</SrcDataSource>' % csvfilename
        print >> vrtfile, '        <GeometryType>wkbPoint</GeometryType>'
        print >> vrtfile, '        <GeometryField encoding="PointFromColumns" x="Longitude" y="Latitude" z="Rating"/>'
        print >> vrtfile, '    </OGRVRTLayer>'
        print >> vrtfile, '</OGRVRTDataSource>'

        src = urllib.urlopen('http://scenic.mysociety.org/votes2009-04-27.tsv')
        input = csv.DictReader(src, dialect='excel-tab')
        output = csv.writer(csvfile)
        
        print >> csvfile, 'Latitude,Longitude,Rating'
        
        for row in input:
            output.writerow((row['Lat'], row['Lon'], row['Rating']))
