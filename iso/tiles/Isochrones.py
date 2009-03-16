import os
import sys
import os.path
import StringIO

import numpy
import pyproj
import TileCache
import PIL.Image
import Cone

class TextLayer(TileCache.Layer.MetaLayer):

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
        # get the tile in spherical mercator
        xmin, ymin, xmax, ymax = tile.bounds()
        width, height = tile.size()
        
        # make conversion stuffs for spherical mercator points back to tile space
        xoffset, yoffset = -xmin, -ymin
        xscale, yscale = width / float(xmax - xmin), height / float(ymax - ymin)
        transform = lambda x, y: (xscale * (x + xoffset), yscale * (y + yoffset))
        
        # create an array to hold travel times
        # note that here 0x00 = zero time, 0xFF = inaccessible; inversion happens later
        array = numpy.ones(tile.size(), numpy.int32) * self.timestep * 255
        
        # 1800 meters is a half hour of walking at 1m/s
        pixels_per_1800_meters = 1.8 * Cone.pixels_per_kilometer(tile)
        
        # create a station cone and mask where value is walking seconds
        station_cone = Cone.make_cone(int(pixels_per_1800_meters))
        station_mask = station_cone <= 1800

        # add each found data point in turn, offseting station cones by base station time
        for (x, y, t) in get_data(self.results_id, tile):
            x, y = transform(*bng2gym(x, y))
            draw_station(array, station_cone + t, station_mask, int(x), int(y))
            
        # convert array to an image
        image = arr2img(-array / self.timestep + 256)
        
        # we rotate the image to deal with row/col vs. x/y transposition in numpy and some other geometry oddness
        image = image.transpose(PIL.Image.ROTATE_90)

        tile.data = img2str(image, self.extension)

        return tile.data 

def draw_station(array, station, mask, x, y):
    """ Given a base map array and a timescaled station array, drop the station
        onto the base map using a minimum filter to correctly overwrite longer times.
    """
    axmin = x - station.shape[0] / 2
    axmax = axmin + station.shape[0]

    aymin = y - station.shape[1] / 2
    aymax = aymin + station.shape[1]
    
    sxmin, symin, sxmax, symax = 0, 0, station.shape[0], station.shape[1]
    
    # find bounds where necessary
    
    assert axmax - axmin == sxmax - sxmin
    assert aymax - aymin == symax - symin
    
    if axmin < 0:
        axmin, sxmin = 0, -axmin
    
    if aymin < 0:
        aymin, symin = 0, -aymin

    if axmax > array.shape[0]:
        axmax, sxmax = array.shape[0], sxmax - (axmax - array.shape[0])

    if aymax > array.shape[1]:
        aymax, symax = array.shape[1], symax - (aymax - array.shape[1])

    assert axmax - axmin == sxmax - sxmin
    assert aymax - aymin == symax - symin
    
    if axmax <= 0 or aymax <= 0:
        return
    
    if axmin > array.shape[0] or aymin > array.shape[1]:
        return

    target = array[axmin:axmax, aymin:aymax]
    value = station[sxmin:sxmax, symin:symax]
    mask = mask[sxmin:sxmax, symin:symax]
    
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

