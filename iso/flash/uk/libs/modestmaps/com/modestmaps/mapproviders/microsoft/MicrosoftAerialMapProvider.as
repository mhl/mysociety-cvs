
package com.modestmaps.mapproviders.microsoft
{
	/**
	 * @author darren
	 * $Id: MicrosoftAerialMapProvider.as,v 1.1 2009-03-20 02:08:57 allens Exp $
	 */
	public class MicrosoftAerialMapProvider extends MicrosoftProvider
	{
		public function MicrosoftAerialMapProvider(minZoom:int=MIN_ZOOM, maxZoom:int=MAX_ZOOM)
		{
			super(AERIAL, true, minZoom, maxZoom);
		}
	}
}