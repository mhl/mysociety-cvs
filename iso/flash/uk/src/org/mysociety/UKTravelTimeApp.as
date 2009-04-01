package org.mysociety
{
    import com.bitstream.fonts.VeraSansBold;
    import com.modestmaps.core.MapExtent;
    import com.modestmaps.extras.MapControls;
    import com.modestmaps.geo.Location;
    import com.modestmaps.mapproviders.CloudMadeProvider;
    import com.quasimondo.geom.ColorMatrix;
    import com.stamen.graphics.color.RGB;
    import com.stamen.ui.BlockSprite;
    import com.stamen.utils.StringUtils;
    
    import flash.display.BlendMode;
    import flash.display.CapsStyle;
    import flash.display.Graphics;
    import flash.display.LineScaleMode;
    import flash.display.Shape;
    import flash.display.Sprite;
    import flash.display.StageAlign;
    import flash.display.StageScaleMode;
    import flash.events.Event;
    import flash.events.KeyboardEvent;
    import flash.filters.BitmapFilterQuality;
    import flash.filters.DropShadowFilter;
    import flash.filters.GlowFilter;
    import flash.geom.ColorTransform;
    import flash.geom.Rectangle;
    import flash.text.Font;
    import flash.text.FontType;
    import flash.text.TextField;
    import flash.text.TextFieldAutoSize;
    import flash.text.TextFormat;
    
    import org.mysociety.display.ThresholdMaskMap;
    import org.mysociety.display.ui.Slider;
    import org.mysociety.map.MySocietyMapButton;
    import org.mysociety.map.providers.ThresholdMaskProvider;
    import org.mysociety.style.StyleGuide;

    public class UKTravelTimeApp extends BlockSprite
    {
        public static var font:Font = new VeraSansBold();
        
        public var map:ThresholdMaskMap;
        
        protected var minThreshold:uint = 0;
        protected var maxThreshold:uint = 0xFFFFFF;
        protected var minMinutes:uint = 0;
        protected var maxMinutes:uint = 0xFFFFFF;
        protected var showMinutes:uint = 360;
        protected var initialMinutes:uint = 0;
        
        protected var isoTileBase:String;
        protected var isoTileFormat:String = '{Z}/{X}/{Y}.png';
        
        protected var cloudmadeAPIKey:String;
        
        protected var mapTileBase:String;
        protected var mapTileFormat:String;
        
        protected var markerLocation:Location;
        
        protected var initialMapExtent:MapExtent; // = new MapExtent(59.57885104663186, 49.724479188712984, 2.98828125, -11.07421875);
        protected var initialMapLocation:Location = new Location(51.759865102943905, -1.2658309936523438);
        protected var initialMapZoom:int = 11;

        protected var minMapZoom:int = 6;
        protected var maxMapZoom:int = 12;

        protected var toggleGlowFilter:GlowFilter = new GlowFilter(0x000000, .2, 3, 3, 2, BitmapFilterQuality.LOW);
        
        protected var timePanel:BlockSprite;
        protected var timeSlider:Slider;
        protected var timeField:TextField;
        protected var timeTicks:Shape;
        
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
            switch (String.fromCharCode(event.charCode))
            {
                case 'O':
                    map.outlineFilter = map.outlineFilter ? null : toggleGlowFilter;
                    break;
            }
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
                    
                case 'iso_tile_url_base':
                    isoTileBase = value;
                    return true;
                case 'iso_tile_url_format':
                    isoTileFormat = value;
                    return true;

                case 'min_threshold':
                    minThreshold = parseInt(value);
                    return true;
                case 'max_threshold':
                    maxThreshold = parseInt(value);
                    return true;

                case 'min_minutes':
                    minMinutes = parseInt(value);
                    return true;
                case 'max_minutes':
                    maxMinutes = parseInt(value);
                    return true;

                case 'show_minutes':
                    showMinutes = parseInt(value);
                    return true;
                case 'initial_minutes':
                    initialMinutes = parseInt(value);
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
            }
            return false;    
        }
        
        protected function createChildren():void
        {
            map = new ThresholdMaskMap(100, 100, true, new CloudMadeProvider(cloudmadeAPIKey, CloudMadeProvider.PALE_DAWN));

            var m:ColorMatrix = new ColorMatrix();
            // m.invert();
            m.adjustSaturation(0);
            m.adjustBrightness(-64);
            map.maskedFilter = m.filter;

            map.outlineColorTransform = null; new ColorTransform(-1, -1, -1, 1, 255, 255, 255, 0);
            map.outlineFilter = null; // toggleGlowFilter;
            map.outlineBlendMode = BlendMode.DARKEN;
            addChild(map);
            
            if (initialMapExtent && false)
            {
                trace('* extent:', initialMapExtent, '(center:', initialMapExtent.center + ')');
                map.displayMap.setExtent(initialMapExtent);
            }
            else if (initialMapLocation)
            {
                trace('* initial location:', initialMapLocation, 'zoom:', initialMapZoom);
                map.displayMap.setCenterZoom(initialMapLocation, initialMapZoom);
                
                if (!markerLocation) markerLocation = initialMapLocation.clone();
            }
            
            updateIsoTileURL();
            
            if (markerLocation)
            {
                var marker:Sprite = new Sprite();
                var mg:Graphics = marker.graphics;
                mg.beginFill(0x000000, 1);
                mg.lineStyle(2, StyleGuide.liteGreen.hex);
                mg.drawCircle(0, 0, 3);
                mg.endFill();
                mg.lineStyle();
                marker.filters = [new GlowFilter(0x000000, 1, 3, 3, 2)];
                map.markerClip.attachMarker(marker, markerLocation);
            }
            
            timePanel = new BlockSprite(width, 60, RGB.white());
            timePanel.filters = [new DropShadowFilter(0, 90, 0x000000, 1, 0, 2, 1)];
            addChild(timePanel);
            
            timeSlider = new Slider(minMinutes, showMinutes, initialMinutes, 100, 0);
            timeSlider.trackTweenDuration = 1.0;
            timeSlider.addEventListener(Event.CHANGE, onSliderChange);
            timePanel.addChild(timeSlider);
            
            timeField = new TextField();
            timeField.defaultTextFormat = new TextFormat(font ? font.fontName : '_sans', 14, 0x000000, true);
            timeField.embedFonts = font && font.fontType == FontType.EMBEDDED;
            timeField.width = 200;
            timeField.x = -timeField.width / 2;
            timeField.autoSize = TextFieldAutoSize.CENTER;
            timeField.y = 13;
            timeField.selectable = false;
            
            // comment this line out and all should be good
            timeSlider.thumb.addChild(timeField);
            
            var invisible:Object = {left: -1000, top: -1000};
            var positions:Object = {
                outButton: {left: 10, top: 10},
                inButton: {left: 60, top: 10},
                leftButton: invisible,
                rightButton: invisible,
                upButton: invisible,
                downButton: invisible
            };
            var controls:MapControls = new MapControls(map.displayMap, false, false, positions, MySocietyMapButton);
            controls.filters = [];
            addChild(controls);

            timeTicks = new Shape();
            var steps:uint = timeSlider.max - timeSlider.min;
            var len:Number = 1000;
            var step:Number = len / (steps - 1);
            var tx:Number = 0;
            var tick:int = 5;
            var g:Graphics = timeTicks.graphics;
            g.beginFill(0xFFFFFF);
            g.drawRect(0, 0, len, 6);
            g.endFill();
            g.lineStyle(1, 0x999999, 1, true, LineScaleMode.NONE, CapsStyle.SQUARE);
            for (var i:int = timeSlider.min; i <= timeSlider.max; i++)
            {
                if (i % tick == 0)
                {
                    var h:Number = 4;
                    if (i % 15 == 0) h = 6;
                    trace('tick @', i);
                    g.moveTo(tx, 0);
                    g.lineTo(tx, h);
                }
                tx += step;
            }
            timeTicks.y = 7;
            timeSlider.addChildAt(timeTicks, 0);
            
            onSliderChange(null);

        }
        
        protected function updateIsoTileURL():void
        {
            var isoTileBaseURL:String = isoTileBase + '/' + isoTileFormat;
            trace('* iso URL:', isoTileBaseURL);
            map.maskMap.setMapProvider(new ThresholdMaskProvider(isoTileBaseURL));
        }
        
        protected function onSliderChange(event:Event):void
        {
            var minutes:uint = timeSlider.value;
            map.minThreshold = minutes * 60;
            if (minutes < 60)
            {
                timeField.text = minutes + StringUtils.pluralize(minutes, ' minute');
            }
            else
            {
                var hours:int = minutes / 60;
                minutes %= 60;
                timeField.text = hours + StringUtils.pluralize(hours, ' hour');
                if (minutes > 0)
                {
                    timeField.appendText(', ' + minutes + StringUtils.pluralize(minutes, ' minute'));
                }
            }
            // trace('threshold:', map.minThreshold);
        }
        
        protected function onStageResize(event:Event):void
        {
            setSize(stage.stageWidth, stage.stageHeight);
        }
        
        override protected function resize():void
        {
            super.resize();
            
            var rect:Rectangle = new Rectangle(0, 0, width, height);
            if (timePanel)
            {
                timePanel.width = rect.width;
                timePanel.x = rect.x;
                timePanel.y = 0;
                
                var controlRect:Rectangle = rect.clone();
                controlRect.left += 100;
                controlRect.inflate(-20, -20);
                // squeeze the rect in to provide room on the sides for the label
                if (timeField && timeSlider.thumb.contains(timeField))
                {
                    controlRect.left += 30;
                    controlRect.right -= 80;
                    // controlRect.inflate(-80, 0);
                }
                timeSlider.width = controlRect.width;
                timeSlider.x = controlRect.x;
                timeSlider.y = controlRect.y;
                
                timeTicks.x = timeSlider.dragRect.x;
                timeTicks.width = timeSlider.dragRect.width;
                
                rect.top += timePanel.height;
            }
            if (map)
            {
                map.x = rect.x;
                map.y = rect.y;
                map.setSize(rect.width, rect.height);
            }
        }
    }
}
