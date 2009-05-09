package org.mysociety
{
    import com.modestmaps.core.MapExtent;
    import com.modestmaps.events.MapEvent;
    import com.modestmaps.extras.MapControls;
    import com.modestmaps.geo.Location;
    import com.modestmaps.mapproviders.CloudMadeProvider;
    import com.modestmaps.mapproviders.IMapProvider;
    import com.stamen.graphics.color.RGB;
    import com.stamen.ui.BlockSprite;
    import com.stamen.utils.MathUtils;
    import com.stamen.utils.NumberFormatter;
    
    import flash.display.Bitmap;
    import flash.display.BitmapData;
    import flash.display.Graphics;
    import flash.display.Sprite;
    import flash.display.StageAlign;
    import flash.display.StageScaleMode;
    import flash.events.Event;
    import flash.events.KeyboardEvent;
    import flash.events.MouseEvent;
    import flash.filters.DropShadowFilter;
    import flash.filters.GlowFilter;
    import flash.geom.Matrix;
    import flash.geom.Point;
    import flash.geom.Rectangle;
    import flash.text.TextField;
    
    import org.mysociety.display.BitmapCacheMap;
    import org.mysociety.display.BitmapThresholdMap;
    import org.mysociety.display.MapLoadingIndicator;
    import org.mysociety.display.ui.SliderPanel;
    import org.mysociety.map.C4MapButton;
    import org.mysociety.map.providers.ThresholdMaskProvider;
    import org.mysociety.style.StyleGuide;
    import org.mysociety.utils.DateUtils;

    [SWF(frameRate="24")]
    public class UKTravelTimeApp extends BlockSprite
    {
        public var map:BitmapCacheMap;
        
        // These are PIXEL VALUES!
        protected var minMinutes:uint = 0;
        protected var maxMinutes:uint = 0xFFFFFF;
        protected var minPrice:uint = 0;
        protected var maxPrice:uint = 0xFFFFFF;

        // min/max/initial value minutes for the time slider
        protected var showMinMinutes:uint = 1;
        protected var showMaxMinutes:uint = 60 * 12;
        protected var initialMinutes:uint = 0;

        // min/max/initial value for the price slider
        protected var showMinPrice:uint = 1;
        protected var showMaxPrice:uint = 1000000;
        protected var initialPrice:uint = 150000;

        // min/max/initial value for the scenicness slider        
        protected var showMinScenicScore:uint = 1;
        protected var showMaxScenicScore:uint = 10;
        protected var initialScenicScore:uint = 5;
        // scenicness score multiplier: what to divide the slider value by to get a displayable score
        protected var scenicMultiplier:uint = 10;
        
        // minutes after midnight that represents the *max* of the time slider
        protected var minutesAfterMidnight:uint = 60 * 17;

        // time tile URL parameters
        protected var timeTileURLTemplate:String;
        protected var timeTileURLSubdomains:Array;

        // price tile URL parameters
        protected var priceTileURLTemplate:String;
        protected var priceTileURLSubdomains:Array;
        
        // scenicness tile URL parameters
        protected var scenicTileURLTemplate:String;
        protected var scenicTileURLSubdomains:Array;
        
        // initial map provider; filled in according to flashvars
        // NOTE: this defaults to a CloudMadeProvider with an API key and style ID from the parameters below
        protected var mapProvider:IMapProvider;

        // Cloudmade API key        
        protected var cloudmadeAPIKey:String;
        // Cloudmade style ID
        protected var cloudmadeStyle:String = CloudMadeProvider.FRESH;
        
        protected var markerLocation:Location;
        
        // initial map state parameters
        protected var initialMapExtent:MapExtent; // = new MapExtent(59.57885104663186, 49.724479188712984, 2.98828125, -11.07421875);
        protected var initialMapLocation:Location = new Location(51.759865102943905, -1.2658309936523438);
        protected var initialMapZoom:int = 11;
        // map min/max zoom levels
        protected var minMapZoom:int = 6;
        protected var maxMapZoom:int = 12;

        protected var controls:MapControls;
        protected var topPanel:BlockSprite;
        
        protected var timePanel:SliderPanel;
        protected var timeMap:BitmapThresholdMap;
        protected var pricePanel:SliderPanel;
        protected var priceMap:BitmapThresholdMap;
        protected var scenicPanel:SliderPanel;
        protected var scenicMap:BitmapThresholdMap;
        protected var thresholdContainer:Sprite;
        
        protected var loadingIndicator:MapLoadingIndicator;
        protected var loadingProgressMaps:Array;
        
        protected var displayBitmap:Bitmap;
        
        public function UKTravelTimeApp()
        {
            if (stage)
            {
                var params:Object = root.loaderInfo.parameters;
                for (var param:String in params)
                {
                    applyParameter(param, params[param]);
                }
            }
            
            super();
            createChildren();
            
            if (stage)
            {
                stage.align = StageAlign.TOP_LEFT;
                stage.scaleMode = StageScaleMode.NO_SCALE;
                
                stage.addEventListener(Event.RESIZE, onStageResize);
                stage.addEventListener(KeyboardEvent.KEY_UP, onKeyUp);
                onStageResize(null);
            }
        }
        
        protected function onKeyUp(event:KeyboardEvent):void
        {
            /*
            switch (String.fromCharCode(event.charCode))
            {
                case 'O':
                    // map.outlineFilter = map.outlineFilter ? null : toggleGlowFilter;
                    break;
            }
            */
        }
        
        protected function applyParameter(name:String, value:String):Boolean
        {
            // ignore empty strings
            if (value.length == 0) return false;
            
            switch (name)
            {
                case 'cloudmade_api_key':
                    cloudmadeAPIKey = value;
                    return true;

                case 'iso_tile_url':
                    timeTileURLTemplate = value;
                    return true;
                case 'iso_tile_subdomains':
                    timeTileURLSubdomains = value.split(',');
                    return true;

                case 'price_tile_url':
                    priceTileURLTemplate = value;
                    return true;
                case 'price_tile_subdomains':
                    priceTileURLSubdomains = value.split(',');
                    return true;
                    
                case 'scenic_tile_url':
                    scenicTileURLTemplate = value;
                    return true;
                case 'scenic_tile_subdomains':
                    scenicTileURLSubdomains = value.split(',');
                    return true;

                case 'base_minutes':
                    minutesAfterMidnight = parseInt(value);
                    return true;
                case 'show_min_minutes':
                    showMinMinutes = parseInt(value);
                    return true;
                case 'show_max_minutes':
                    showMaxMinutes = parseInt(value);
                    return true;
                case 'initial_minutes':
                    initialMinutes = parseInt(value);
                    return true;

                case 'show_min_price':
                    showMinPrice = parseInt(value);
                    return true;
                case 'show_max_price':
                    showMaxPrice = parseInt(value);
                    return true;
                case 'initial_price':
                    initialPrice = parseInt(value);
                    return true;
                    
                case 'show_min_scenicness':
                    showMinScenicScore = parseInt(value);
                    return true;
                case 'show_max_scenicness':
                    showMaxScenicScore = parseInt(value);
                    return true;
                case 'initial_scenicness':
                    initialScenicScore = parseInt(value);
                    return true;
                case 'scenicness_multiplier':
                    scenicMultiplier = parseInt(value);
                    return true;
                          
                case 'marker_location':
                    markerLocation = Location.fromString(value);
                    return true;
                                  
                case 'map_extent':
                    initialMapExtent = MapExtent.fromString(value);
                    return true;
                case 'map_center':
                    initialMapLocation = Location.fromString(value);
                    return true;
                case 'map_zoom':
                    initialMapZoom = parseInt(value);
                    return true;
                case 'min_zoom':
                    minMapZoom = parseInt(value);
                    return true;
                case 'max_zoom':
                    maxMapZoom = parseInt(value);
                    return true;
                    
                case 'map_provider':
                    switch (value)
                    {
                        case 'midnight':
                            cloudmadeStyle = CloudMadeProvider.MIDNIGHT_COMMANDER;
                            return true;
                        case 'fresh':
                            cloudmadeStyle = CloudMadeProvider.FRESH;
                            return true;
                        case 'pale_dawn':
                            cloudmadeStyle = CloudMadeProvider.PALE_DAWN;
                            return true;
                    }
                    return false;
            }
            return false;    
        }
        
        protected function createChildren():void
        {
            if (!mapProvider)
            {
                mapProvider = new CloudMadeProvider(cloudmadeAPIKey, cloudmadeStyle);
            }
            
            map = new BitmapCacheMap(100, 100, true, mapProvider);
            map.addEventListener(MapEvent.RENDERED, onMapRendered);
            map.addEventListener(MapEvent.BEGIN_TILE_LOADING, onMapBeginTileLoad);
            map.addEventListener(MapEvent.ALL_TILES_LOADED, onMapFinishTileLoad);
            map.addEventListener(MouseEvent.DOUBLE_CLICK, map.onDoubleClick);
            var positions:Object = { 
                leftButton:     {left: '0px', top: '12px'},
                rightButton:    {left: '50px', top: '12px'},
                upButton:       {left: '25px', top: '0px'},
                downButton:     {left: '25px', top: '25px'},
                inButton:       {left: '25px', top: '53px'},
                outButton:      {left: '25px', top: '78px'}
            };
            controls = new MapControls(map, true, false, positions, C4MapButton);
            controls.filters = [new GlowFilter(0x000000, .6, 3, 3, 2)];
            addChild(map);

            thresholdContainer = new Sprite();
            thresholdContainer.mouseEnabled = thresholdContainer.mouseChildren = false;
            thresholdContainer.visible = false;
            addChild(thresholdContainer);

            displayBitmap = new Bitmap();
            displayBitmap.alpha = .65;
            addChild(displayBitmap);

            addChild(controls);

            timeMap = createThresholdMap(timeTileURLTemplate, timeTileURLSubdomains);
            timeMap.name = 'time';
            thresholdContainer.addChild(timeMap);

            priceMap = createThresholdMap(priceTileURLTemplate, priceTileURLSubdomains);
            priceMap.name = 'price';
            thresholdContainer.addChild(priceMap);
            scenicMap = createThresholdMap(scenicTileURLTemplate, scenicTileURLSubdomains);
            scenicMap.name = 'scenicness';
            var maxScenicness:uint = showMaxScenicScore * scenicMultiplier;
            scenicMap.maxThreshold = new RGB(maxScenicness, maxScenicness, maxScenicness).hex;
            thresholdContainer.addChild(scenicMap);

            // make them all transparent            
            for (var i:int = 0; i < thresholdContainer.numChildren; i++)
            {
                thresholdContainer.getChildAt(i).alpha = 1 / thresholdContainer.numChildren;
            }
            
            if (initialMapExtent && false)
            {
                trace('* extent:', initialMapExtent, '(center:', initialMapExtent.center + ')');
                map.setExtent(initialMapExtent);
            }
            else if (initialMapLocation)
            {
                trace('* initial location:', initialMapLocation, 'zoom:', initialMapZoom);
                map.setCenterZoom(initialMapLocation, initialMapZoom);
            }
            
            if (markerLocation)
            {
                var marker:Sprite = new Sprite();
                var mg:Graphics = marker.graphics;
                mg.beginFill(0x000000, 1);
                mg.lineStyle(2, StyleGuide.orange.hex);
                mg.drawCircle(0, 0, 3);
                mg.endFill();
                mg.lineStyle();
                marker.filters = [new GlowFilter(0x000000, 1, 3, 3, 2)];
                map.markerClip.attachMarker(marker, markerLocation);
            }
            
            topPanel = new BlockSprite(width, 82, RGB.white());
            topPanel.filters = [new DropShadowFilter(0, 90, 0x000000, 1, 0, 2, 1)];
            addChild(topPanel);
            
            timePanel = new SliderPanel('Travel time', showMinMinutes, showMaxMinutes, initialMinutes, 100);
            timePanel.slider.updateTicks(15, 60);
            timePanel.slider.addEventListener(Event.CHANGE, onTimeChange);
            topPanel.addChild(timePanel);
            onTimeChange(null);
            
            pricePanel = new SliderPanel('Price', showMinPrice, showMaxPrice, initialPrice, 100);
            pricePanel.slider.updateTicks(25000, 100000);
            pricePanel.slider.addEventListener(Event.CHANGE, onPriceChange);
            topPanel.addChild(pricePanel);
            onPriceChange(null);
            
            scenicPanel = new SliderPanel('Scenicness', showMinScenicScore, showMaxScenicScore, initialScenicScore, 100);
            scenicPanel.slider.updateTicks(1);
            scenicPanel.slider.flipFill = true;
            scenicPanel.slider.addEventListener(Event.CHANGE, onScenicChange);
            topPanel.addChild(scenicPanel);
            onScenicChange(null);
            
            loadingIndicator = new MapLoadingIndicator();
        }
        
        protected function createThresholdMap(baseTileURL:String, subdomains:Array=null):BitmapThresholdMap
        {
            var provider:ThresholdMaskProvider = new ThresholdMaskProvider(baseTileURL, subdomains);
            var thresholdMap:BitmapThresholdMap = new BitmapThresholdMap(100, 100, false, provider);
            thresholdMap.addEventListener(MapEvent.RENDERED, onThresholdMapRendered);
            thresholdMap.addEventListener(MapEvent.BEGIN_TILE_LOADING, onMapBeginTileLoad);
            thresholdMap.addEventListener(MapEvent.ALL_TILES_LOADED, onMapFinishTileLoad);
            return thresholdMap;
        }
        
        protected var mapsLoading:int = 0;
        protected function onMapBeginTileLoad(event:MapEvent):void
        {
            mapsLoading++;
            if (!contains(loadingIndicator))
            {
                addChild(loadingIndicator);
            }
        }
        
        protected function onMapFinishTileLoad(event:MapEvent):void
        {
            mapsLoading--;
            if (mapsLoading <= 0 && contains(loadingIndicator))
            {
                removeChild(loadingIndicator);
            }
        }
        
        protected function onThresholdMapRendered(event:MapEvent):void
        {
            dirty = true;
        }
        
        protected function onMapRendered(event:MapEvent):void
        {
            if (!thresholdContainer) return;
            
            var m:Matrix = map.grid.getMatrix();
            for (var i:int = 0; i < thresholdContainer.numChildren; i++)
            {
                (thresholdContainer.getChildAt(i) as BitmapThresholdMap).grid.setMatrix(m);
            }
            dirty = true;
        }

        protected var _dirty:Boolean = false;
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
        
        protected function rasterize(event:Event):void
        {
            if (!displayBitmap.bitmapData)
            {
                displayBitmap.bitmapData = new BitmapData(map.cache.width, map.cache.height, true, 0x00000000);
            }
            else
            {
                displayBitmap.bitmapData.fillRect(displayBitmap.bitmapData.rect, 0x00000000);
            }
            var shield:BitmapData = displayBitmap.bitmapData;
            var fillColor:uint = 0xFF000000 | StyleGuide.darkBlue.hex;
            for (var i:int = 0; i < thresholdContainer.numChildren; i++)
            {
                var thresholdMap:BitmapThresholdMap = thresholdContainer.getChildAt(i) as BitmapThresholdMap;
                shield.threshold(thresholdMap.maskBitmap, shield.rect, new Point(), '!=', 0xFFFFFF, fillColor, 0x00FFFFFF);
            }
        }

        protected function onTimeChange(event:Event):void
        {
            var minutes:uint = timePanel.slider.value;
            if (timeMap) timeMap.maxThreshold = minutes * 60;
            var field:TextField = timePanel.label;
            
            var date:Date = DateUtils.dateFromMinutesAfterMidnight(minutesAfterMidnight - (timePanel.slider.max - minutes));
            field.text = 'Leaving at '+ date.hours + ':' + NumberFormatter.zerofill(date.minutes, 2);
            /*
            if (minutes < 60)
            {
                field.text = minutes + StringUtils.pluralize(minutes, ' minute');
            }
            else
            {
                var hours:int = minutes / 60;
                minutes %= 60;
                field.text = hours + StringUtils.pluralize(hours, ' hour');
                if (minutes > 0)
                {
                    field.appendText(', ' + minutes + StringUtils.pluralize(minutes, ' minute'));
                }
            }
            */
            dirty = true;
        }
        
        protected function onPriceChange(event:Event):void
        {
            var price:uint = MathUtils.quantize(pricePanel.slider.value, 1000);
            pricePanel.label.text = 'Less than £' + NumberFormatter.thousands(price);
            priceMap.maxThreshold = price;
            dirty = true;
        }
        
        protected function onScenicChange(event:Event):void
        {
            var value:Number = scenicPanel.slider.value;
            scenicPanel.label.text = 'Score: ' + ((value % 1 == 0) ? value : value.toFixed(1));
            value *= scenicMultiplier;
            if (scenicMap) scenicMap.minThreshold = new RGB(value, value, value).hex;
            dirty = true;
        }
        
        protected function onStageResize(event:Event):void
        {
            setSize(stage.stageWidth, stage.stageHeight);
        }
        
        override protected function resize():void
        {
            super.resize();
            
            var rect:Rectangle = new Rectangle(0, 0, width, height);
            if (topPanel)
            {
                topPanel.width = rect.width;
                topPanel.x = rect.x;
                topPanel.y = 0;
                
                var controlRect:Rectangle = rect.clone();
                controlRect.inflate(-15, -10);
                controlRect.right -= 5;
                var right:Number = controlRect.right;
                controlRect.width = Math.floor(.45 * controlRect.width);
                timePanel.setRect(controlRect);
                var left:Number = controlRect.right;

                controlRect.width = scenicPanel.titleWidth - 5;
                controlRect.x = right - controlRect.width;
                scenicPanel.setRect(controlRect);

                var spacing:Number = 30;
                controlRect.right = controlRect.left - spacing;
                controlRect.left = left + spacing;
                pricePanel.setRect(controlRect);
                
                rect.top += topPanel.height;
            }
            if (map)
            {
                map.x = rect.x;
                map.y = rect.y;
                controls.x = map.x + 16;
                controls.y = map.y + 16;
                map.setSize(rect.width, rect.height);
                
                thresholdContainer.x = map.x;
                thresholdContainer.y = map.y;
                for (var i:int = 0; i < thresholdContainer.numChildren; i++)
                {
                    (thresholdContainer.getChildAt(i) as BitmapThresholdMap).setSize(map.getWidth(), map.getHeight());
                }
                
                displayBitmap.x = map.x;
                displayBitmap.y = map.y;
                
                displayBitmap.bitmapData = null;
            }
            if (loadingIndicator)
            {
                loadingIndicator.x = Math.floor((width - loadingIndicator.width) / 2);
                loadingIndicator.y = height - (loadingIndicator.height + 20);
            }
        }
    }
}
