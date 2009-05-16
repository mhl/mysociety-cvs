package org.mysociety
{
    import com.modestmaps.Map;
    import com.modestmaps.core.MapExtent;
    import com.modestmaps.events.MapEvent;
    import com.modestmaps.extras.MapControls;
    import com.modestmaps.geo.Location;
    import com.modestmaps.mapproviders.CloudMadeProvider;
    import com.modestmaps.mapproviders.IMapProvider;
    import com.stamen.graphics.color.RGB;
    import com.stamen.ui.BlockSprite;
    import com.stamen.ui.tooltip.Tooltip;
    import com.stamen.utils.MathUtils;
    import com.stamen.utils.NumberFormatter;
    import com.stamen.utils.StringUtils;
    
    import flash.display.Bitmap;
    import flash.display.BitmapData;
    import flash.display.Graphics;
    import flash.display.Sprite;
    import flash.display.StageAlign;
    import flash.display.StageScaleMode;
    import flash.events.Event;
    import flash.events.KeyboardEvent;
    import flash.events.MouseEvent;
    import flash.events.TimerEvent;
    import flash.filters.DropShadowFilter;
    import flash.filters.GlowFilter;
    import flash.geom.Matrix;
    import flash.geom.Point;
    import flash.geom.Rectangle;
    import flash.text.TextField;
    import flash.utils.Timer;
    
    import org.mysociety.display.BitmapThresholdMap;
    import org.mysociety.display.MapLoadingIndicator;
    import org.mysociety.display.ui.SliderPanel;
    import org.mysociety.map.C4MapButton;
    import org.mysociety.map.MapInfoBubble;
    import org.mysociety.map.providers.ThresholdMaskProvider;
    import org.mysociety.style.StyleGuide;
    import org.mysociety.utils.DateUtils;

    [SWF(frameRate="24")]
    public class UKTravelTimeApp extends BlockSprite
    {
        public static const ARRIVE:String = 'arrive';
        public static const DEPART:String = 'depart';
        
        // tooltip strings
        protected var timeSliderArriveTooltip:String = "Setting the travel time slider to a certain time highlights everywhere on the map\n" + 
                                                       "that you could leave at that time, in order to get to your chosen destination by {T},\n" + 
                                                       "via the quickest possible combination of public transport."
        protected var timeSliderDepartTooltip:String = "Setting the travel time slider to a certain time highlights everywhere on the map\n" + 
                                                       "that you could get to at that time, given departure from your chosen origin at {T},\n" + 
                                                       "via the quickest possible combination of public transport.";
        protected var priceSliderTooltip:String = "Setting the house prices slider highlights everywhere on the map where the average mean\n" + 
                                                  "price of homes sold from January 2008 to March 2009 was less than the price you've chosen.";
        protected var scenicSliderTooltip:String = "Setting the scenicness slider highlights everywhere on the map that players of\n" + 
                                                   "the game ScenicOrNot (http://scenic.mysociety.org) rated as equally or more pretty\n" + 
                                                   "than the score you've chosen (score is out of 10).";
                                                   
        protected var originName:String;
        protected var originPrefix:String;
        
        // min/max/initial value minutes for the time slider
        protected var showMinMinutes:uint = 0;
        protected var showMaxMinutes:uint = 60 * 12;
        protected var initialMinutes:uint = 0;
        // minutes after midnight that represents the *max* of the time slider
        protected var baseTimeInMinutes:uint = 60 * 17;
        // maximum number of travel minutes before we show the "inaccessible" text in the tooltip
        protected var maxTravelMinutes:uint = 24 * 60;
        protected var arriveOrDepart:String = ARRIVE;

        // min/max/initial value for the price slider
        protected var showMinPrice:uint = 1000;
        protected var showMaxPrice:uint = 1000000;
        protected var initialPrice:uint = 150000;
        protected var freeString:String = '£0';

        // min/max/initial value for the scenicness slider        
        protected var showMinScenicScore:uint = 1;
        protected var showMaxScenicScore:uint = 10;
        protected var initialScenicScore:uint = 5;
        // scenicness score multiplier: what to divide the slider value by to get a displayable score
        protected var scenicMultiplier:uint = 10;
        
        // time tile URL parameters
        protected var enableTime:Boolean = true;
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
        
        protected var map:Map;

        // initial map state parameters
        protected var initialMapExtent:MapExtent; // = new MapExtent(59.57885104663186, 49.724479188712984, 2.98828125, -11.07421875);
        protected var initialMapLocation:Location = new Location(51.759865102943905, -1.2658309936523438);
        protected var initialMapZoom:int = 11;
        protected var markerLocation:Location;
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
        
        protected var mapBubble:MapInfoBubble;
        protected var bubbleText:String = 'This exact location is <a class="time">{T}</a> by public transport {O}<a class="location">{L}</a>. ' + 
                                          'The house prices here average <a class="price">{P}</a> and the scenicness rating is <a class="scenic">{S}</a> out of 10.';
        protected var bubbleTimer:Timer;
        
        protected var tooltip:Tooltip;
        
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

            bubbleTimer = new Timer(750);
            bubbleTimer.addEventListener(TimerEvent.TIMER, showMapBubble);
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
                case 'origin_name':
                    originName = value;
                    return true;
                case 'origin_prefix':
                    originPrefix = value;
                    return true;

                case 'cloudmade_api_key':
                    cloudmadeAPIKey = value;
                    return true;

                case 'iso_enabled':
                    enableTime = (value == 'true');
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
                    baseTimeInMinutes = parseInt(value);
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
                case 'depart_or_arrive':
                    arriveOrDepart = value;
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
                case 'free_string':
                    freeString = value;
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
            
            map = new Map(100, 100, true, mapProvider);
            map.addEventListener(MouseEvent.DOUBLE_CLICK, map.onDoubleClick);
            map.addEventListener(MouseEvent.MOUSE_MOVE, resetMapBubble);
            map.addEventListener(MouseEvent.MOUSE_OUT, disableMapBubble);
            map.addEventListener(MapEvent.RENDERED, onMapRendered);
            map.addEventListener(MapEvent.BEGIN_TILE_LOADING, onMapBeginTileLoad);
            map.addEventListener(MapEvent.ALL_TILES_LOADED, onMapFinishTileLoad);
            addChild(map);

            thresholdContainer = new Sprite();
            thresholdContainer.mouseEnabled = thresholdContainer.mouseChildren = false;
            thresholdContainer.visible = false;
            addChild(thresholdContainer);

            displayBitmap = new Bitmap();
            displayBitmap.alpha = .65;
            addChild(displayBitmap);

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
            addChild(controls);

            if (enableTime)
            {
                timeMap = createThresholdMap(timeTileURLTemplate, timeTileURLSubdomains);
                timeMap.name = 'time';
                thresholdContainer.addChild(timeMap);
            }

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
            // topPanel.visible = false;
            addChild(topPanel);
            
            var timeSliderTooltip:String;
            var timeSliderFlip:Boolean = false;
            var timePanelTitle:String;
            var timeSliderDate:Date = DateUtils.dateFromMinutesAfterMidnight(baseTimeInMinutes);
            switch (arriveOrDepart)
            {
                case ARRIVE:
                    timePanelTitle = 'Public transport arriving at ' + formatTime(timeSliderDate);
                    timeSliderFlip = true;
                    timeSliderTooltip = timeSliderArriveTooltip;
                    break;
                case DEPART:
                default:
                    timePanelTitle = 'Public transport departing at ' + formatTime(timeSliderDate); 
                    timeSliderTooltip = timeSliderDepartTooltip;
                    break;
            }
            timePanel = new SliderPanel(timePanelTitle, showMinMinutes, showMaxMinutes, initialMinutes, 100);
            timePanel.slider.tooltipText = timeSliderTooltip.replace('{T}', formatTime(timeSliderDate));
            timePanel.slider.flipFill = timeSliderFlip;
            timePanel.slider.updateTicks(15, 60);
            timePanel.slider.addEventListener(Event.CHANGE, onTimeChange);
            topPanel.addChild(timePanel);
            onTimeChange(null);
            timePanel.enabled = enableTime;
            
            pricePanel = new SliderPanel('House price (average)', showMinPrice, showMaxPrice, initialPrice, 100);
            pricePanel.slider.tooltipText = priceSliderTooltip;
            pricePanel.slider.updateTicks(20000, 100000);
            pricePanel.slider.addEventListener(Event.CHANGE, onPriceChange);
            topPanel.addChild(pricePanel);
            onPriceChange(null);
            
            scenicPanel = new SliderPanel('Scenicness', showMinScenicScore, showMaxScenicScore, initialScenicScore, 100);
            scenicPanel.slider.tooltipText = scenicSliderTooltip;
            scenicPanel.slider.updateTicks(1);
            scenicPanel.slider.flipFill = true;
            scenicPanel.slider.addEventListener(Event.CHANGE, onScenicChange);
            topPanel.addChild(scenicPanel);
            onScenicChange(null);
            
            loadingIndicator = new MapLoadingIndicator();
            
            mapBubble = new MapInfoBubble();
            mapBubble.filters = [new DropShadowFilter(.5, 45, 0x000000, .25, 2, 2, 2)];
            mapBubble.field.htmlText = 'This is a <b>test of bold text</b>. We should have all of the characters to display <b>£123,456,789</b>';
            trace('text:', mapBubble.field.htmlText);
            mapBubble.visible = false;
            addChild(mapBubble);
            
            tooltip = new Tooltip();
            tooltip.bgColor = 0x000000;
            tooltip.setTextFormat(StyleGuide.getTextFormat(13, RGB.white()), true);
            stage.addChild(tooltip);
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
            updateMapBubble();
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
            trace('rasterizing!');
            if (!displayBitmap.bitmapData)
            {
                displayBitmap.bitmapData = new BitmapData(map.getWidth(), map.getHeight(), true, 0x00000000);
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
            dirty = false;
        }

        protected function onTimeChange(event:Event):void
        {
            var minutes:uint = timePanel.slider.value;
            var field:TextField = timePanel.label;
            var date:Date;
            switch (arriveOrDepart)
            {
                case ARRIVE:
                    minutes = (timePanel.slider.max - minutes);
                    if (timeMap)
                    {
                        timeMap.maxThreshold = minutes * 60;
                    }
                    date = DateUtils.dateFromMinutesAfterMidnight(baseTimeInMinutes - minutes);
                    field.text = 'Departing at ' + formatTime(date);
                    break;
                case DEPART:
                default:
                    if (timeMap)
                    {
                        timeMap.maxThreshold = minutes * 60;
                    }
                    date = DateUtils.dateFromMinutesAfterMidnight(baseTimeInMinutes + minutes);
                    field.text = 'Arriving by ' + formatTime(date);
                    break;
            }
            dirty = true;
        }
        
        protected function onPriceChange(event:Event):void
        {
            if (pricePanel.slider.value == pricePanel.slider.max)
            {
                priceMap.maxThreshold = 0xFFFFFF;
                pricePanel.label.text = 'Any price';
            }
            else
            {
                var price:uint = MathUtils.quantize(pricePanel.slider.value, 1000);
                pricePanel.label.text = formatPrice(price) + ((price > 0) ? ' or less' : '');
                priceMap.maxThreshold = price;
            }
            dirty = true;
        }
        
        protected function onScenicChange(event:Event):void
        {
            var value:Number = scenicPanel.slider.value;
            scenicPanel.label.text = 'Score: ' + formatScenicness(value);
            value *= scenicMultiplier;
            if (scenicMap) scenicMap.minThreshold = new RGB(value, value, value).hex;
            dirty = true;
        }
        
        protected function formatTime(date:Date):String
        {
            return date.hours + ':' + NumberFormatter.zerofill(date.minutes, 2);
        }
        
        protected function formatTravelTime(minutes:uint):String
        {
            return (minutes <= maxTravelMinutes)
                   ? DateUtils.relativeTimeString(minutes)
                   : 'over ' + (maxTravelMinutes / 60) + ' hours'
        }
        
        protected function formatPrice(price:uint):String
        {
            price = MathUtils.quantize(price, 1000, Math.ceil);
            return (price > 0)
                   ? '£' + NumberFormatter.thousands(price)
                   : freeString;
        }
        
        protected function formatScenicness(score:Number):String
        {
            return (score % 1 == 0)
                   ? score.toString()
                   : score.toFixed(1);
        }
        
        protected function resetMapBubble(event:Event=null):void
        {
            mapBubble.visible = false;
            bubbleTimer.reset();
            bubbleTimer.start();
        }
        
        protected function disableMapBubble(event:Event=null):void
        {
            mapBubble.visible = false;
            bubbleTimer.stop();
        }
        
        protected function showMapBubble(event:TimerEvent):void
        {
            bubbleTimer.reset();
            mapBubble.x = Math.round(mouseX);
            mapBubble.y = Math.floor(mouseY - 2);
            mapBubble.visible = true;
            
            updateMapBubble();
        }
        
        protected function updateMapBubble():void
        {
            var minutes:uint = timeMap.cache.getPixel(map.mouseX, map.mouseY) / 60;
            var timeText:String = timeMap
                ? formatTravelTime(minutes)
                : '?';
            var priceText:String = priceMap
                ? formatPrice(priceMap.cache.getPixel(map.mouseX, map.mouseY))
                : '?';
            var scenicText:String = scenicMap
                ? formatScenicness((scenicMap.cache.getPixel(map.mouseX, map.mouseY) & 0x0000FF) / scenicMultiplier)
                : '?';
            var originPrefixText:String = originPrefix ? originPrefix + ', ' : '';
            mapBubble.field.htmlText = StringUtils.replace(bubbleText,
                                                           {'{T}': timeText,
                                                            '{P}': priceText,
                                                            '{S}': scenicText,
                                                            '{O}': originPrefixText,
                                                            '{L}': originName});
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
                controlRect.bottom = topPanel.y + topPanel.height;
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
