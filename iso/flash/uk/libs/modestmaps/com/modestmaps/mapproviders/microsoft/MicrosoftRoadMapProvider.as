package com.modestmaps.mapproviders.microsoft
{
	/**
	 * @author darren
	 * $Id: MicrosoftRoadMapProvider.as,v 1.1 2009-03-20 02:08:57 allens Exp $
	 */
	public class MicrosoftRoadMapProvider extends MicrosoftProvider
	{
	    public function MicrosoftRoadMapProvider(hillShading:Boolean=true, minZoom:int=MIN_ZOOM, maxZoom:int=MAX_ZOOM)
	    {
	        super(ROAD, hillShading, minZoom, maxZoom);
	    }
	}
}
