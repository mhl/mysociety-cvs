"""
Custom TileCache module for rendering of heat grids based on GDAL VRT files.

Copyright (c) 2009 UK Citizens Online Democracy. All rights reserved.
Email: mike@stamen.com; WWW: http://www.mysociety.org/

$Id: HeatGrids.py,v 1.14 2009-05-14 11:18:26 francis Exp $
"""
import os
import sys
import time
import os.path
import StringIO
import tempfile
import commands
import struct

import numpy
import PIL.Image, PIL.ImageOps
import TileCache
import osgeo.gdal as gdal

class GenericHeatGridLayer(TileCache.Layer.MetaLayer):
    config_properties = [
      {'name': 'datafile', 'description': 'VRT datafile'},
      {'name': 'iso_tile_log', 'description': 'Log file, or none for none'},
    ] + TileCache.Layer.MetaLayer.config_properties 

    def __init__(self, name, datafile=None, iso_tile_log=None, **kwargs):
        """ call super.__init__, store some other details,
            and make a permanent connection to the database
        """
        self.datafile = datafile
        self.iso_tile_log = iso_tile_log

        TileCache.Layer.MetaLayer.__init__(self, name, **kwargs)

    def renderTile(self, tile):
        """
        """
        # open a log file, or not, either way is cool
        log = self.iso_tile_log and open(self.iso_tile_log, 'a') or None
        
        radius = self.get_radius()
        datafile = self.datafile
        xmin, ymin, xmax, ymax = tile.bounds()
        width, height = tile.size()
        layer_name = self.layer_name()
        
        # grab points data
        print >> log, (xmin, ymin, xmax, ymax), (width, height)
        
        (handle, filename) = tempfile.mkstemp(suffix='.tif', prefix='scenic-grid-')
        os.close(handle)

        where_clause = """-where "Easting >= %d and Northing >= %d and Easting <= %d and Northing <= %d" """ % (int(xmin - radius), int(ymin - radius), int(xmax + radius), int(ymax + radius))

        # render an image
        cmd = self.get_gdal_command(locals())
        cmd += '-txe %(xmin)f %(xmax)f -tye %(ymin)f %(ymax)f -outsize %(width)d %(height)d ' % locals() \
            + '%(where_clause)s -l %(layer_name)s -of GTiff -ot Float32 %(datafile)s %(filename)s' % locals()

        print >> log, cmd
        
        status, output = commands.getstatusoutput(cmd)

        print >> log, "gdal_grid output status", status
        
        if status != 0:
            raise Exception("Got error code from GDAL " + str(status) + " message " + output)
    
        heat = gdal.Open(filename)
        band = heat.GetRasterBand(1)
        cols, rows = heat.RasterXSize, heat.RasterYSize
        
        print >> log, "raster cols, rows", cols, rows
        
        data = band.ReadRaster(0, 0, cols, rows, buf_type=gdal.GDT_Float32)
        
        print >> log, "start of data", repr(data[:16]), struct.unpack('ffff', data[:16])
        
        cell = numpy.fromstring(data, dtype=numpy.float32).reshape(rows, cols)

        print >> log, "min, max", numpy.min(cell), '-', numpy.max(cell)

        # flip it, because GDAL gives it to us upside-down
        image = self.convert_cell_to_image(cell)
        image = PIL.ImageOps.flip(image)
        
        os.unlink(filename)
        
        tile.data = img2str(image, self.extension)

        return tile.data
 
class ScenicLayer(GenericHeatGridLayer):
    def get_gdal_command(self, params):
        cmd = '/usr/bin/gdal_grid -a invdist:power=2.0:smoothing=2.0:radius1=%(radius)d:radius2=%(radius)d ' % params
        return cmd

    def convert_cell_to_image(self, cell):
        image = arr2img(cell * 10)
        return image

    def layer_name(self):
        return "scenic"

    def get_radius(self):
        return 10000

class HousingLayer(GenericHeatGridLayer):
    def get_gdal_command(self, params):
        cmd = '/usr/bin/gdal_grid -a invdist:power=2.0:smoothing=2.0:min_points=3:radius1=%(radius)d:radius2=%(radius)d ' % params
        return cmd

    def convert_cell_to_image(self, cell):
        image = arr2img32(cell)
        return image

    def layer_name(self):
        return "housingprices"

    def get_radius(self):
        return 5000

def arr2img(ar):
    """ Convert Numeric.array to PIL.Image.
    """
    return PIL.Image.fromstring('L', (ar.shape[1], ar.shape[0]), ar.astype('b').tostring())

def arr2img32(arr):
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

def img2str(image, format):
    """ Convert image to a data buffer in a given format, e.g. PNG or JPEG
    """
    buffer = StringIO.StringIO()
    image.save(buffer, format)
    buffer.seek(0)
    return buffer.read()
