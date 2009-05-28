package org.mysociety.display
{
    import com.modestmaps.mapproviders.IMapProvider;
    
    import flash.display.Bitmap;
    import flash.display.BitmapData;
    import flash.events.Event;
    import flash.geom.Point;

    public class BitmapThresholdMap extends BitmapCacheMap
    {
        protected var _maskBitmap:BitmapData;
        protected var thresholdMask:uint = BitmapCacheMap.MASK_RGB;
        
        protected var absMinThreshold:uint = 0;
        protected var absMaxThreshold:uint = 0xFFFFFFFF;

        protected var _minThreshold:uint = absMinThreshold;
        protected var _maxThreshold:uint = absMaxThreshold;
        
        protected var transparent:Boolean = true;
        protected var _offColor:uint = 0xFF000000;
        protected var _onColor:uint = 0xFFFFFFFF;
        protected var display:Bitmap;
        
        protected var _dirty:Boolean = false;
        
        public function BitmapThresholdMap(width:Number=320, height:Number=240, draggable:Boolean=true, mapProvider:IMapProvider=null, ...rest)
        {
            display = new Bitmap();
            super(width, height, draggable, mapProvider, rest);
            addChild(display);
            
            grid.visible = false;
        }
        
        public function get offColor():uint
        {
            return _offColor;
        }
        
        public function set offColor(value:uint):void
        {
            if (offColor != value)
            {
                _offColor = value;
                dirty = true;
            }
        }
        
        public function get onColor():uint
        {
            return _onColor;
        }
        
        public function set onColor(value:uint):void
        {
            if (onColor != value)
            {
                _onColor = value;
                dirty = true;
            }
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
            display.visible = false;
            grid.visible = true;
            super.onRendered(event);
            display.visible = true;
            grid.visible = false;

            _maskBitmap.fillRect(_cache.rect, onColor);
            
            if (minThreshold > absMinThreshold)
                _maskBitmap.threshold(_cache, _cache.rect, new Point(), '<', _minThreshold, offColor, thresholdMask);
                
            if (maxThreshold < absMaxThreshold)
                _maskBitmap.threshold(_cache, _cache.rect, new Point(), '>', _maxThreshold, offColor, thresholdMask);

            dirty = false;
        }
        
        override protected function onResized(event:Event):void
        {
            super.onResized(event);
            if (_cache)
            {
                display.bitmapData = _maskBitmap = new BitmapData(_cache.width, _cache.height, transparent, offColor);
            }
        }
    }
}