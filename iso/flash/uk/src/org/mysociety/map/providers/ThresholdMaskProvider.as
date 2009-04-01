package org.mysociety.map.providers
{
    import com.modestmaps.core.Coordinate;
    import com.modestmaps.mapproviders.OpenStreetMapProvider;
    import com.stamen.utils.StringUtils;

    public class ThresholdMaskProvider extends OpenStreetMapProvider
    {
        // protected var _baseURL:String = 'http://studio.stamen.com/~tom/mysociety_tiles/$z/$r/$c.png';
        protected var _baseURL:String = 'http://locog.stamen.com/~allens/mysociety/guardian-tiles/out/{Z}-r{Y}-c{X}.png';
        
        public function ThresholdMaskProvider(baseURL:String=null, minZoom:int=MIN_ZOOM, maxZoom:int=MAX_ZOOM)
        {
            super(minZoom, maxZoom);
            if (baseURL) this.baseURL = baseURL;
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

            // work out which subdomain to retrieve it from 
            var server:String = [ 'a.', 'b.', 'c.', '' ][int(mod.row + mod.column) % 4];
            url = StringUtils.replace(url, { 'http://' : 'http://'+server });

            return [url];
        }
        
        override public function toString():String
        {
            return 'THRESHOLD_MASK_' + baseURL;
        }
    }
}
