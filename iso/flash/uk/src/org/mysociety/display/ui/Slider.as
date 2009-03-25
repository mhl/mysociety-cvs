package org.mysociety.display.ui
{
    import com.stamen.graphics.color.IColor;
    import com.stamen.graphics.color.RGB;
    import com.stamen.ui.BlockSprite;
    import com.stamen.utils.MathUtils;
    
    import flash.display.CapsStyle;
    import flash.display.Graphics;
    import flash.display.LineScaleMode;
    import flash.display.Shape;
    import flash.display.Sprite;
    import flash.events.Event;
    import flash.events.MouseEvent;
    import flash.geom.Rectangle;
    
    import org.mysociety.style.StyleGuide;

    public class Slider extends BlockSprite
    {
        public var trackTweenDuration:Number = 0;
        
        public var track:Sprite;
        public var thumb:Sprite;
        public var dragRect:Rectangle;
        
        protected var _value:Number = 0;
        protected var _min:Number = 0;
        protected var _max:Number = 1;
        protected var trackColor:IColor;
        
        protected var inset:Number;
        
        public function Slider(min:Number=0, max:Number=1, value:Number=0, w:Number=120, h:Number=0, color:IColor=null)
        {
            _min = min;
            _max = max;
            _value = value;

            track = new Sprite();
            track.buttonMode = true;
            track.addEventListener(MouseEvent.MOUSE_DOWN, onThumbDown);
            track.addEventListener(MouseEvent.CLICK, onTrackClick);
            addChild(track);
            
            trackColor = RGB.grey(0x99);

            thumb = new Sprite();
            var grabber:Shape = new Shape();
            var g:Graphics = grabber.graphics;
            g.beginFill(StyleGuide.liteGreen.hex);
            // g.lineStyle(1.5, 0x000000, .6);
            var size:Number = 18;
            g.drawRoundRect(0, 0, size, size, 4, 4);
            g.endFill();
            g.lineStyle(1, 0x000000, 1, true, LineScaleMode.NONE, CapsStyle.NONE);
            for each (var sx:Number in [6, 9, 12])
            {
                g.moveTo(sx, 4);
                g.lineTo(sx, 13);
            }
            grabber.x = grabber.y = -size / 2;
            // grabber.filters = [new GlowFilter(trackColor.hex, 1, 3, 3, 3, BitmapFilterQuality.MEDIUM)];
            thumb.addChild(grabber);
            thumb.buttonMode = true;
            thumb.mouseChildren = false;
            thumb.addEventListener(MouseEvent.MOUSE_DOWN, onThumbDown);
            addChild(thumb);
            
            super(w, h, color);
        }
        
        protected function onTrackClick(event:MouseEvent):void
        {
            thumb.x = MathUtils.bound(mouseX, dragRect.left, dragRect.right);
            update(event);
        }
        
        protected function onThumbDown(event:MouseEvent):void
        {
            thumb.startDrag(true, dragRect);
            stage.addEventListener(MouseEvent.MOUSE_MOVE, update);
            stage.addEventListener(MouseEvent.MOUSE_UP, stopDragging);
            stage.addEventListener(Event.MOUSE_LEAVE, stopDragging);
        }
        
        protected function update(event:Event=null):void
        {
            var old:Number = value;
            var changed:Number = MathUtils.map(thumb.x, dragRect.left, dragRect.right, min, max);
            if (changed != old)
            {
                _value = changed;
                dispatchEvent(new Event(Event.CHANGE));
            }
            if (event is MouseEvent) (event as MouseEvent).updateAfterEvent();
        }
        
        protected function stopDragging(event:Event=null):void
        {
            thumb.stopDrag();
            stage.removeEventListener(MouseEvent.MOUSE_MOVE, update);
            stage.removeEventListener(MouseEvent.MOUSE_UP, stopDragging);
            stage.removeEventListener(Event.MOUSE_LEAVE, stopDragging);
        }
        
        public function get min():Number
        {
            return _min;
        }
        
        public function get max():Number
        {
            return _max;
        }
        
        public function get value():Number
        {
            return _value;
        }
        
        public function set value(val:Number):void
        {
            if (value != val)
            {
                _value = MathUtils.bound(val, Math.min(min, max), Math.max(min, max));
                updateThumbPosition();
                dispatchEvent(new Event(Event.CHANGE));
            }
        }
        
        protected function updateThumbPosition():void
        {
            var val:Number = MathUtils.bound(value, Math.min(min, max), Math.max(min, max));
            thumb.x = MathUtils.map(val, min, max, dragRect.left, dragRect.right);
        }
        
        override protected function resize():void
        {
            super.resize();

            var g:Graphics = track.graphics;
            g.clear();
            g.beginFill(0xFFFFFF, 0);
            g.drawRect(-2, -6, width + 4, 18);
            g.endFill();
            
            g.lineStyle(5, trackColor.hex, 1, true, LineScaleMode.NONE, CapsStyle.ROUND);
            g.moveTo(0, 0);
            g.lineTo(width, 0);
            //g.lineStyle(0, 0xFFFFFF);
            //g.lineTo(0, 0);

            dragRect = new Rectangle(0, 0, width, 0);
            dragRect.inflate(-2, 0);
            updateThumbPosition();
        }
    }
}