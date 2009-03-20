package com.modestmaps.mapproviders.yahoo
{
	import com.modestmaps.core.Coordinate;
	import com.modestmaps.mapproviders.AbstractMapProvider;
	import com.modestmaps.mapproviders.IMapProvider;
	
	/**
	 * @author darren
	 * $Id: YahooRoadMapProvider.as,v 1.1 2009-03-20 02:08:57 allens Exp $
	 */
	public class YahooRoadMapProvider 
		extends AbstractMapProvider
		implements IMapProvider
	{
	    public function YahooRoadMapProvider(minZoom:int=MIN_ZOOM, maxZoom:int=MAX_ZOOM)
        {
            super(minZoom, maxZoom);
        }

		public function toString():String
		{
			return "YAHOO_ROAD";
		}
	
		public function getTileUrls(coord:Coordinate):Array
		{		
	        return [ "http://us.maps2.yimg.com/us.png.maps.yimg.com/png?v=3.52&t=m" + getZoomString(sourceCoordinate(coord)) ];
		}
		
		protected function getZoomString(coord:Coordinate):String
		{		
	        var row : Number = (Math.pow(2, coord.zoom) / 2) - coord.row - 1;
			return "&x=" + coord.column + "&y=" + row + "&z=" + (18 - coord.zoom);
		}	
	}
}