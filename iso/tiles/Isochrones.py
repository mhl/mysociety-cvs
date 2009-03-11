import os
import sys
import os.path
import StringIO
import pyproj
import TileCache
import PIL.Image

class TextLayer(TileCache.Layer.MetaLayer):

    def __init__(self, *args, **kwargs):
        """ call super.__init__, but also store the results_id from PATH_INFO
        """
        TileCache.Layer.MetaLayer.__init__(self, *args, **kwargs)

        # the result set ID is the first part of the path
        self.results_id = os.environ["PATH_INFO"].lstrip('/').split('/')[0]
    
    def renderTile(self, tile, force=None):
        """
        """
        # get the tile in spherical mercator
        xmin, ymin, xmax, ymax = tile.bounds()
        width, height = tile.size()
        
        # make conversion stuffs for spherical mercator points back to tile space
        xoffset, yoffset = -xmin, -ymin
        xscale, yscale = width / float(xmax - xmin), height / float(ymax - ymin)
        transform = lambda x, y: (xscale * (x + xoffset), yscale * (y + yoffset))
        
        image = PIL.Image.new('L', tile.size(), 0x00)
        
        for (x, y, t) in get_data(self.results_id, tile):
            x, y = transform(*bng2gym(x, y))
            
            if 0 <= x and x <= width and 0 <= y and y <= height:
                # TODO: why is this upside-down?
                image.putpixel((x, height - y), 0xFF)

        tile.data = img2str(image, self.extension)

        return tile.data 

BNG = pyproj.Proj(proj='tmerc', lat_0=49, lon_0=-2, k=0.999601, x_0=400000, y_0=-100000, ellps='airy', towgs84='446.448,-125.157,542.060,0.1502,0.2470,0.8421,-20.4894', units='m', no_defs=True)
GYM = pyproj.Proj(proj='merc', a=6378137, b=6378137, lat_ts=0.0, lon_0=0.0, x_0=0.0, y_0=0, k=1.0, units='m', nadgrids=None, no_defs=True)

def img2str(image, format):
    """
    """
    buffer = StringIO.StringIO()
    image.save(buffer, format)
    buffer.seek(0)
    return buffer.read()

def bng2gym(x, y):
    """
    """
    return GYM(*BNG(x, y, inverse=True))

def gym2bng(x, y):
    """
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

