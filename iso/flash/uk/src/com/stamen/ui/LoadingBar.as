package com.stamen.ui
{
	import com.stamen.graphics.color.IColor;
	import com.stamen.graphics.color.RGB;
	
	import flash.display.BitmapData;
	import flash.display.Shape;
	import flash.events.TimerEvent;
	import flash.geom.Matrix;
	import flash.geom.Rectangle;
	import flash.utils.Timer;
	
	import mx.core.BitmapAsset;

	public class LoadingBar extends BlockSprite
	{
	    [Embed(source="indeterminate.png")]
		public static const IndeterminatePattern:Class;

		public var progressFillColor:IColor;
		protected var outlineColor:IColor;
		
		protected var _progress:Number = 0;
		protected var _indeterminate:Boolean = false;

		protected var outline:Shape;
		protected var progressIndicator:Shape;

		protected var indShape:Shape;
		protected var indMatrix:Matrix;
		protected var indTimer:Timer;
		
		protected var pattern:BitmapData;

		public function LoadingBar(fillColor:IColor=null, outlineColor:IColor=null, bgColor:IColor=null)
		{
			progressFillColor = fillColor ? fillColor.clone() : RGB.black();
			if (outlineColor) this.outlineColor = outlineColor.clone();

			pattern = (new IndeterminatePattern() as BitmapAsset).bitmapData;

			indTimer = new Timer(60);
			indTimer.addEventListener(TimerEvent.TIMER, onIndeterminateTimer);

			indShape = new Shape();
			indShape.alpha = .5;
			indMatrix = new Matrix();
			
			progressIndicator = new Shape();
			addChild(progressIndicator);
			
			outline = new Shape();
			addChild(outline);

            super(120, 10, bgColor);
		}
		
		override public function setSize(w:Number, h:Number):Boolean
		{
			var resized:Boolean = super.setSize(w, h);
			if (resized) redraw();
			return resized;
		}
		
		public function get progress():Number
		{
			return _progress;
		}

		public function set progress(value:Number):void
		{
			// indeterminate = false;
			if (value != _progress)
			{
				_progress = value;
				redraw();
			}
		}

		public function get indeterminate():Boolean
		{
			return _indeterminate;
		}

		public function set indeterminate(value:Boolean):void
		{
			if (value != _indeterminate)
			{
				var wasInd:Boolean = _indeterminate;
				if (wasInd)
				{
					indTimer.stop();
					removeChild(indShape);
				}
				else
				{
					indTimer.start();
					addChildAt(indShape, 0);
				}
				_indeterminate = value;
				redraw();
			}
		}
		
		protected function onIndeterminateTimer(event:TimerEvent):void
		{
			if (indMatrix.tx < pattern.width)
			{
				indMatrix.tx += 3;
			}
			else
			{
				indMatrix.tx = 0;
			}
			redraw();
		}

		protected function redraw():void
		{
			var rect:Rectangle = new Rectangle(0, 0, _width, _height);
			rect.x = rect.y = 0;
			
			with (outline.graphics)
			{
				clear();
				if (outlineColor)
				{
    				lineStyle(0, outlineColor.hex, 1, true);
    				drawRect(0, 0, rect.width - 1, rect.height - 1);
    				lineStyle();
                }
			}
				
			if (_indeterminate)
			{
				with (indShape.graphics)
				{
					clear();
					beginBitmapFill(pattern, indMatrix, true, false);
					drawRect(rect.x, rect.y, rect.width, rect.height);
					endFill();
				}
			}

			rect.width *= _progress;
			with (progressIndicator.graphics)
			{
				clear();
				if (!isNaN(rect.width) && progressFillColor)
				{
					beginFill(progressFillColor.hex, progressFillColor.alpha);
					drawRect(rect.x, rect.y, rect.width, rect.height);
					endFill();
				}
			}
		}
	}
}