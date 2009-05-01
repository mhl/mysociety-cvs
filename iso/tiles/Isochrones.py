"""
Custom TileCache module for rendering of isochrone images based on travel time data.

Copyright (c) 2009 UK Citizens Online Democracy. All rights reserved.
Email: mike@stamen.com; WWW: http://www.mysociety.org/

$Id: Isochrones.py,v 1.30 2009-05-01 00:22:41 francis Exp $
"""
import os
import sys
import time
import os.path
import StringIO

import numpy
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
      {'name': 'tmpwork', 'description': 'Directory where iso files are put.'},
      {'name': 'iso_tile_log', 'description': 'Log file, or none for none'},
    ] + TileCache.Layer.MetaLayer.config_properties 
    
    def __init__(self, name, pgsql_hostname=None, pgsql_port=None, pgsql_database=None, pgsql_username=None, pgsql_password=None, tmpwork=None, iso_tile_log=None, **kwargs):
        """ call super.__init__, store some other details,
            and make a permanent connection to the database
        """
        self.basename = name
        self.map_id = None

        self.hostname = pgsql_hostname
        self.port = pgsql_port
        self.database = pgsql_database
        self.username = pgsql_username
        self.password = pgsql_password
        self.tmpwork = tmpwork
        self.iso_tile_log = iso_tile_log

        self.db = Data.get_db_cursor(database=self.database, port=self.port, host=self.hostname, user=self.username, password=self.password)

        TileCache.Layer.MetaLayer.__init__(self, name, **kwargs)
        self.init_kwargs = kwargs
    
    def updatePathInfo(self, path_info):
        """
        """
        # the map ID overloads the first part of the TMS path: /1.0.0/iso/0/0/0.jpg
        self.map_id = int(path_info.lstrip('/').split('/')[-5])

        # add id to name
        name = self.basename + str(self.map_id)
        TileCache.Layer.MetaLayer.__init__(self, name, **self.init_kwargs)
    
    def renderTile(self, tile, force=None):
        """
        """
        # open a log file, or not, either way is cool
        log = self.iso_tile_log and open(self.iso_tile_log, 'a') or None

        if self.map_id is None:
            raise Exception('self.map_id is missing, did you forget to call updatePathInfo()?')
        
        # grab points data
        points = Data.get_place_times(self.map_id, tile, self.db, log, self.tmpwork)
        
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
    
    # 2400 meters is a half hour of walking at 1.34 m/s
    pixels_per_max_walk_meters = 2400 * Cone.pixels_per_kilometer(tile) / 1000
    
    prep_time = time.time() - prep_start
    cone_start = time.time()
    
    # create a station cone and mask where value is walking seconds
    station_cone = Cone.make_cone(pixels_per_max_walk_meters)
    station_mask = station_cone <= 2400
    
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
