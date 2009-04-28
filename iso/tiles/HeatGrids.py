"""
Custom TileCache module for rendering of heat grids based on GDAL VRT files.

Copyright (c) 2009 UK Citizens Online Democracy. All rights reserved.
Email: mike@stamen.com; WWW: http://www.mysociety.org/

$Id: HeatGrids.py,v 1.1 2009-04-28 00:24:18 migurski Exp $
"""
import os
import sys
import time
import os.path
import StringIO
import tempfile

import PIL.Image
import TileCache

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
        
        radius = 5000
        datafile = self.datafile
        xmin, ymin, xmax, ymax = tile.bounds()
        width, height = tile.size()
        
        # grab points data
        print >> log, (xmin, ymin, xmax, ymax), (width, height)
        
        (handle, filename) = tempfile.mkstemp(suffix='.tif', prefix='scenic-grid-')
        os.close(handle)
        
        # render an image
        cmd = '/opt/local/bin/gdal_grid -a average:radius1=%(radius)d:radius2=%(radius)d ' % locals() \
            + '-txe %(xmin)f %(xmax)f -tye %(ymin)f %(ymax)f -outsize %(width)d %(height)d ' % locals() \
            + '-l scenicness.2009-04-27 -of GTiff -ot Float32 %(datafile)s %(filename)s' % locals()

        print >> log, cmd
        
        os.unlink(filename)
        
        tile.data = img2str(image, self.extension)

        return tile.data

def img2str(image, format):
    """ Convert image to a data buffer in a given format, e.g. PNG or JPEG
    """
    buffer = StringIO.StringIO()
    image.save(buffer, format)
    buffer.seek(0)
    return buffer.read()
