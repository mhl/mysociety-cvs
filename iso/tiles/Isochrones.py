"""
Custom TileCache module for rendering of isochrone images based on travel time data.

Copyright (c) 2009 UK Citizens Online Democracy. All rights reserved.
Email: mike@stamen.com; WWW: http://www.mysociety.org/

$Id: Isochrones.py,v 1.19 2009-03-24 22:16:54 migurski Exp $
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
import Data

class TileLayer(TileCache.Layer.MetaLayer):

    config_properties = [
      {'name': 'pgsql_hostname', 'description': 'PostGIS host name or IP.'},
      {'name': 'pgsql_port', 'description': 'PostGIS port.'},
      {'name': 'pgsql_database', 'description': 'PostGIS database name.'},
      {'name': 'pgsql_username', 'description': 'PostGIS username.'},
      {'name': 'pgsql_password', 'description': 'PostGIS password.'},
    ] + TileCache.Layer.MetaLayer.config_properties 
    
    def __init__(self, name, pgsql_hostname=None, pgsql_port=None, pgsql_database=None, pgsql_username=None, pgsql_password=None, **kwargs):
        """ call super.__init__, but also store the map_id from PATH_INFO
        """
        # the result set ID is the part of the path just before the layer name
        self.map_id = int(os.environ["PATH_INFO"].lstrip('/').split('/')[-5])

        self.hostname = pgsql_hostname
        self.port = pgsql_port
        self.database = pgsql_database
        self.username = pgsql_username
        self.password = pgsql_password

        # add id to name
        name = name + str(self.map_id)
        TileCache.Layer.MetaLayer.__init__(self, name, **kwargs)
    
    def renderTile(self, tile, force=None):
        """
        """
        # open a log file, or not, either way is cool
        log = False #open(os.path.dirname(__file__)+'/log.txt', 'a')
        
        # grab points data
        db = Data.get_db_cursor(database=self.database, port=self.port, host=self.hostname, user=self.username, password=self.password)
        points = Data.get_place_times(self.map_id, tile, db, log)
        
        # render a PIL image
        image = draw_tile(points, tile, log)

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

def draw_tile(points, tile, log):
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
    array = numpy.ones(tile.size(), numpy.int32) * 0xFFFFFF
    
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
        x, y = transform(x, y)
        draw_station(array, station_cone + t, station_mask, int(x), int(y))

    points_time = time.time() - points_start

    if log:
        print >> log, 'Tile %d/%d/%d' % (tile.z, tile.x, tile.y),
        print >> log, 'prep: %.2fs, %dx%d cone: %.2fs,' % (prep_time, station_cone.shape[0], station_cone.shape[1], cone_time),
        print >> log, '%d points, %d points/sec,' % (len(points), len(points) / points_time),
        print >> log, '%.1fm point-pixels/sec,' % ((len(points) * station_cone.shape[0] * station_cone.shape[1]) / (points_time * 1000000)),
        print >> log, 'total: %.2fs' % (prep_time + cone_time + points_time)
        
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
    target[mask] = numpy.minimum(target, value)[mask]

def img2str(image, format):
    """ Convert image to a data buffer in a given format, e.g. PNG or JPEG
    """
    buffer = StringIO.StringIO()
    image.save(buffer, format)
    buffer.seek(0)
    return buffer.read()

def arr2img(arr):
    """ Convert numpy.array to PIL.Image.
    """
    # convert to 32bit unsigned int
    arr = arr.astype(numpy.uint32)
    
    # shift unsigned int from RGB to RGBA
    arr = (arr << 8) | 0x000000FF

    # account for byte order, this may be an issue
    if arr.dtype.byteorder == '<' or (arr.dtype.byteorder == '=' and numpy.little_endian):
        arr = arr.byteswap()

    return PIL.Image.fromstring('RGBA', (arr.shape[1], arr.shape[0]), arr.tostring())
