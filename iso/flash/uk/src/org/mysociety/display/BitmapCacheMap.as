package org.mysociety.display
{
    import com.modestmaps.Map;
    import com.modestmaps.core.TileGrid;
    import com.modestmaps.events.MapEvent;
    import com.modestmaps.mapproviders.IMapProvider;
    
    import flash.display.BitmapData;
    import flash.events.Event;
    import flash.geom.ColorTransform;
    import flash.geom.Rectangle;

    public class BitmapCacheMap extends Map
    {
        public static const CLEAR:uint = 0x00FFFFFF;
        public static const WHITE:uint = 0xFFFFFFFF;
        public static const BLACK:uint = 0xFF000000;

        public static const MASK_RGB:uint = 0x00FFFFFF;
        public static const MASK_ARGB:uint = 0xFFFFFFFF;
        public static const MASK_ALPHA:uint = 0xFF000000;
        
        public static const INVERT:ColorTransform = new ColorTransform(-1, -1, -1, 1, 255, 255, 255, 0);

        public var backgroundColor:uint = CLEAR;
        protected var _cache:BitmapData;
        
        public function BitmapCacheMap(width:Number=320, height:Number=240, draggable:Boolean=true, mapProvider:IMapProvider=null, ...rest)
        {
            addEventListener(MapEvent.RESIZED, onResized);
            addEventListener(MapEvent.RENDERED, onRendered);
            
            super(width, height, draggable, mapProvider, rest);
            
            TileGrid.cacheLoaders = true;
        }
        
        protected function onResized(event:Event):void
        {
            _cache = new BitmapData(Math.max(mapWidth, 1), Math.max(mapHeight, 1), true, backgroundColor);
            onRendered(null);
        }
        
        protected function onRendered(event:Event):void
        {
            // trace('* render');
            if (_cache)
            {
                _cache.fillRect(_cache.rect, backgroundColor);
                _cache.draw(this, null, null, null, scrollRect, false);
            }
        }

        public function get cache():BitmapData
        {
            return _cache;
        }
    }
}
