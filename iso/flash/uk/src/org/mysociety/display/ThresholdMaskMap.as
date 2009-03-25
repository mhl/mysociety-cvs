package org.mysociety.display
{
    import com.modestmaps.Map;
    import com.modestmaps.events.MapEvent;
    import com.modestmaps.mapproviders.IMapProvider;
    import com.modestmaps.overlays.MarkerClip;
    import com.stamen.ui.BlockSprite;
    
    import flash.display.Bitmap;
    import flash.display.BitmapData;
    import flash.display.BitmapDataChannel;
    import flash.display.PixelSnapping;
    import flash.events.Event;
    import flash.events.MouseEvent;
    import flash.events.ProgressEvent;
    import flash.filters.BitmapFilter;
    import flash.filters.ColorMatrixFilter;
    import flash.geom.ColorTransform;
    import flash.geom.Matrix;
    import flash.geom.Point;
    import flash.geom.Rectangle;
    import flash.utils.getTimer;
    
    import org.mysociety.map.providers.ThresholdMaskProvider;

    public class ThresholdMaskMap extends BlockSprite
    {
        // pay attention to the whole RGB gamut
        public var thresholdMask:uint = 0x00FFFFFF;
        public var maskedFilter:ColorMatrixFilter;
        public var markerClip:MarkerClip;
        
        // blur the threshold edge with this
        public var thresholdBlur:BitmapFilter; // = new BlurFilter(7, 7, BitmapFilterQuality.MEDIUM);
        
        // this should either be a GlowFilter or ConvolutionFilter that draw an outline around the threshold mask
        public var outlineFilter:BitmapFilter;
        
        // this transform is applied to the outline if outlineFilter is set, *before* outlineFilter is applied
        // (so that you can invert the colors, for instance, which is helpful when you want to add a white outline)
        public var outlineColorTransform:ColorTransform;
        
        // different color outlines may require different blend modes (white: BlendMode.SCREEN; black: BlendMode.DARKEN)
        public var outlineBlendMode:String;
        
        protected var _displayMap:BitmapCacheMap;
        protected var _maskMap:BitmapCacheMap;
        protected var _dirty:Boolean = false;
        protected var rasterized:Bitmap;
        
        protected var absMinThreshold:uint = 0;
        protected var absMaxThreshold:uint = 0xFFFFFF;
        
        protected var _minThreshold:uint = absMinThreshold;
        
        protected var mapsLoaded:int = 0;
        
        public function ThresholdMaskMap(width:Number=640, height:Number=480, draggable:Boolean=true, provider:IMapProvider=null, thresholdBaseURL:String=null)
        {
            _displayMap = new BitmapCacheMap(width, height, draggable, provider);
            _displayMap.name = 'display';
            _displayMap.addEventListener(MouseEvent.DOUBLE_CLICK, _displayMap.onDoubleClick);
            //_displayMap.grid.setTileClass(NullTile);
            _displayMap.addEventListener(MapEvent.RENDERED, onDisplayMapRendered);
            _displayMap.grid.addEventListener(ProgressEvent.PROGRESS, onMapRendered);
            addChild(_displayMap);

            _maskMap = new BitmapCacheMap(width, height, false, new ThresholdMaskProvider(thresholdBaseURL));
            _maskMap.name = 'mask';
            //_maskMap.backgroundColor = 0x000000;
            //_maskMap.grid.setTileClass(NullTile);
            _maskMap.grid.addEventListener(ProgressEvent.PROGRESS, onMapRendered);
            _maskMap.mouseEnabled = _maskMap.mouseChildren = false;
            addChild(_maskMap);
            
            rasterized = new Bitmap(null, PixelSnapping.NEVER, false);
            addChild(rasterized);
            
            markerClip = new MarkerClip(_displayMap);
            addChild(markerClip);

            _maskMap.visible = false;
            _displayMap.alpha = 0;

            super(width, height, null);
            
            addEventListener(Event.ADDED_TO_STAGE, rasterize);
        }
        
        public function get displayMap():Map
        {
            return _displayMap;
        }
        
        public function get maskMap():Map
        {
            return _maskMap;
        }
        
        public function get minThreshold():uint
        {
            return _minThreshold;
        }
        
        public function set minThreshold(value:uint):void
        {
            value = Math.min(value, absMaxThreshold);
            if (minThreshold != value)
            {
                _minThreshold = value;
                updateThresholds();
            }
        }
        
        protected function updateThresholds():void
        {
            dirty = true;
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
                    // addEventListener(MapEvent.RENDERED, rasterize);
                }
                else
                {
                    removeEventListener(Event.ENTER_FRAME, rasterize);
                    // removeEventListener(MapEvent.RENDERED, rasterize);
                }
            }
        }
        
        public function getThresholdAtPoint(p:Point):int
        {
            var cache:BitmapData = _maskMap.cache;
            if (cache)
            {
                var color:uint = cache.getPixel32(p.x, p.y);
                return color & thresholdMask;
            }
            else
            {
                return -1;
            }
        }
        
        public function clear(event:Event=null):void
        {
            var bmp:BitmapData = rasterized.bitmapData;
            bmp.threshold(bmp, bmp.rect, new Point(), '!=', BitmapCacheMap.CLEAR, BitmapCacheMap.CLEAR, BitmapCacheMap.MASK_ARGB, false);
        }
        
        protected var numRasters:int = 0;
        protected var p:Point = new Point();
        protected var whiteFill:uint = BitmapCacheMap.WHITE;
        protected var whiteMask:uint = BitmapCacheMap.MASK_ARGB;
        
        protected function rasterize(event:Event=null, resizing:Boolean=false):void
        {
            // trace('** rasterize');
            // first, grab the bitmap of the display map
            var bmp:BitmapData = rasterized.bitmapData = _displayMap.cache.clone();
            
            bmp.copyChannel(_maskMap.cache, bmp.rect, p, BitmapDataChannel.ALPHA, BitmapDataChannel.ALPHA);
            
            // then clone it; this is what we're going to mask with the threshold operation 
            var result:BitmapData = bmp.clone();

            // apply the maskedFilter to the display map, turning it into the darker version 
            if (maskedFilter) bmp.applyFilter(bmp, bmp.rect, p, maskedFilter);
            
            // then create a pure white bitmap. this is used to create a new alpha channel
            var white:BitmapData = new BitmapData(bmp.width, bmp.height, true, BitmapCacheMap.BLACK);

            // then threshold the result bitmap using the mask as the source
            if (minThreshold > 0)
            {
                // trace('minThreshold:', minThreshold);
                white.threshold(_maskMap.cache, bmp.rect, p, '<=', minThreshold, whiteFill, BitmapCacheMap.MASK_RGB, false);
            }

            var t:int = getTimer();
            var boundColor:uint = whiteFill & whiteMask;
            var rect:Rectangle = resizing
                                 ? null
                                 : white.getColorBoundsRect(whiteMask, boundColor, true);
            if ((rect && rect.width > 0 && rect.height > 0)
                || white.getPixel(0, 0) == (whiteFill & BitmapCacheMap.MASK_RGB))
            {
                // then, apply the blue channel of the white bitmap as the alpha channel of the result
                result.copyChannel(white, white.rect, p, BitmapDataChannel.BLUE, BitmapDataChannel.ALPHA);
                
                // finally, draw the result (the masked display map) onto the darker version
                bmp.draw(result);

                if (outlineFilter)
                {
                    if (rect) rect.inflate(1, 1);

                    white.copyChannel(white, white.rect, p, BitmapDataChannel.BLUE, BitmapDataChannel.ALPHA);

                    var m:Matrix = new Matrix();
                    if (rect) m.translate(rect.x, rect.y);
                    if (outlineColorTransform) white.colorTransform(white.rect, outlineColorTransform);
                    white.applyFilter(white, rect || white.rect, p, outlineFilter);
                    bmp.draw(white, m, null, outlineBlendMode);
                }
            }
            trace('[took', getTimer() - t, 'ms]');

            white.dispose();
            result.dispose();
            
            dirty = false;
        }
        
        protected function onMapRendered(event:Event):void
        {
            if (event.type == ProgressEvent.PROGRESS)
            {
                var pEvent:ProgressEvent = (event as ProgressEvent);
                // trace('* loaded', pEvent.bytesLoaded, 'of', pEvent.bytesTotal, 'tiles for', event.target.parent.name);
            }
            dirty = true;
        }
        
        protected function onDisplayMapRendered(event:Event):void
        {
            _maskMap.grid.setMatrix(_displayMap.grid.getMatrix());
            dirty = true;
        }

        override protected function resize():void
        {
            super.resize();
            
            _displayMap.setSize(width, height);
            _maskMap.setSize(width, height);
            
            rasterize(null, true);
        }
    }
}