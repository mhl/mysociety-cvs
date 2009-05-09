"""
Custom TileCache module for rendering of heat grids based on GDAL VRT files.

Copyright (c) 2009 UK Citizens Online Democracy. All rights reserved.
Email: mike@stamen.com; WWW: http://www.mysociety.org/

$Id: LandMasses.py,v 1.1 2009-05-09 00:39:14 migurski Exp $
"""
import os
import sys
import StringIO

import PIL.Image
import TileCache

import mapnik

class LandMassLayer(TileCache.Layer.MetaLayer):

    def renderTile(self, tile, force=None):
        """
        """
        width, height = tile.size()
        
        map = mapnik.Map(width, height, "+proj=merc +a=6378137 +b=6378137 +lat_ts=0.0 +lon_0=0.0 +x_0=0.0 +y_0=0 +k=1.0 +units=m +nadgrids=@null +no_defs")
        map.background = mapnik.Color('white')
        
        style = mapnik.Style()
        
        rule = mapnik.Rule()
        rule.symbols.append(mapnik.PolygonSymbolizer(mapnik.Color('black')))
        rule.symbols.append(mapnik.LineSymbolizer(mapnik.Color('black'), .5))
        
        style.rules.append(rule)
        
        map.append_style('Dry Land', style)
        
        layer = mapnik.Layer('world')
        
        # comes from http://hypercube.telascience.org/~kleptog/processed_p.zip
        layer.datasource = mapnik.Shapefile(file='landmass/processed_p')
        layer.styles.append('Dry Land')
        layer.srs = map.srs
        
        map.layers.append(layer)
        
        xmin, ymin, xmax, ymax = tile.bounds()
        box = mapnik.Envelope(mapnik.Coord(xmin, ymin), mapnik.Coord(xmax, ymax))
        map.zoom_to_box(box)
        
        img = mapnik.Image(width, height)
        mapnik.render(map, img)
        img = PIL.Image.fromstring('RGBA', (width, height), img.tostring())
        img = img.convert('1').convert('L')
        
        tile.data = img2str(img, self.extension)

        return tile.data

def img2str(image, format):
    """ Convert image to a data buffer in a given format, e.g. PNG or JPEG
    """
    buffer = StringIO.StringIO()
    image.save(buffer, format)
    buffer.seek(0)
    return buffer.read()
