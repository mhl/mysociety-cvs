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
 * @version $Id: MaskedContourMapApp.as,v 1.1 2008-01-15 03:01:01 tcarden Exp $
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
	import flash.filters.BitmapFilterQuality;
	import flash.filters.ColorMatrixFilter;
	import flash.filters.ConvolutionFilter;
	import flash.filters.DropShadowFilter;
	import flash.filters.GlowFilter;
	import flash.geom.ColorTransform;
	import flash.geom.Point;
	import flash.geom.Rectangle;
	import flash.net.URLRequest;
	import flash.text.AntiAliasType;
	import flash.text.TextField;
	import flash.text.TextFormatAlign;
	import flash.utils.clearTimeout;
	import flash.utils.setTimeout;
	
	import org.mysociety.BaseApp;
	import org.mysociety.util.buildDesaturateArray;

	public class MaskedContourMapApp extends BaseApp
	{
		private var map:Bitmap;
		private var contours:Bitmap;
		private var houseMask:Bitmap;
		
		override public function configReady(config:XML):void
		{
			var map:Loader = new Loader();
			map.load(new URLRequest(config.mapURL.text()));
			map.contentLoaderInfo.addEventListener(Event.COMPLETE, onMapLoaded);
			map.contentLoaderInfo.addEventListener(ProgressEvent.PROGRESS, function(event:ProgressEvent):void { progress('contours', event); });			
			map.contentLoaderInfo.addEventListener(SecurityErrorEvent.SECURITY_ERROR, function(event:ErrorEvent):void { error(event.text); });			
			map.contentLoaderInfo.addEventListener(HTTPStatusEvent.HTTP_STATUS, function(event:HTTPStatusEvent):void { trace(event); });
			map.contentLoaderInfo.addEventListener(IOErrorEvent.IO_ERROR, function(event:ErrorEvent):void { error(event.text); });			
		}
		
		private function onMapLoaded(event:Event):void
		{
			map = (event.target as LoaderInfo).content as Bitmap;
	
			var loader:Loader = new Loader();
			if (config.contour.length() > 0) {		
				loader.load(new URLRequest(config.contour[0].url.text()));
				loader.contentLoaderInfo.addEventListener(Event.COMPLETE, onContoursLoaded);
				loader.contentLoaderInfo.addEventListener(ProgressEvent.PROGRESS, function(event:ProgressEvent):void { progress('contours', event); });			
				loader.contentLoaderInfo.addEventListener(SecurityErrorEvent.SECURITY_ERROR, function(event:ErrorEvent):void { error(event.text); });			
				loader.contentLoaderInfo.addEventListener(HTTPStatusEvent.HTTP_STATUS, function(event:HTTPStatusEvent):void { trace(event); });
				loader.contentLoaderInfo.addEventListener(IOErrorEvent.IO_ERROR, function(event:ErrorEvent):void { error(event.text); });
			}
			else if (config.mask.length() > 0) {			
				loader.load(new URLRequest(config.mask[0].url.text()));
				loader.contentLoaderInfo.addEventListener(Event.COMPLETE, onHouseMaskLoaded);
				loader.contentLoaderInfo.addEventListener(ProgressEvent.PROGRESS, function(event:ProgressEvent):void { progress('house data', event); });			
				loader.contentLoaderInfo.addEventListener(SecurityErrorEvent.SECURITY_ERROR, function(event:ErrorEvent):void { error(event.text); });			
				loader.contentLoaderInfo.addEventListener(HTTPStatusEvent.HTTP_STATUS, function(event:HTTPStatusEvent):void { trace(event); });
				loader.contentLoaderInfo.addEventListener(IOErrorEvent.IO_ERROR, function(event:ErrorEvent):void { error(event.text); });
			}
			else {
				error("no contour or mask URL given");
			}	
		}

		private function onContoursLoaded(event:Event):void
		{
			contours = (event.target as LoaderInfo).content as Bitmap;

			if (config.mask.length() > 0) {			
				var loader:Loader = new Loader();
				loader.load(new URLRequest(config.mask[0].url.text()));
				loader.contentLoaderInfo.addEventListener(Event.COMPLETE, onHouseMaskLoaded);
				loader.contentLoaderInfo.addEventListener(ProgressEvent.PROGRESS, function(event:ProgressEvent):void { progress('house data', event); });			
				loader.contentLoaderInfo.addEventListener(SecurityErrorEvent.SECURITY_ERROR, function(event:ErrorEvent):void { error(event.text); });			
				loader.contentLoaderInfo.addEventListener(HTTPStatusEvent.HTTP_STATUS, function(event:HTTPStatusEvent):void { trace(event); });
				loader.contentLoaderInfo.addEventListener(IOErrorEvent.IO_ERROR, function(event:ErrorEvent):void { error(event.text); });
			}
			else {
				onHouseMaskLoaded(null);
			}			
		}
		
		private function onHouseMaskLoaded(event:Event):void
		{
			if (event && event.target) {
				houseMask = (event.target as LoaderInfo).content as Bitmap;
			}
		
			clearText();
			
			// for whole-image filtering and threshold operations, below...
			var sourceRect:Rectangle = new Rectangle(0, 0, map.width, map.height);
			var destPoint:Point = new Point();

			//////////////////

			if (!houseMask) map.bitmapData.applyFilter(map.bitmapData, sourceRect, destPoint, new ColorMatrixFilter(buildDesaturateArray(0)));
			addChild(map);

			if (contours) {
			
				/////////////////
				
				// let's only parse XML once:
				var mappings:Array = [];
				for each (var m:XML in config.contour[0].mapping) {
					mappings.push({
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
				
				var mappedContainer:Sprite = new Sprite();
				mappedContainer.cacheAsBitmap = true;
				mappedContainer.addChild(mapped);
				addChild(mappedContainer);
	
				if (!houseMask) {
					mappedContainer.blendMode = BlendMode.MULTIPLY;
				}
				
			}
			
			/////////////////

			if (houseMask) {

				var thresh:uint = parseInt(config.mask[0].goodColor[0].text().toString(), 16);

				// if there are contours, let's mask those:
				if (contours) {	
					
					// make the coloured contour data (or map) only show where house prices are OK:
					
					var mappedMask:Bitmap = new Bitmap(new BitmapData(houseMask.width, houseMask.height, true, 0x00000000));
					mappedMask.bitmapData.threshold(houseMask.bitmapData,
												   sourceRect,
												   destPoint,
												   "==",
												   thresh,
												   0xffffffff,
												   0xffffffff,
												   false);
					mappedMask.cacheAsBitmap = true;
					addChild(mappedMask);
					
					mappedContainer.mask = mappedMask;
	
					// find the intersection and highlight it with yellow?
					mappedContainer.filters = [ new GlowFilter(0xffff00, 1, 4, 4, 8, 1, true) ];
	
					// now make the rest be grey:
					
					var greyMap:Bitmap = new Bitmap(map.bitmapData.clone());
					greyMap.alpha = 0.3;
					//greyMap.bitmapData.applyFilter(greyMap.bitmapData, sourceRect, destPoint, new ColorMatrixFilter(buildDesaturateArray()));
					
					var greyData:Bitmap = new Bitmap(mapped.bitmapData.clone());
					greyData.alpha = 0.4;
					
					var greyMask:Bitmap = new Bitmap(new BitmapData(houseMask.width, houseMask.height, true, 0x00000000));
					greyMask.bitmapData.threshold(houseMask.bitmapData,
												 sourceRect,
												 destPoint,
												 "!=",
												 thresh,
												 0xffffffff,
												 0xffffffff,
												 false);
					greyMask.cacheAsBitmap = true;
					
					var greyContainer:Sprite = new Sprite();
					greyContainer.graphics.beginFill(0x000000);
					greyContainer.graphics.drawRect(0,0,map.width,map.height);
					greyContainer.cacheAsBitmap = true;
					greyContainer.addChild(greyMap);
					greyContainer.addChild(greyData);
					greyContainer.addChild(greyMask);
					greyContainer.mask = greyMask;
					greyContainer.filters = [ new ColorMatrixFilter(buildDesaturateArray()) ];
					//new GlowFilter(0xffffff, 1, 4, 4, 8, 1, true) ];
					addChild(greyContainer);
					
					// TODO: make optional			
		 			var greyLabels:Loader = new Loader();
					greyLabels.load(new URLRequest(config.labelURL.text()));
					greyLabels.mouseEnabled = false;
					greyLabels.transform.colorTransform = new ColorTransform(-1,-1,-1,1,255,255,255,0);
					greyContainer.addChild(greyLabels);
				
				}				
				else {					
					// but if there aren't any contours, let's mask the map

					// make the coloured contour data (or map) only show where house prices are OK:
					
					var mapMask:Bitmap = new Bitmap(new BitmapData(houseMask.width, houseMask.height, true, 0x00000000));
 					mapMask.bitmapData.threshold(houseMask.bitmapData,
												   sourceRect,
												   destPoint,
												   "==",
												   thresh,
												   0xffffffff,
												   0xffffffff,
												   false);
					mapMask.cacheAsBitmap = true;
					addChild(mapMask);

 					var greyStuff:Sprite = new Sprite();
					greyStuff.addChild(new Bitmap(map.bitmapData.clone()));
					greyStuff.cacheAsBitmap = true;
					greyStuff.mask = mapMask;
					greyStuff.filters = [ new GlowFilter(0xffff00, 1, 4, 4, 8, 1, true) ];
					addChild(greyStuff);
 					
 					// desaturate and dim the map:
					map.filters = [ new ColorMatrixFilter(buildDesaturateArray()) ];
					map.alpha = 0.4;

					// add inverted labels for the desaturated map:
 		 			var inverseLabels:Loader = new Loader();
					inverseLabels.load(new URLRequest(config.labelURL.text()));
					inverseLabels.mouseEnabled = false;
					inverseLabels.transform.colorTransform = new ColorTransform(-1,-1,-1,1,255,255,255,0);
					addChildAt(inverseLabels, getChildIndex(map)+1);
					
				}
			}
						
			/////////////////
			
			if (contours) {
			
				// make an outline image from the mapped image by desaturating, edge detecting and setting alpha to red brightness
				var outlines:Bitmap = new Bitmap(new BitmapData(mapped.width, mapped.height, true, 0xff000000));
				outlines.bitmapData.applyFilter(contours.bitmapData, sourceRect, destPoint, new ColorMatrixFilter(buildDesaturateArray())); 
	
				// this is approximately "Sobel" Edge detection...
				
				// get horizontal edges,
				// bias is 128 so that "left" and "right" edges can be black or white
				var horiz:BitmapData = new BitmapData(outlines.width, outlines.height);
				horiz.applyFilter(outlines.bitmapData, sourceRect, destPoint, new ConvolutionFilter(3, 3, [ -1, 0, 1, -2, 0, 2, -1, 0, 1 ], 1, 128, true, true));			
	
				// get vertical edges,
				// bias is 128 so that "top" and "bottom" edges can be black or white
				var vertz:BitmapData = new BitmapData(outlines.width, outlines.height);
				vertz.applyFilter(outlines.bitmapData, sourceRect, destPoint, new ConvolutionFilter(3, 3, [ -1, -2, -1, 0, 0, 0, 1, 2, 1 ], 1, 128, true, true));			
	
				// set outlines data to be magnitude of horizontal and vertical edges
				for (var px:int = 0; px < horiz.width; px++) {
					for (var py:int = 0; py < horiz.height; py++) {
						var hb:int = 0x80 - (horiz.getPixel(px,py) & 0x000000ff);
						var vb:int = 0x80 - (vertz.getPixel(px,py) & 0x000000ff);
						var b:uint = Math.min(0x80, Math.sqrt( (hb * hb) + (vb * vb) )); 
						var color:uint = b << 24 | b << 16 | b << 8 | b;
						outlines.bitmapData.setPixel(px,py,color);
					}				
				}
				
				// these were temporary...
				horiz.dispose();
				vertz.dispose();
	
				// set alpha to red brightness (so that non-edges are transparent)
				outlines.bitmapData.copyChannel(outlines.bitmapData, sourceRect, destPoint, BitmapDataChannel.RED, BitmapDataChannel.ALPHA);
	
				outlines.blendMode = BlendMode.ADD;
	//			outlines.alpha = 0.5;
				addChild(outlines);
				
			}
			
			/////////////////

			if (!houseMask) {
				// TODO: make optional			
	 			var labels:Loader = new Loader();
				labels.load(new URLRequest(config.labelURL.text()));
				labels.mouseEnabled = false;
				addChild(labels);
			}

			/////////////////

			setTextFormat("HelveticaBold", (stage.stageWidth > 500) ? 14 : 12, 0x000000, true);
			var text:TextField = getText(config.title[0].text(), 5, 5, stage.stageWidth-11, 0, true);
			var textBack:Shape = new Shape();
			textBack.graphics.lineStyle(0,0xffffff,0.5,true);
			textBack.graphics.beginFill(0xffffff,0.7);
			textBack.graphics.drawRect(0,0,text.x+text.width+5,text.y+text.height+3);
			addChild(textBack);
			addChild(text);

			/////////////////

			if (contours) {

				var rmappings:Array = mappings.reverse().filter(function(mapping:Object, i:int, array:Array):Boolean {
					return ((mapping.color & 0xff000000) >>> 24) > 0;
				});
				
				
				// TODO: make optional
				var key:Sprite = new Sprite();
				var ky:Number = 0;
				var kh:Number = 22;
				setTextFormat("HelveticaBold", (stage.stageWidth > 500) ? 12 : 11, 0x000000, true, false, false, null, null, TextFormatAlign.CENTER);
				var keyTitle:TextField = getText(config.contour[0].labelDescription[0].text(), 5, (kh-12)/2);
				key.addChild(keyTitle);
				var kw:Number = Math.min(stage.stageWidth - 10 - keyTitle.width, stage.stageWidth/2);
				key.graphics.beginFill(0xffffff, 0.7);
				key.graphics.drawRect(0,0,stage.stageWidth,kh);
				key.graphics.endFill();
				kw =  Math.round(kw / rmappings.length);
				var kx:Number = stage.stageWidth - kw;
				trace(kw);
				for each (var rmapping:Object in rmappings) {
					key.graphics.beginFill(rmapping.color);
					key.graphics.drawRect(kx+1,ky,kw-1,kh);
					key.graphics.endFill();
					var kt:TextField = getText(rmapping.label, kx, ky + (kh-12)/2, kw); 
					kt.textColor = rmapping.labelColor;					 
					key.addChild( kt );					
					kx -= kw;
				}			
				key.y = contours.height - key.height;
				//key.alpha = 0.7;			
				addChild(key);
			}

			/////////////////

			if (config.centerLabel.length() > 0) {

				var center:Sprite = new Sprite();
				center.graphics.beginFill(0xff0000,0);
				center.graphics.drawCircle(0,0,10);
				center.graphics.beginFill(0xaa0000);
				center.graphics.lineStyle(1,0xffffff,1,true);
				center.graphics.drawCircle(0,0,4);
				center.x = stage.stageWidth/2;
				center.y = stage.stageHeight/2;
				addChild(center);

				var centerOffX:int = 0;
				var centerOffY:int = 0;
				
				if (config.centerLabel[0].@offsetX) {
					centerOffX = parseInt(config.centerLabel[0].@offsetX.toString());					
				}
				if (config.centerLabel[0].@offsetY) {
					centerOffY = parseInt(config.centerLabel[0].@offsetY.toString());					
				}


				var centerTextColor:uint = 0xffffff;
				setTextFormat("HelveticaNorm", (stage.stageWidth > 500) ? 14 : 12, centerTextColor, false);
				var centerText:TextField = getText(config.centerLabel[0].text(), 5, 5);

				var centerTextBack:Sprite = new Sprite();
				centerTextBack.x = centerOffX + 3 + stage.stageWidth / 2;
				centerTextBack.y = centerOffY - ((centerText.y+centerText.height+3)/2) + (stage.stageHeight / 2);
				centerTextBack.addChild(centerText);

				var centerTextBorder:uint = 0x800000;
				setTextFormat("HelveticaNorm", (stage.stageWidth > 500) ? 14 : 12, centerTextBorder, false);
				
				var borders:Sprite = new Sprite();
				
 				for (var offsetX:int = -2; offsetX <= 2; offsetX += 1) {
	 				for (var offsetY:int = -2; offsetY <= 2; offsetY += 1) {
						var borderText:TextField = getText(config.centerLabel[0].text(), 5+offsetX, 5+offsetY);
						borders.addChild(borderText);
					}
				}			
				
				centerTextBack.addChildAt(borders,0);	
				 				 
				addChild(centerTextBack);
				
/* 				var centerTimer:uint = setTimeout(function():void { centerTextBack.visible = false }, 2000);
				
				centerTextBack.mouseEnabled = false;
				
 				center.useHandCursor = center.buttonMode = center.mouseEnabled = true;
				center.addEventListener(MouseEvent.MOUSE_OVER, function(event:MouseEvent):void { clearTimeout(centerTimer); centerTextBack.visible = true; });
				center.addEventListener(MouseEvent.MOUSE_OUT, function(event:MouseEvent):void { centerTimer = setTimeout(function():void { centerTextBack.visible = false }, 750); }); */ 
			}
		
			
			/////////////////

			// TODO: make optional, make text color smart about background color
			setTextFormat("HelveticaNorm", (stage.stageWidth > 500) ? 12 : 11, 0x000000, false);
			var tip:TextField = getText('',0,0);
			tip.filters = [ new DropShadowFilter(3, 30, 0x000000, 0.5, 4, 4, 1, 1) ];
			tip.wordWrap = false;
			tip.multiline = false;
			tip.background = true;
			tip.backgroundColor = 0xffffffdd;
			tip.visible = false;
			addChild(tip);
			
			// check colour of mapped bitmap under the mouse and set the tooltip accordingly
			var mousey:Sprite = new Sprite();
			mousey.graphics.beginFill(0x000000,0);
			mousey.graphics.drawRect(0,0,map.width,map.height);
			addChild(mousey);
			var labelUnits:String = config.contour.length() > 0 ? config.contour[0].labelUnits[0].text() : "";

			var tipTimer:uint;

			var goodColor:uint; 
			var goodLabel:String; 
			var badLabel:String;
			if (houseMask) { 
				goodColor = parseInt(config.mask[0].goodColor[0].text().toString(), 16); 
				goodLabel = config.mask[0].goodLabel[0].text(); 
				badLabel = config.mask[0].badLabel[0].text();
			} 
			var showTip:Function = function(mx:Number, my:Number):void
			{
				tip.visible = true;					
				tip.text = '';
				tip.backgroundColor = 0xffffffdd;
				if (contours) {
					var mouseColor:uint = 0xff000000 | mapped.bitmapData.getPixel(stage.mouseX, stage.mouseY);
					for each (var mapping:Object in mappings) {
						if (mapping.color == mouseColor) {
							tip.text = labelUnits.replace("${l}", mapping.label);						 
							tip.backgroundColor = mapping.color;
							tip.textColor = mapping.labelColor;
							if (houseMask) {
								tip.appendText('\n');
							}
							break;
						}
					}
				}
				if (houseMask) {
					var houseColor:uint = 0xff000000 | houseMask.bitmapData.getPixel(stage.mouseX, stage.mouseY);
					if (houseColor == goodColor) {
						tip.appendText(goodLabel);
					}
					else {
						tip.appendText(badLabel);
						tip.backgroundColor = 0xc0c0c0;
					}
				}
				else {
					if (tip.text.length == 0) {
						tip.visible = false;					
					}
				}
				tip.height = tip.textHeight + 4;
				tip.width = tip.textWidth + 4;
				if (mx + tip.width > stage.stageWidth) {
					tip.x = mx - tip.width;
				}
				else {
					tip.x = mx;
				}
				if (my - tip.height < 0) {
					tip.y = my + tip.height;
				}
				else {
					tip.y = my - tip.height;
				}
			};
			var mouseyFun:Function = function (event:Event):void {
				if (tipTimer) {
					clearTimeout(tipTimer);
				}
				tip.visible = false;
				tipTimer = setTimeout(showTip, 750, stage.mouseX, stage.mouseY);
			};
			mousey.addEventListener(MouseEvent.MOUSE_OVER, mouseyFun);
			mousey.addEventListener(MouseEvent.MOUSE_MOVE, mouseyFun);
			mousey.addEventListener(MouseEvent.MOUSE_OUT, function(event:Event):void { clearTimeout(tipTimer); tip.visible = false; });						
			
		}
				
	}
}

