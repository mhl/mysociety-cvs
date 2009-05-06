"""
Custom TileCache module for rendering of heat grids based on GDAL VRT files.

Copyright (c) 2009 UK Citizens Online Democracy. All rights reserved.
Email: mike@stamen.com; WWW: http://www.mysociety.org/

$Id: HeatGrids.py,v 1.5 2009-05-06 23:58:45 migurski Exp $
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

class ScenicLayer(TileCache.Layer.MetaLayer):

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
    
    def renderTile(self, tile, force=None):
        """
        """
        # open a log file, or not, either way is cool
        log = self.iso_tile_log and open(self.iso_tile_log, 'a') or None
        
        radius = 10000
        datafile = self.datafile
        xmin, ymin, xmax, ymax = tile.bounds()
        width, height = tile.size()
        
        # grab points data
        print >> log, (xmin, ymin, xmax, ymax), (width, height)
        
        (handle, filename) = tempfile.mkstemp(suffix='.tif', prefix='scenic-grid-')
        os.close(handle)
        
        # render an image
        cmd = '/usr/bin/gdal_grid -a invdist:power=2.0:smoothing=2.0:radius1=%(radius)d:radius2=%(radius)d ' % locals() \
            + '-txe %(xmin)f %(xmax)f -tye %(ymin)f %(ymax)f -outsize %(width)d %(height)d ' % locals() \
            + '-l scenicness.2009-04-29 -of GTiff -ot Float32 %(datafile)s %(filename)s' % locals()

        print >> log, cmd
        
        status, output = commands.getstatusoutput(cmd)

        print >> log, status
        
        if status == 0:
        
            heat = gdal.Open(filename)
            band = heat.GetRasterBand(1)
            cols, rows = heat.RasterXSize, heat.RasterYSize
            
            print >> log, cols, rows
            
            data = band.ReadRaster(0, 0, cols, rows, buf_type=gdal.GDT_Float32)
            
            print >> log, repr(data[:16]), struct.unpack('ffff', data[:16])
            
            cell = numpy.fromstring(data, dtype=numpy.float32).reshape(rows, cols)

            # flip it, because GDAL gives it to us upside-down
            image = arr2img(cell * 1)
            image = PIL.ImageOps.flip(image)
        
        os.unlink(filename)
        
        tile.data = img2str(image, self.extension)

        return tile.data

class HousingLayer(TileCache.Layer.MetaLayer):

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
    
    def renderTile(self, tile, force=None):
        """
        """
        # open a log file, or not, either way is cool
        log = self.iso_tile_log and open(self.iso_tile_log, 'a') or None
        
        radius = 10000
        datafile = self.datafile
        xmin, ymin, xmax, ymax = tile.bounds()
        width, height = tile.size()
        
        # grab points data
        print >> log, (xmin, ymin, xmax, ymax), (width, height)
        
        (handle, filename) = tempfile.mkstemp(suffix='.tif', prefix='scenic-grid-')
        os.close(handle)
        
        # render an image
        cmd = '/usr/bin/gdal_grid -a average:radius1=%(radius)d:radius2=%(radius)d ' % locals() \
            + '-txe %(xmin)f %(xmax)f -tye %(ymin)f %(ymax)f -outsize %(width)d %(height)d ' % locals() \
            + '-l housingprices -of GTiff -ot Float32 %(datafile)s %(filename)s' % locals()

        print >> log, cmd
        
        status, output = commands.getstatusoutput(cmd)

        print >> log, status
        
        if status == 0:
        
            heat = gdal.Open(filename)
            band = heat.GetRasterBand(1)
            cols, rows = heat.RasterXSize, heat.RasterYSize
            
            print >> log, cols, rows
            
            data = band.ReadRaster(0, 0, cols, rows, buf_type=gdal.GDT_Float32)
            
            print >> log, repr(data[:16]), struct.unpack('ffff', data[:16])
            
            cell = numpy.fromstring(data, dtype=numpy.float32).reshape(rows, cols)
            
            print >> log, numpy.min(cell), '-', numpy.max(cell)

            # flip it, because GDAL gives it to us upside-down
            image = arr2img32(cell)
            image = PIL.ImageOps.flip(image)
        
        os.unlink(filename)
        
        tile.data = img2str(image, self.extension)

        return tile.data

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
