"""
Custom TileCache module for rendering of isochrone images based on travel time data.

Copyright (c) 2009 UK Citizens Online Democracy. All rights reserved.
Email: mike@stamen.com; WWW: http://www.mysociety.org/

$Id: Isochrones.py,v 1.8 2009-03-18 17:14:57 migurski Exp $
"""
import os
import sys
import time
import os.path
import StringIO

import numpy
import pyproj
import TileCache
import PIL.Image
import Cone

class TileLayer(TileCache.Layer.MetaLayer):

    config_properties = [
      {'name': 'timestep', 'description': 'Time step, in seconds, per level of gray.'},
    ] + TileCache.Layer.MetaLayer.config_properties 
    
    def __init__(self, name, timestep=60, **kwargs):
        """ call super.__init__, but also store the results_id from PATH_INFO
        """
        TileCache.Layer.MetaLayer.__init__(self, name, **kwargs)

        # the result set ID is the first part of the path
        self.results_id = os.environ["PATH_INFO"].lstrip('/').split('/')[0]
        self.timestep = float(timestep)
    
    def renderTile(self, tile, force=None):
        """
        """
        # grab points data
        points = get_data(self.results_id, tile)
        
        # open a log file
        log = False # open(os.path.dirname(__file__)+'/log.txt', 'a')
        
        #if log:
        #    width, height = tile.size()
        #    xmin, ymin, xmax, ymax = tile.bounds()
        #    print >> log, 'Tile(%d, %d, %d, %d, %d, %d)' % (width, height, xmin, ymin, xmax, ymax)

        # render a PIL image
        image = draw_tile(points, tile, self.timestep, log)

        tile.data = img2str(image, self.extension)

        return tile.data

class TileStub:
    """ Imitation  of TileCache.Tile for test purposes
    """
    def __init__(self, width, height, xmin, ymin, xmax, ymax):
        self.width = width
        self.height = height
        self.xmin = xmin
        self.ymin = ymin
        self.xmax = xmax
        self.ymax = ymax

    def size(self):
        return self.width, self.height

    def bounds(self):
        return self.xmin, self.ymin, self.xmax, self.ymax

def draw_tile(points, tile, timestep, log):
    """ Render points to a single tile image
    """
    prep_start = time.time()
    
    # get the tile in spherical mercator
    xmin, ymin, xmax, ymax = tile.bounds()
    width, height = tile.size()
    
    # make conversion stuffs for spherical mercator points back to tile space
    xoffset, yoffset = -xmin, -ymin
    xscale, yscale = width / float(xmax - xmin), height / float(ymax - ymin)
    transform = lambda x, y: (xscale * (x + xoffset), yscale * (y + yoffset))
    
    # create an array to hold travel times
    # note that here 0x00 = zero time; inversion for output image happens later
    array = numpy.ones(tile.size(), numpy.int32) * timestep * 0xFF
    
    # 1800 meters is a half hour of walking at 1m/s
    pixels_per_1800_meters = 1800 * Cone.pixels_per_kilometer(tile) / 1000
    
    prep_time = time.time() - prep_start
    cone_start = time.time()
    
    # create a station cone and mask where value is walking seconds
    station_cone = Cone.make_cone(pixels_per_1800_meters)
    station_mask = station_cone <= 1800
    
    cone_time = time.time() - cone_start
    points_start = time.time()
    
    # add each found data point in turn, offseting station cones by base station time
    for (x, y, t) in points:
        x, y = transform(*bng2gym(x, y))
        draw_station(array, station_cone + t, station_mask, int(x), int(y))

    points_time = time.time() - points_start

    if log:
        print >> log, 'Tile %d/%d/%d' % (tile.z, tile.x, tile.y),
        print >> log, 'prep: %.2fs, %dx%d cone: %.2fs,' % (prep_time, station_cone.shape[0], station_cone.shape[1], cone_time),
        print >> log, '%d points, %d points/sec,' % (len(points), len(points) / points_time),
        print >> log, '%.1fm point-pixels/sec,' % ((len(points) * station_cone.shape[0] * station_cone.shape[1]) / (points_time * 1000000)),
        print >> log, 'total: %.2fs' % (prep_time + cone_time + points_time)
        
    # invert array and scale for timestep, so that 0xFF = zero time
    array = 256 - (array / timestep)
    
    # convert array to an image
    # we rotate the image to deal with row/col vs. x/y transposition in numpy and some other geometry oddness
    image = arr2img(array).transpose(PIL.Image.ROTATE_90)

    return image

