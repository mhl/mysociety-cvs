package com.stamen.ui
{
	import com.stamen.display.ColorSprite;
	import com.stamen.graphics.color.*;
	
	import flash.display.BitmapData;
	import flash.display.Graphics;
	import flash.geom.Rectangle;

	public class BlockSprite extends ColorSprite
	{
		public var bitmap:BitmapData;
		
		protected var _width:Number;
		protected var _height:Number;
		
		public function BlockSprite(w:Number=0, h:Number=0, color:IColor=null)
		{
			super(color);
			_width = w;
			_height = h;
			resize();
		}
		
		public function setSize(w:Number, h:Number):Boolean
		{
			if (w != _width || h != _height)
			{
				_width = w;
				_height = h;
				resize();
				return true;
			}
			return false;
		}
		
		public function setRect(rect:Rectangle):void
		{
		    x = rect.x;
		    y = rect.y;
		    setSize(rect.width, rect.height);
		}
		
		protected function resize():void
		{
			draw();
		}

		override public function get width():Number
		{
			return isNaN(_width) ? super.width : _width;
		}
		
		override public function get height():Number
		{
			return isNaN(_height) ? super.height : _height;
		}
		
		override public function set width(value:Number):void
		{
			setSize(value, _height);
		}
		
		override public function set height(value:Number):void
		{
			setSize(_width, value);
		}
		
		public function get actualWidth():Number
		{
			return super.width;
		}
		
		public function get actualHeight():Number
		{
			return super.height;
		}

        override protected function updateColor():void
        {
            draw();
        }
        
		protected function draw(color:IColor=null):void
		{
			if (!color) color = _color;
			
			var g:Graphics = graphics;
			g.clear();
				
			if (color || bitmap)
			{
			    if (bitmap)
			    {
			        g.beginBitmapFill(bitmap);
			    }
			    else
			    {
                    g.beginFill(color.hex, color.alpha);
			    }
			}
		    drawShape(g);
		    
			g.endFill();
			g.lineStyle();
		}
		
		protected function drawShape(g:Graphics=null):void
		{
		    if (!g) g = graphics;
            g.drawRect(0, 0, width, height);
		}
	}
}