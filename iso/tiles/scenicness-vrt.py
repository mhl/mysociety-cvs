import sys
import csv
import urllib
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
        print >> vrtfile, '        <GeometryField encoding="PointFromColumns" x="Easting" y="Northing" z="Rating"/>'
        print >> vrtfile, '        <LayerSRS>%s</LayerSRS>' % GYM.srs.replace('"', '&quot;')
        print >> vrtfile, '    </OGRVRTLayer>'
        print >> vrtfile, '</OGRVRTDataSource>'

        src = urllib.urlopen('http://scenic.mysociety.org/votes2009-04-29.tsv')
        input = csv.reader(src, dialect='excel-tab')
        output = csv.writer(csvfile)
        
        print >> csvfile, 'Easting,Northing,Rating'
        
        for row in input:
            id, lat, lon, rating = row
            x, y = GYM(lon, lat)
            output.writerow((x, y, rating))
