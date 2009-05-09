package org.mysociety.display
{
    import com.modestmaps.mapproviders.IMapProvider;
    
    import flash.display.Bitmap;
    import flash.display.BitmapData;
    import flash.events.Event;
    import flash.events.MouseEvent;
    import flash.geom.Point;

    public class BitmapThresholdMap extends BitmapCacheMap
    {
        protected var _maskBitmap:BitmapData;
        protected var thresholdMask:uint = BitmapCacheMap.MASK_RGB;
        
        protected var absMinThreshold:uint = 0;
        protected var absMaxThreshold:uint = 0xFFFFFFFF;

        protected var _minThreshold:uint = absMinThreshold;
        protected var _maxThreshold:uint = absMaxThreshold;
        
        protected var transparent:Boolean = false;
        protected var offColor:uint = 0xFF000000;
        protected var onColor:uint = 0xFFFFFFFF;
        
        protected var _dirty:Boolean = false;
        
        public function BitmapThresholdMap(width:Number=320, height:Number=240, draggable:Boolean=true, mapProvider:IMapProvider=null, ...rest)
        {
            super(width, height, draggable, mapProvider, rest);
        }
        
        public function get minThreshold():uint
        {
            return _minThreshold;
        }
        
        public function set minThreshold(value:uint):void
        {
            // value = Math.max(value, absMinThreshold);
            if (minThreshold != value)
            {
                _minThreshold = value;
                dirty = true;
            }
        }
        
        public function get maxThreshold():uint
        {
            return _maxThreshold;
        }
        
        public function set maxThreshold(value:uint):void
        {
            // value = Math.min(value, absMaxThreshold);
            if (maxThreshold != value)
            {
                _maxThreshold = value;
                dirty = true;
            }
        }
        
        public function get maskBitmap():BitmapData
        {
            return _maskBitmap;
        }
        
        public function get dirty():Boolean
        {
            return _dirty;
        }
        
        public function set dirty(value:Boolean):void
        {
            if (dirty != value)
            {
                _dirty = value;
                if (value)
                {
                    addEventListener(Event.ENTER_FRAME, rasterize);
                }
                else
                {
                    removeEventListener(Event.ENTER_FRAME, rasterize);
                }
            }
        }
        
        override protected function onRendered(event:Event):void
        {
            dirty = true;
        }
        
        protected function rasterize(event:Event=null):void
        {
            if (!_maskBitmap) return;
            
            // update the cache
            super.onRendered(event);

            _maskBitmap.fillRect(_maskBitmap.rect, onColor);
            if (minThreshold > absMinThreshold)
                _maskBitmap.threshold(_cache, _cache.rect, new Point(), '<', _minThreshold, offColor, thresholdMask);
            if (maxThreshold < absMaxThreshold)
                _maskBitmap.threshold(_cache, _cache.rect, new Point(), '>', _maxThreshold, offColor, thresholdMask);

            /*                
            if (name == 'scenicness')
            {
                trace('min:', minThreshold, 'max:', maxThreshold);
                trace(_maskBitmap.getPixel32(_maskBitmap.width / 2, _maskBitmap.height / 2).toString(16));
            }
            */
            dirty = false;
        }
        
        override protected function onResized(event:Event):void
        {
            super.onResized(event);
            if (_cache)
            {
                _maskBitmap = new BitmapData(_cache.width, _cache.height, transparent, offColor);
            }
        }
    }
}