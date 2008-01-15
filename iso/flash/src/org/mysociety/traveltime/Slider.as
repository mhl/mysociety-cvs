/**
 * Copyright (c) 2008 UK Citizens Online Democracy. All rights reserved.
 * 
 * Email: tom@stamen.com. WWW: http://www.stamen.com/
 * 
 * Redistribution and use in source and binary forms, with or without 
 * modification, are permitted provided that the following conditions are met:
 * 
 * - Redistributions of source code must retain the above copyright notice, 
 *   this list of conditions and the following disclaimer.
 * 
 * - Redistributions in binary form must reproduce the above copyright notice, 
 *   this list of conditions and the following disclaimer in the documentation 
 *   and/or other materials provided with the distribution.
 * 
 * - Neither the name of UK Citizens Online Democracy nor the names of its 
 *   contributors may be used to endorse or promote products derived from 
 *   this software without specific prior written permission.
 * 
 * THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
 * "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
 * LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
 * A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR
 * CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
 * EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
 * PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
 * PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
 * LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
 * NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
 * SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
 * 
 * @version $Id: Slider.as,v 1.1 2008-01-15 03:01:01 tcarden Exp $
 */
package org.mysociety.traveltime
{
	import flash.display.Shape;
	import flash.display.Sprite;
	import flash.events.Event;
	import flash.events.MouseEvent;
	import flash.filters.DropShadowFilter;
	import flash.geom.ColorTransform;
	import flash.geom.Rectangle;
	import flash.text.AntiAliasType;
	import flash.text.TextField;
	import flash.text.TextFormat;
	import flash.text.TextFormatAlign;	
	
	public class Slider extends Sprite 
	{
		// events
		public static const RANGE_CHANGED:String = "rangeChanged";
		public static const DONE_CHANGING:String = "doneChanging";

		// "between this and that"		
		public var descriptionText:String;
		// pounds, minutes, whatever
		public var labelFormat:String;
		public var min:Number;
		public var max:Number;
		public var precision:Number;
	
		// for position and sizing
		public var bounds:Rectangle;
		
		// graphics
		public var slider1:Sprite;
		public var slider2:Sprite;
		public var sliderTrack:Sprite;
		public var runner:Sprite;
	
		// label text
		public var lowerText:String;
		public var upperText:String;
	
		// interaction
		public var sliding:Sprite;
		
		// output
		public var range:Array = [0, 0];
		public var labelRange:Array = [0, 0];
		
		private var hPadding:Number = 50;
		
		public var belowColor:uint = 0x000000; 
		public var aboveColor:uint = 0x000000; 
	
		public function Slider(bounds:Rectangle=null, descriptionText:String="between ${l} and ${u}", labelFormat:String='£${d}', min:Number=0, max:Number=500000, precision:Number=5000)
		{
			if (!bounds) bounds = new Rectangle(0,0,1000,1000);
			this.bounds = bounds;

			this.descriptionText = descriptionText;			
			this.labelFormat = labelFormat;
			this.min = min;
			this.max = max;
			this.precision = precision;
			
			sliderTrack = new Sprite();
			sliderTrack.x = hPadding;
			sliderTrack.y = bounds.y + 6;
			//sliderTrack.scaleX = 0.5;
			addChild(sliderTrack);
			
			runner = new Sprite();
			runner.buttonMode = runner.useHandCursor = true;
			runner.graphics.clear();
			runner.graphics.beginFill(0xffffff);
			runner.graphics.lineStyle(1, 0x808080);
			runner.graphics.drawRect(0,-5,bounds.width-(2*hPadding),10);
			runner.addEventListener(MouseEvent.MOUSE_DOWN, onRunnerMouseDown);
			sliderTrack.addChild(runner);
			
			slider1 = new Sprite();
			slider2 = new Sprite();
			for each (var slider:Sprite in [slider1, slider2]) {
				slider.buttonMode = slider.useHandCursor = true;
				slider.addEventListener(MouseEvent.MOUSE_DOWN, onSliderMouseDown);
				
				var nib:Shape = new Shape();
				nib.name = 'nib';
				
				nib.graphics.clear();
				nib.graphics.beginFill(0xff8080);
				nib.graphics.lineStyle(0,0x800000,1,true);
//				nib.graphics.drawCircle(0,0,4);

				nib.graphics.moveTo(0,-4);
				nib.graphics.lineTo(4,1);
				nib.graphics.lineTo(4,6);
				nib.graphics.lineTo(-4,6);
				nib.graphics.lineTo(-4,1);
				nib.graphics.lineTo(0,-4);
				
				nib.graphics.endFill();

				nib.graphics.lineStyle(0,0x800000,0.5,true);
				nib.graphics.moveTo(-1,0);
				nib.graphics.lineTo(-1,4);

				nib.graphics.moveTo(1,0);
				nib.graphics.lineTo(1,4);
				
				nib.filters = [ new DropShadowFilter(3, 30, 0x000000, 0.5, 8, 8, 2, 1, false, false, false) ];
				slider.addChild(nib);
				
				slider.addEventListener(MouseEvent.MOUSE_OVER, function(event:Event):void {
					var nib:Shape = event.target.getChildByName('nib') as Shape;
					nib.transform.colorTransform = new ColorTransform(2,2,2,1,20,0,0,0);				
				});
				slider.addEventListener(MouseEvent.MOUSE_OUT, function(event:Event):void {
					var nib:Shape = event.target.getChildByName('nib') as Shape;
					nib.transform.colorTransform = new ColorTransform();				
				});

				sliderTrack.addChild(slider);
				var label:TextField = new TextField();
				label.defaultTextFormat = new TextFormat("HelveticaNorm", 14, 0xffffff, null, null, null, null, null, TextFormatAlign.CENTER);
				label.embedFonts = true;
				label.antiAliasType = AntiAliasType.ADVANCED;
				label.name = 'label';
				slider.addChild(label);
				slider.mouseChildren = false;
				label.y = 8;
				label.x = -label.width/2;
				label.text = 'hello';
				label.height = label.textHeight+4;
				label.text = '';
				label.selectable = false;
				label.backgroundColor = 0x000000;
				label.background = true;
			}
			
			slider1.x = 2;
			slider2.x = bounds.width-2-(hPadding*2);
	
			redraw(true);
		}	

		public function getDescription():String
		{
			var des:String = descriptionText.replace("${l}", lowerText);
			des = des.replace("${u}", upperText);
			return des;
		}

		/** gives numbers between 0 and 1 */		
		public function getRange():Array
		{
			return this.range;
		}

		/** gives numbers between min and max */		
		public function getLabelRange():Array
		{
			return this.labelRange;
		}

		/** takes numbers between 0 and 1 */				
		public function setRange(rMin:Number, rMax:Number):void
		{
			slider1.x = 2 + (rMin*(bounds.width-4-(2*hPadding)));
			slider2.x = 2 + (rMax*(bounds.width-4-(2*hPadding)));
			redraw(true);			
		}

		/** takes numbers between min and max */				
		public function setLabelRange(lMin:Number, lMax:Number):void
		{
			var lMin2:Number = Math.min(lMin, lMax);
			var lMax2:Number = Math.max(lMin, lMax);
			lMin2 = Math.max(min, lMin2);
			lMax2 = Math.min(max, lMax2);
			var rMin:Number = (lMin2 - min) / (max - min);
			var rMax:Number = (lMax2 - min) / (max - min);
			setRange(rMin, rMax);
		}
		
		private function onRunnerMouseDown(event:MouseEvent):void
		{
			runner.startDrag(false, new Rectangle(2,0,bounds.width-4-(2*hPadding)-runner.width,0));
			stage.addEventListener(MouseEvent.MOUSE_UP, onRunnerMouseUp);			
			stage.addEventListener(Event.MOUSE_LEAVE, onRunnerMouseUp);			
			stage.addEventListener(MouseEvent.MOUSE_MOVE, onRunnerMouseMove);			
		}
				
		private function onRunnerMouseUp(event:Event):void
		{
			runner.stopDrag();
			stage.removeEventListener(MouseEvent.MOUSE_UP, onRunnerMouseUp);
			stage.removeEventListener(Event.MOUSE_LEAVE, onRunnerMouseUp);			
			stage.removeEventListener(MouseEvent.MOUSE_MOVE, onRunnerMouseMove);			
			slider1.x = runner.x;
			slider2.x = runner.x + runner.width;
			redraw(false);
			dispatchEvent(new Event(Slider.DONE_CHANGING));			
		}
		
		private function onRunnerMouseMove(event:MouseEvent):void
		{
			slider1.x = runner.x;
			slider2.x = runner.x + runner.width;
			redraw(false);
		}
		
		private function onSliderMouseDown(event:MouseEvent):void
		{
			sliding = event.target as Sprite;
			sliding.startDrag(false, new Rectangle(2,0,bounds.width-4-(2*hPadding),0));
			stage.addEventListener(MouseEvent.MOUSE_UP, onSliderMouseUp);			
			stage.addEventListener(Event.MOUSE_LEAVE, onSliderMouseUp);			
			stage.addEventListener(MouseEvent.MOUSE_MOVE, onSliderMouseMove);
		}
		
		private function onSliderMouseUp(event:Event):void
		{
			sliding.stopDrag();
			sliding = null;
			stage.removeEventListener(MouseEvent.MOUSE_UP, onSliderMouseUp);			
			stage.removeEventListener(Event.MOUSE_LEAVE, onSliderMouseUp);			
			stage.removeEventListener(MouseEvent.MOUSE_MOVE, onSliderMouseMove);
			onSliderMouseMove(null);
			dispatchEvent(new Event(Slider.DONE_CHANGING));			
		}
	
		private function onSliderMouseMove(event:Event):void
		{
			redraw(true);
		}
		
		private function redraw(resizeRunner:Boolean):void
		{
			var left:Sprite = slider1.x < slider2.x ? slider1 : slider2; 
			var right:Sprite = slider1.x >= slider2.x ? slider1 : slider2; 
	
			sliderTrack.graphics.clear();
			sliderTrack.graphics.beginFill(0x000000);
			sliderTrack.graphics.drawRect(0,-3,bounds.width-(2*hPadding),6);
			sliderTrack.graphics.beginFill(belowColor);
			sliderTrack.graphics.drawRect(0,-2,left.x,4);
	
			if (resizeRunner) {
				runner.x = left.x;
				runner.width = right.x - left.x;
			}
	
			sliderTrack.graphics.beginFill(aboveColor);
			sliderTrack.graphics.drawRect(right.x,-2,bounds.width-(2*hPadding)-right.x,4);		
	
			var leftLabel:TextField = slider1.x < slider2.x ? slider1.getChildByName('label') as TextField : slider2.getChildByName('label') as TextField; 
			var rightLabel:TextField = slider1.x >= slider2.x ? slider1.getChildByName('label') as TextField : slider2.getChildByName('label') as TextField; 
			
			var lower:Number = Math.min(slider1.x, slider2.x);
			var upper:Number = Math.max(slider1.x, slider2.x);
			
			lower = (lower-2) / (bounds.width-4-(2*hPadding));
			upper = (upper-2) / (bounds.width-4-(2*hPadding));
					
 			this.range = [lower, upper];
			trace("range: " + range);
	
			lower = min + (lower * (max-min));
			upper = min + (upper * (max-min));
			
			var lowerExact:Number = lower;
			var upperExact:Number = upper;
	
/* 			lower = precision * Math.floor(lower / precision);		
			upper = precision * Math.ceil(upper / precision); */

			lower = precision * Math.ceil(lower / precision);		
			upper = precision * Math.ceil(upper / precision);

 			this.labelRange = [lower, upper];
						
			// put commas in long numbers: let's just assume we're not talking about 1000s of minutes here
			// TODO replace labelFormat with 'units' that numFormat knows about?
			lowerText = numFormat(lower.toString());
			upperText = numFormat(upper.toString());
			
			lowerText = labelFormat.replace('${d}', lowerText);
/* 			if (lower == min) {
				lCommad = "<"+lCommad;
 			}*/
			
			if (upperExact == max) {
				upperText += "+";
				trace("+", upperExact, max);
			}
			else {
				trace(upperExact, max);
			}
			upperText = labelFormat.replace('${d}', upperText);
						
	 		leftLabel.text = lowerText;
			leftLabel.width = leftLabel.textWidth+4;
			leftLabel.x = -leftLabel.width/2;
			rightLabel.text = upperText;
			rightLabel.width = rightLabel.textWidth+4;
			rightLabel.x = -rightLabel.width/2;
			
			leftLabel.backgroundColor = belowColor;
			rightLabel.backgroundColor = aboveColor;
			
			dispatchEvent(new Event(Slider.RANGE_CHANGED));
		}
	
		private function numFormat(s:String):String
		{	
			for (var i:int = s.length - 3; i > 0; i -= 3) {
				s = s.substr(0,i) + "," + s.slice(i);
			}
			return s;
		}		
			
	}
}
