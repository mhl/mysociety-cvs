package com.modestmaps.mapproviders.microsoft
{
	/**
	 * @author darren
	 * $Id: MicrosoftHybridMapProvider.as,v 1.1 2009-03-20 02:08:57 allens Exp $
	 */
	public class MicrosoftHybridMapProvider extends MicrosoftProvider
	{
		public function MicrosoftHybridMapProvider(minZoom:int=MIN_ZOOM, maxZoom:int=MAX_ZOOM)
		{
			super(HYBRID, true, minZoom, maxZoom);
		}
	}
}