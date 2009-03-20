/**
 * @author migurski
 * $Id: BlueMarbleMapProvider.as,v 1.1 2009-03-20 02:08:56 allens Exp $
 */
package com.modestmaps.mapproviders
{
	import com.modestmaps.core.Coordinate;
	
	public class BlueMarbleMapProvider 
		extends AbstractMapProvider
		implements IMapProvider
	{
	    public function BlueMarbleMapProvider(minZoom:int=MIN_ZOOM, maxZoom:int=MAX_ZOOM)
        {
            super(minZoom, Math.min(9, maxZoom));
	    }
	
	    public function toString():String
	    {
	        return "BLUE_MARBLE";
	    }
	
	    public function getTileUrls(coord:Coordinate):Array
	    {
	        var sourceCoord:Coordinate = sourceCoordinate(coord);
	        if (sourceCoord.row < 0 || sourceCoord.row >= Math.pow(2, coord.zoom)) {
	        	return [];
	    	}
	        return [ 'http://s3.amazonaws.com/com.modestmaps.bluemarble/' + 
	        		 (sourceCoord.zoom) + '-r' + (sourceCoord.row) + '-c' + (sourceCoord.column) +
	        	    '.jpg' ];
	    }
	    
	}
}