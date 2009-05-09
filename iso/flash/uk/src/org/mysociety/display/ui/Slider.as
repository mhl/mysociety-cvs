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
        public var track:Sprite;
        public var thumb:Sprite;
        public var dragRect:Rectangle;
        
        protected var _value:Number = 0;
        protected var _min:Number = 0;
        protected var _max:Number = 1;
        protected var trackColor:IColor;
        
        protected var _fillColor:IColor;
        protected var _flipFill:Boolean = false;
        protected var filler:Shape;
        
        protected var ticks:Shape;
        protected var inset:Number;
        
        public function Slider(min:Number=0, max:Number=1, value:Number=0, w:Number=120)
        {
            _min = min;
            _max = max;
            _value = value;
            
            _fillColor = StyleGuide.darkBlue;
            trackColor = RGB.grey(0x99);

            ticks = new Shape();
            addChild(ticks);
            
            track = new Sprite();
            track.buttonMode = true;
            track.addEventListener(MouseEvent.MOUSE_DOWN, onThumbDown);
            track.addEventListener(MouseEvent.CLICK, onTrackClick);
            addChild(track);

            filler = new Shape();
            addChild(filler);            

            thumb = new Sprite();
            var grabber:Shape = new Shape();
            grabber.name = 'grabber';
            var g:Graphics = grabber.graphics;
            g.beginFill(StyleGuide.turquoise.hex);
            // g.lineStyle(1.5, 0x000000, .6);
            var size:Number = 18;
            g.drawRoundRect(0, 0, size, size, 4, 4);
            g.endFill();
            g.lineStyle(1, 0xFFFFFF, 1, true, LineScaleMode.NONE, CapsStyle.SQUARE);
            for each (var sx:Number in [6, 9, 12])
            {
                g.moveTo(sx, 5);
                g.lineTo(sx, 12);
            }
            grabber.x = grabber.y = -size / 2;
            // grabber.filters = [new GlowFilter(trackColor.hex, 1, 3, 3, 3, BitmapFilterQuality.MEDIUM)];
            thumb.addChild(grabber);
            thumb.buttonMode = true;
            thumb.mouseChildren = false;
            thumb.addEventListener(MouseEvent.MOUSE_DOWN, onThumbDown);
            addChild(thumb);
            
            super(w, 0);
        }
        
        public function get flipFill():Boolean
        {
            return _flipFill;
        }
        
        public function set flipFill(value:Boolean):void
        {
            if (flipFill != value)
            {
                _flipFill = value;
                updateFill();
            }
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
                updateFill();
                dispatchEvent(new Event(Event.CHANGE));
            }
            if (event is MouseEvent) (event as MouseEvent).updateAfterEvent();
        }
        
        protected function updateFill():void
        {
            var rect:Rectangle = thumb.getChildByName('grabber').getRect(this);
            var g:Graphics = filler.graphics;
            g.clear();

            var fillRect:Rectangle = rect.clone();
            if (flipFill)
            {
                fillRect.right = dragRect.right + 6;
                fillRect.left = rect.right;
            }
            else
            {
                fillRect.left = dragRect.left - 4;
                fillRect.right = rect.left;
            }
            if (fillRect.width > 0)
            {
                fillRect.inflate(0, -5);
                fillRect.y += 4;
                
                // g.lineStyle(0, 0x000000, 1, true, LineScaleMode.NONE, CapsStyle.NONE, JointStyle.MITER);
                g.beginFill(_fillColor.hex, _fillColor.alpha);
                var r:Number = 3.5;
                if (flipFill)
                {
                    g.drawRoundRectComplex(fillRect.x, fillRect.y, fillRect.width, fillRect.height, 0, r, 0, r);
                }
                else
                {
                    g.drawRoundRectComplex(fillRect.x, fillRect.y, fillRect.width, fillRect.height, r, 0, r, 0);
                }   
                g.endFill();
                g.lineStyle();
            }

            filler.y = -filler.height / 2;
        }
        
        public function updateTicks(tickStep:Number, markHigh:Number=0, color:uint=0x999999):void
        {
            ticks.scaleX = ticks.scaleY = 1;
            
            var steps:int = (max - min) / tickStep;
            var len:Number = dragRect.width;
            var step:Number = len / (steps - 1);
            var tx:Number = 0;
            var g:Graphics = ticks.graphics;
            g.clear();
            g.beginFill(0xFFFFFF, 0);
            g.drawRect(0, 0, len, 6);
            g.endFill();
            g.lineStyle(1, color, 1, true, LineScaleMode.NONE, CapsStyle.SQUARE);
            for (var i:Number = min; i <= max; i += tickStep)
            {
                var h:Number = 4;
                if (markHigh > 0 && (i % markHigh == 0)) h = 6;
                trace('tick @', i, 'x:', tx, 'h:', h);
                g.moveTo(tx, 0);
                g.lineTo(tx, h);
                tx += step;
            }
            updateTicksPosition();
        }
        
        protected function stopDragging(event:Event=null):void
        {
            thumb.stopDrag();
            update(event);
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
            thumb.x = Math.round(MathUtils.map(val, min, max, dragRect.left, dragRect.right));
            updateFill();
        }
        
        protected function updateTicksPosition():void
        {
            ticks.y = 7;
            ticks.x = dragRect.x;
            ticks.width = dragRect.width;
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
            updateTicksPosition();
        }
    }
}