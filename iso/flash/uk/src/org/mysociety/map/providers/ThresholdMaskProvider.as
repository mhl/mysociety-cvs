package org.mysociety.map.providers
{
    import com.modestmaps.core.Coordinate;
    import com.modestmaps.mapproviders.OpenStreetMapProvider;
    import com.stamen.utils.StringUtils;

    public class ThresholdMaskProvider extends OpenStreetMapProvider
    {
        public var subdomains:Array;
        protected var _baseURL:String;
        
        public function ThresholdMaskProvider(baseURL:String, subdomains:Array=null, minZoom:int=MIN_ZOOM, maxZoom:int=MAX_ZOOM)
        {
            super(minZoom, maxZoom);
            this.baseURL = baseURL;
            this.subdomains = subdomains;
        }
        
        public function get baseURL():String
        {
            return _baseURL;
        }
        
        public function set baseURL(value:String):void
        {
            // for backwards compatibility with old Europe maps
            _baseURL = StringUtils.replace(value, {'$z': '{Z}', '$r': '{Y}', '$c': '{X}'});
        }
        
        override public function getTileUrls(coord:Coordinate):Array
        {
            var mod:Coordinate = coord.copy();

            // fill in coordinates into URL
            var url:String = baseURL.replace('{Z}', mod.zoom).replace('{X}', mod.column).replace('{Y}', mod.row);

            // replace the {S} portion of the url with the appropriate subdomain
            if (url.indexOf('{S}') > -1)
            {
                var subdomain:String = (subdomains && subdomains.length > 0)
                                       ? subdomains[int(mod.row + mod.column) % subdomains.length]
                                       : '';
                url = url.replace('{S}', subdomain ? subdomain + '.' : '');
            }

            return [url];
        }
        
        override public function toString():String
        {
            return 'THRESHOLD_MASK_' + baseURL;
        }
    }
}
