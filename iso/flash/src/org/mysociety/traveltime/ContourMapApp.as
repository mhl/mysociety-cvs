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
 * @version $Id: ContourMapApp.as,v 1.1 2008-01-15 03:01:01 tcarden Exp $
 */
package org.mysociety.traveltime
{
	import flash.display.Bitmap;
	import flash.display.BitmapData;
	import flash.display.BitmapDataChannel;
	import flash.display.BlendMode;
	import flash.display.Loader;
	import flash.display.LoaderInfo;
	import flash.display.Shape;
	import flash.display.Sprite;
	import flash.events.ErrorEvent;
	import flash.events.Event;
	import flash.events.HTTPStatusEvent;
	import flash.events.IOErrorEvent;
	import flash.events.MouseEvent;
	import flash.events.ProgressEvent;
	import flash.events.SecurityErrorEvent;
	import flash.filters.ColorMatrixFilter;
	import flash.filters.ConvolutionFilter;
	import flash.geom.Point;
	import flash.geom.Rectangle;
	import flash.net.URLRequest;
	import flash.text.TextField;
	import flash.text.TextFormat;
	import flash.text.TextFormatAlign;
	
	import org.mysociety.BaseApp;
	import org.mysociety.util.buildDesaturateArray;
	import org.mysociety.util.buildLaplacianEdgeArray;

	public class ContourMapApp extends BaseApp
	{
		override public function configReady(config:XML):void
		{
			var map:Loader = new Loader();
			map.load(new URLRequest(config.mapURL.text()));
			map.contentLoaderInfo.addEventListener(Event.COMPLETE, onMapLoaded);
			map.contentLoaderInfo.addEventListener(ProgressEvent.PROGRESS, function(event:ProgressEvent):void { progress('contours', event); });			
			map.contentLoaderInfo.addEventListener(SecurityErrorEvent.SECURITY_ERROR, function(event:ErrorEvent):void { error(event.text); });			
			map.contentLoaderInfo.addEventListener(HTTPStatusEvent.HTTP_STATUS, function(event:HTTPStatusEvent):void { trace(event); });
			map.contentLoaderInfo.addEventListener(IOErrorEvent.IO_ERROR, function(event:ErrorEvent):void { error(event.text); });			
			addChild(map);
		}
		
		private function onMapLoaded(event:Event):void
		{
			var contours:Loader = new Loader();
			contours.load(new URLRequest(config.contour[0].url.text()));
			contours.contentLoaderInfo.addEventListener(Event.COMPLETE, onContoursLoaded);
			contours.contentLoaderInfo.addEventListener(ProgressEvent.PROGRESS, function(event:ProgressEvent):void { progress('contours', event); });			
			contours.contentLoaderInfo.addEventListener(SecurityErrorEvent.SECURITY_ERROR, function(event:ErrorEvent):void { error(event.text); });			
			contours.contentLoaderInfo.addEventListener(HTTPStatusEvent.HTTP_STATUS, function(event:HTTPStatusEvent):void { trace(event); });
			contours.contentLoaderInfo.addEventListener(IOErrorEvent.IO_ERROR, function(event:ErrorEvent):void { error(event.text); });			
		}
		
		private function onContoursLoaded(event:Event):void
		{
			clearText();
			
			var contours:Bitmap = (event.target as LoaderInfo).content as Bitmap;

			// for whole-image filtering and threshold operations, below...
			var sourceRect:Rectangle = new Rectangle(0, 0, contours.width, contours.height);
			var destPoint:Point = new Point();

			/////////////////
			
			// let's only parse XML once:
			var mappings:Array = [];
			for each (var m:XML in config.contour[0].mapping) {
				mappings.push( {
					threshold: parseInt(m.@source, 16),
					mask: parseInt(m.@mask, 16),
					color: parseInt(m.@target, 16),
					label: m.@label,
					labelColor: parseInt(m.@labelColor, 16)
				});
			}

			/////////////////
			
			// map the contour image using source-->target colors from the XML config file
			var mapped:Bitmap = new Bitmap(new BitmapData(contours.width, contours.height, true, 0x00000000));
			for each (var mapping:Object in mappings) {
				mapped.bitmapData.threshold(contours.bitmapData, 
											sourceRect, 
											destPoint, 
											"<=",
											mapping.threshold, 
											mapping.color, 
											mapping.mask,
											false);
			}
			mapped.blendMode = BlendMode.MULTIPLY;
			addChild(mapped);
			
			/////////////////
			
			// make an outline image from the mapped image by desaturating, edge detecting and setting alpha to red brightness
			var outlines:Bitmap = new Bitmap(new BitmapData(mapped.width, mapped.height, true, 0x00000000));
			outlines.bitmapData.applyFilter(mapped.bitmapData, sourceRect, destPoint, new ColorMatrixFilter(buildDesaturateArray())); 
			outlines.bitmapData.applyFilter(outlines.bitmapData, sourceRect, destPoint, new ConvolutionFilter(5, 5, buildLaplacianEdgeArray()));
			outlines.bitmapData.copyChannel(outlines.bitmapData, sourceRect, destPoint, BitmapDataChannel.RED, BitmapDataChannel.ALPHA);
			outlines.blendMode = BlendMode.ADD;
			outlines.alpha = 0.4;
			addChild(outlines);
			
			/////////////////

			// TODO: make optional			
			var labels:Loader = new Loader();
			labels.load(new URLRequest(config.labelURL.text()));
			labels.mouseEnabled = false;
			addChild(labels);

			/////////////////

			setTextFormat("Helvetica", 14, 0x000000, true);
			var text:TextField = getText(config.title[0].text(), 5, 5, stage.stageWidth-11);
			var textBack:Shape = new Shape();
			textBack.graphics.lineStyle(0,0xffffff,0.5,true);
			textBack.graphics.beginFill(0xffffff,0.6);
			textBack.graphics.drawRect(0,0,text.x+text.width+5,text.y+text.height+3);
			addChild(textBack);
			addChild(text);

			/////////////////

			// TODO: make optional
			var key:Sprite = new Sprite();
			var ky:Number = 0;
			var kw:Number = 55;
			var kh:Number = 22;
			var kx:Number = stage.stageWidth - kw - 1;
			key.graphics.beginFill(0xffffff, 0.6);
			key.graphics.lineStyle(0,0xffffff,0.5,true);
			key.graphics.drawRect(0,0,stage.stageWidth-1,kh);
			key.graphics.endFill(); 
			var rmappings:Array = mappings.reverse();
			setTextFormat("Helvetica", 12, 0x000000, true, false, false, null, null, TextFormatAlign.CENTER);
			key.addChild(getText(config.contour[0].labelDescription[0].text(), 5, (kh-12)/2));
			for each (var rmapping:Object in rmappings) {
				var alpha:uint = (rmapping.color & 0xff000000) >>> 24; 
				if (alpha > 0) {
					key.graphics.beginFill(rmapping.color);
					key.graphics.lineStyle(0,0xffffff,0.5,true);
					key.graphics.drawRect(kx,ky,kw,kh);
					key.graphics.endFill();
					var kt:TextField = getText(rmapping.label, kx, ky + (kh-12)/2, kw); 
					kt.textColor = rmapping.labelColor;					 
					key.addChild( kt );					
					kx -= kw;
				}
			}			
			key.y = contours.height - key.height - 1;			
			addChild(key);

			/////////////////

			// TODO: make optional, make text color smart about background color
			setTextFormat("Helvetica", 12, 0x000000);
			var tip:TextField = getText('',0,0);
			tip.wordWrap = false;
			tip.multiline = false;
			tip.background = true;
			tip.backgroundColor = 0xffffffdd;
			tip.visible = false;
			addChild(tip);
			
			// check colour of mapped bitmap under the mouse and set the tooltip accordingly
			var mousey:Sprite = new Sprite();
			mousey.graphics.beginFill(0x000000,0);
			mousey.graphics.drawRect(0,0,mapped.width,mapped.height);
			addChild(mousey);
			var labelFormat:String = config.contour[0].labelUnits[0].text(); 
			var mouseyFun:Function = function (event:Event):void {
				var mouseColor:uint = 0xff000000 | mapped.bitmapData.getPixel(stage.mouseX, stage.mouseY);
				//trace(mouseColor.toString(16));
				var got:Boolean = false;
				for each (var mapping:Object in mappings) {
					if (mapping.color == mouseColor) {
						tip.text = labelFormat.replace("${l}", mapping.label);						 
						tip.x = stage.mouseX + 10;
						tip.y = stage.mouseY + 10;
						tip.height = tip.textHeight + 4;
						tip.width = tip.textWidth + 4;
						tip.backgroundColor = mapping.color;
						tip.textColor = rmapping.labelColor;
						if (tip.text.length > 0) {
							got = true;
						}
						break;
					}
				}
				tip.visible = got;
			};
			mousey.addEventListener(MouseEvent.MOUSE_OVER, mouseyFun);
			mousey.addEventListener(MouseEvent.MOUSE_MOVE, mouseyFun);
			mousey.addEventListener(MouseEvent.MOUSE_OUT, function(event:Event):void { tip.visible = false; });						
			
		}
		
		// Processing-style stateful text functions, because I'm tired of writing all these lines:
		// not good Actionscript, but tidy up there ^
		
		private var dtf:TextFormat = new TextFormat("Helvetica", 11, 0x000000, false);
		
		private function setTextFormat(font:String="Helvetica", size:int=11, color:uint=0x000000, bold:Boolean=false, italic:Boolean=false, underline:Boolean=false, url:String=null, target:String=null, align:String=null):TextFormat
		{
			dtf = new TextFormat(font, size, color, bold, italic, underline, url, target, align);
			return dtf;
		}
		
		private function getText(t:String, tx:Number=0, ty:Number=0, tw:Number=0, th:Number=0):TextField
		{
			var tf:TextField = new TextField();
			tf.selectable = false;
			tf.mouseEnabled = false;
			tf.defaultTextFormat = dtf;
			tf.text = t;
			tf.width = tw > 0 ? tw : tf.textWidth + 4;
			tf.height = th > 0 ? th : tf.textHeight + 4;
			tf.x = tx;
			tf.y = ty;
			return tf;
		}
		
	}
}