def draw_station(array, station, station_mask, x, y):
    """ Given a base map array and a timescaled station array, drop the station
        onto the base map using a minimum filter to correctly overwrite longer times.
    """
    axmin = x - station.shape[0] / 2
    axmax = axmin + station.shape[0]

    aymin = y - station.shape[1] / 2
    aymax = aymin + station.shape[1]
    
    sxmin, symin, sxmax, symax = 0, 0, station.shape[0], station.shape[1]
    
    assert axmax - axmin == sxmax - sxmin
    assert aymax - aymin == symax - symin
    
    # find bounds where necessary
    
    if axmin < 0:
        axmin, sxmin = 0, -axmin
    
    if aymin < 0:
        aymin, symin = 0, -aymin

    if axmax > array.shape[0]:
        axmax, sxmax = array.shape[0], sxmax - (axmax - array.shape[0])

    if aymax > array.shape[1]:
        aymax, symax = array.shape[1], symax - (aymax - array.shape[1])
    
    if axmax <= 0 or aymax <= 0:
        return
    
    if axmin > array.shape[0] or aymin > array.shape[1]:
        return

    assert axmax - axmin == sxmax - sxmin
    assert aymax - aymin == symax - symin

    target = array[axmin:axmax, aymin:aymax]
    value = station[sxmin:sxmax, symin:symax]
    mask = station_mask[sxmin:sxmax, symin:symax]
    
    # set just the masked parts
    target[mask] = numpy.minimum(target[mask], value[mask])

BNG = pyproj.Proj(proj='tmerc', lat_0=49, lon_0=-2, k=0.999601, x_0=400000, y_0=-100000, ellps='airy', towgs84='446.448,-125.157,542.060,0.1502,0.2470,0.8421,-20.4894', units='m', no_defs=True)
GYM = pyproj.Proj(proj='merc', a=6378137, b=6378137, lat_ts=0.0, lon_0=0.0, x_0=0.0, y_0=0, k=1.0, units='m', nadgrids=None, no_defs=True)

def img2str(image, format):
    """ Convert image to a data buffer in a given format, e.g. PNG or JPEG
    """
    buffer = StringIO.StringIO()
    image.save(buffer, format)
    buffer.seek(0)
    return buffer.read()

def arr2img(ar):
    """ Convert numpy.array to PIL.Image.
    """
    return PIL.Image.fromstring('L', (ar.shape[1], ar.shape[0]), ar.clip(0x00, 0xFF).astype(numpy.ubyte).tostring())

def bng2gym(x, y):
    """ Project from British National Grid to spherical mercator
    """
    return GYM(*BNG(x, y, inverse=True))

def gym2bng(x, y):
    """ Project from spherical mercator to British National Grid
    """
    return BNG(*GYM(x, y, inverse=True))

def get_data(results_id, tile):
    """ Given a result ID and a tile, return data points for all the bits that intersect
    """
    # tile bounds in spherical mercator
    xmin, ymin, xmax, ymax = tile.bounds()

    # convert bounds to british national grid
    xmin, ymin = gym2bng(xmin, ymin)
    xmax, ymax = gym2bng(xmax, ymax)
    
    # make it true
    xmin, xmax = min(xmin, xmax), max(xmin, xmax)
    ymin, ymax = min(ymin, ymax), max(ymin, ymax)
    
    # adjust by 1800 meters
    xmin, ymin, xmax, ymax = xmin - 1800, ymin - 1800, xmax + 1800, ymax + 1800

    # open the file
    datapoints = open(os.path.dirname(__file__) + '/nptdr-OX26DR-10000.txt', 'r')

    # split the easting, northing, and seconds on each line
    datapoints = (line.split() for line in datapoints)

    # convert them all to numbers
    datapoints = ((float(x), float(y), int(t)) for (x, y, t) in datapoints)
    
    # get just the ones in the bounding box
    datapoints = [(x, y, t) for (x, y, t) in datapoints
                  if xmin <= x and x <= xmax and ymin <= y and y <= ymax]
    
    return datapoints

