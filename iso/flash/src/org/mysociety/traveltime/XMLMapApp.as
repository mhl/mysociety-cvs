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
 * @version $Id: XMLMapApp.as,v 1.2 2008-12-10 18:38:42 francis Exp $
 */
package org.mysociety.traveltime
{
	
	import flash.display.Bitmap;
	import flash.display.BlendMode;
	import flash.display.Loader;
	import flash.display.Shape;
	import flash.display.Sprite;
	import flash.events.Event;
	import flash.events.HTTPStatusEvent;
	import flash.events.IOErrorEvent;
	import flash.events.ProgressEvent;
	import flash.events.SecurityErrorEvent;
	import flash.events.MouseEvent;
	import flash.external.ExternalInterface;
	import flash.filters.ColorMatrixFilter;
	import flash.filters.GlowFilter;
	import flash.geom.ColorTransform;
	import flash.geom.Rectangle;
	import flash.net.URLRequest;
	import flash.net.URLLoader;
	import flash.net.URLLoaderDataFormat;
	import flash.text.AntiAliasType;
	import flash.text.TextField;
	import flash.text.TextFormat;
	import flash.text.TextFormatAlign;
    import flash.utils.ByteArray;
    import flash.xml.XMLNode;
	
	import org.mysociety.BaseApp;
	import org.mysociety.util.buildDesaturateArray;

	public class XMLMapApp extends BaseApp
	{

		public var map:Loader;
		public var overlayLoaders:Array = [];

		public var pointDetailsLoader:URLLoader;
		public var pointDetails:XML;
		
		// for setting label ranges from query strings
		public var slidersByOverlay:Object = {};

        public var francisDebug:String = 'initial';
				
		override public function configReady(config:XML):void
		{
			if (config && config.mapURL.length() > 0 && config.overlay.length() > 0 && config.labelURL.length() > 0) {
				map = new Loader();
				map.load(new URLRequest(config.mapURL.text()));
				map.contentLoaderInfo.addEventListener(Event.COMPLETE, onMapLoaded);
				map.contentLoaderInfo.addEventListener(ProgressEvent.PROGRESS, function (event:ProgressEvent):void { progress('map', event); });
				map.contentLoaderInfo.addEventListener(HTTPStatusEvent.HTTP_STATUS, function(event:Event):void { trace(event.toString()); });
				map.contentLoaderInfo.addEventListener(IOErrorEvent.IO_ERROR, function(event:IOErrorEvent):void { error(event.text); });
				map.contentLoaderInfo.addEventListener(SecurityErrorEvent.SECURITY_ERROR, function(event:SecurityErrorEvent):void { error(event.text); });
			}
			else {
				error("Configuration file incomplete, sorry!");
			}
		}

		private function onMapLoaded(event:Event):void
		{
			// keep loading overlays until we've got them all
			if (overlayLoaders.length < config.overlay.length()) {
				var overlay:Loader = new Loader();
				var url:String = config.overlay[overlayLoaders.length].@url;
				overlay.load(new URLRequest(url));
				overlay.contentLoaderInfo.addEventListener(Event.COMPLETE, onMapLoaded);
				overlay.contentLoaderInfo.addEventListener(ProgressEvent.PROGRESS, function (event:ProgressEvent):void { progress('overlays', event); });
				overlay.contentLoaderInfo.addEventListener(HTTPStatusEvent.HTTP_STATUS, function(event:Event):void { trace(event.toString()); });
				overlay.contentLoaderInfo.addEventListener(IOErrorEvent.IO_ERROR, function(event:IOErrorEvent):void { error(event.text); });
				overlay.contentLoaderInfo.addEventListener(SecurityErrorEvent.SECURITY_ERROR, function(event:SecurityErrorEvent):void { error(event.text); });
				overlayLoaders.push(overlay);
			}
			else {
                if (config.pointDetailsURL.length() > 0) {
                    pointDetailsLoader = new URLLoader(new URLRequest(config.pointDetailsURL.text()));
                    pointDetailsLoader.dataFormat = URLLoaderDataFormat.BINARY;
                    pointDetailsLoader.addEventListener(Event.COMPLETE, onPointDetailsLoaded);
                    pointDetailsLoader.addEventListener(HTTPStatusEvent.HTTP_STATUS, function(event:Event):void { trace(event.toString()); });
                    pointDetailsLoader.addEventListener(IOErrorEvent.IO_ERROR, function(event:IOErrorEvent):void { error(event.text); });
                    pointDetailsLoader.addEventListener(SecurityErrorEvent.SECURITY_ERROR, function(event:SecurityErrorEvent):void { error(event.text); });
                    pointDetailsLoader.addEventListener(ProgressEvent.PROGRESS, function(event:ProgressEvent):void { progress('pointDetails', event); });
                } else {
                    cleanUpProgressErrors();
                }
			}
		}		

		private function onPointDetailsLoaded(event:Event):void {
            francisDebug = 'onPointDetailsLoaded';

            var ba:ByteArray = pointDetailsLoader.data;

   /*         for (var i:int = 100000; i < 100100; i++) {
                //francisDebug = francisDebug + ba[i];
            }

			pointDetails = XML((event.target as URLLoader).data);
            var x:XMLNode = pointDetails.elements()[0];
            for (var j:int = 0; j < 100; j++) {
                francisDebug = francisDebug + x.toString();
                x = x.nextSibling;
            }
            */

            //for (var i:int = 0; i < pointDetails.point.length(); i++) {
        //    var pe:ProgressEvent = new ProgressEvent('pointDetails');
         //   for (var i:int = 0; i < 100; i++) {
          //      francisDebug = pointDetails.point[i].@name;
           // }
            //tipLabel.appendText(pointDetails.point[0].@name);


            cleanUpProgressErrors();
        }

        private function cleanUpProgressErrors():void {
            // clean up progress/errors
            if (getChildByName('progress')) {
                removeChild(getChildByName('progress'));
            }
            if (getChildByName('error')) {
                removeChild(getChildByName('error'));
            }
            draw();
        }
		
		private function draw():void
		{
			var ui:Sprite = new Sprite();
			addChild(ui);

			var all:Sprite = new Sprite();
			// all.y gets set at the end to leave room for ui
			addChild(all);			

			all.addChild(map);
			map.content.filters = [ new ColorMatrixFilter(buildDesaturateArray()) ];
			
			var sliders:Array = [];
			var overlays:Array = [];

			// loop variables, oh how scoping is strange in AS3
			var slider:Slider;
			var overlay:Overlay;
				
			// make a grid of sliders, basically all we'll ever see is two columns but you never know
			var sliderX:Number = 0;
			var sliderY:Number = 0;
			var sliderBounds:Rectangle = map.getBounds(this);
			if (config.overlay.length() > 1) {
				sliderBounds.width = sliderBounds.width/2;
			}
			for each (var oxml:XML in config.overlay) {
				overlay = new Overlay(overlayLoaders.shift(), oxml.@name, oxml.@greyOfMin, oxml.@greyOfMax, parseInt(oxml.@belowColor,16), parseInt(oxml.@aboveColor,16));
				slider = new Slider(sliderBounds, oxml.@descriptionText, oxml.@sliderLabel, oxml.@sliderMin, oxml.@sliderMax, oxml.@sliderPrecision);
				slidersByOverlay[overlay.name] = slider;
				ui.addChild(slider);	
				slider.x = sliderX;
				slider.y = sliderY;
				overlaySliderGlue(overlay, slider);
				if (sliderX > 0) {
					sliderX = 0;
					sliderY += slider.height + 10;
				}
				else {
					sliderX += sliderBounds.width;
				}
				sliders.push(slider);
				overlays.push(overlay);
			}
			
			//////////////////////

			var hash:String = ExternalInterface.call('eval', 'location.hash').toString();
			if (hash) {
				var querys:Array = hash.slice(1).replace(/amp;/g,'').split('&'); 
				for each (var query:String in querys) {
					var parts:Array = query.split('=');
					slider = slidersByOverlay[parts[0]] as Slider;
					if (slider) {
						var range:Array = parts[1].split(":");
						if (range.length == 2) {
							var smin:Number = parseFloat(range[0]);
							var smax:Number = parseFloat(range[1]);							
							if (!isNaN(smin) && !isNaN(smax)) {
								slider.setLabelRange(smin, smax);
							}
						}
					}
				}
			}

			for each (slider in sliders) {
				slider.addEventListener(Slider.DONE_CHANGING, updateHash);
			}
			updateHash(null);
			
			//////////////////////
			
			var layerSources:Array = [];
			var layerColors:Array = [];
			for each (overlay in overlays) {
				layerSources = layerSources.concat( [ overlay.aboveMask, overlay.belowMask ] );
				layerColors = layerColors.concat( [ overlay.aboveColor, overlay.belowColor ] );
			}
			for each (var layerSource:Bitmap in layerSources) {				
				var layer:Sprite = new Sprite();
				layer.blendMode = BlendMode.MULTIPLY;
				layer.cacheAsBitmap = true;
				all.addChild(layer);
				
				var layerMask:Sprite = new Sprite();
				layerMask.cacheAsBitmap = true;
				layerMask.addChild(layerSource);
				all.addChild(layerMask);
				
				var colorFill:Shape = new Shape();			
				colorFill.graphics.beginFill(layerColors.shift());
				colorFill.graphics.drawRect(0, 0, map.width, map.height);
				layer.addChild(colorFill);
				
				layer.mask = layerMask;
			}

			////////////////////
			
            if (config.labelURL.length() > 1) {
                var labels:Loader = new Loader();
                labels.load(new URLRequest(config.labelURL.text()));
                labels.transform.colorTransform = new ColorTransform(-1,-1,-1,1,255,255,255,0);
                all.addChild(labels);
            }

			////////////////////
			
			var bitmaps:Array = [];
			for each (overlay in overlays) {
				bitmaps = bitmaps.concat( [ overlay.aboveMask, overlay.belowMask ] );
			}
			var intersection:Intersection = new Intersection(bitmaps);
			all.addChild(intersection);

			var maskedMap:Bitmap = new Bitmap((map.content as Bitmap).bitmapData);			
			maskedMap.mask = intersection;
			maskedMap.filters = [ new GlowFilter(0xffffff00, 1, 6, 6, 5, 1, true, false) ];
			all.addChild(maskedMap);

			for each (slider in sliders) {
				slider.addEventListener(Slider.RANGE_CHANGED, intersection.intersect);
			}
			
			///////////////////
			
			var niceLabel:TextField = new TextField();
			niceLabel.embedFonts = true;
			niceLabel.antiAliasType = AntiAliasType.ADVANCED;
			niceLabel.defaultTextFormat = new TextFormat("HelveticaBold", 10 + (2*stage.stageWidth/400), 0x000000, true, null, false, null, null, TextFormatAlign.CENTER, 5, 5, null, 4);
			niceLabel.multiline = false;
			niceLabel.wordWrap = false;
			var drawNiceLabel:Function = function(event:Event=null):void {
				niceLabel.text = "Areas " + (sliders[0] as Slider).getDescription();
				for each (var s:Slider in sliders.slice(1)) {
					niceLabel.appendText("\n" + s.getDescription());
				}
				niceLabel.width = stage.stageWidth-4;
				niceLabel.height = niceLabel.textHeight + 4;								 							    
			};
			drawNiceLabel();			
			niceLabel.x = 2;
			niceLabel.y = 4;
			addChild(niceLabel);
						
			for each (slider in sliders) {
				slider.addEventListener(Slider.RANGE_CHANGED, drawNiceLabel);
			}

			//////////////////

			ui.y = niceLabel.y + niceLabel.height + 4;
			
			var rect:Rectangle = ui.getBounds(this);
//			graphics.beginFill(0xffffc0); // Tom S doesn't like yellow :(
			graphics.beginFill(0xf0f0ff);
			graphics.drawRect(0,0,stage.stageWidth, rect.y + rect.height + 10);
			graphics.endFill();
			graphics.lineStyle(2, 0x804000, 0.3);
			graphics.moveTo(0, rect.y + rect.height + 9);
			graphics.lineTo(stage.stageWidth, rect.y + rect.height + 9);
			
 			all.y = rect.y + rect.height + 10;
 			trace('all y', all.y);

/* 			for each (overlay in overlays) {
				var b:Bitmap = new Bitmap(overlay.originalData);
				b.alpha = 0.5;
				all.addChild(b);
				all.addEventListener(MouseEvent.MOUSE_MOVE, function(event:MouseEvent):void {
					var color:uint = b.bitmapData.getPixel(event.localX, event.localY);
					trace(event.localX, event.localY, color & 0x000000ff); 
				});
			} */

			/////////////////

			if (config.centerLabel.length() > 0) {

				var center:Sprite = new Sprite();
				center.graphics.beginFill(0xff0000,0);
				center.graphics.drawRect(-6,-6,12,12);
				center.graphics.beginFill(0xaa0000);
				center.graphics.lineStyle(1,0xffffff,1,true);
				center.graphics.drawRect(-3,-3,6,6);
				center.x = map.width/2;
				center.y = map.height/2;
				all.addChild(center);

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
				centerTextBack.x = centerOffX + 3 + map.width / 2;
				centerTextBack.y = centerOffY - ((centerText.y+centerText.height+3)/2) + (map.height / 2);

				var centerTextBorder:uint = 0x800000;
				setTextFormat("HelveticaNorm", (stage.stageWidth > 500) ? 14 : 12, centerTextBorder, false);
				
				var borders:Sprite = new Sprite();
				
 				for (var offsetX:int = -2; offsetX <= 2; offsetX += 1) {
	 				for (var offsetY:int = -2; offsetY <= 2; offsetY += 1) {
						var borderText:TextField = getText(config.centerLabel[0].text(), 5+offsetX, 5+offsetY);
						borders.addChild(borderText);
					}
				}
				centerTextBack.addChild(borders);

				all.addChild(centerTextBack);
				centerTextBack.addChild(centerText);
				
/* 				var centerTimer:uint = setTimeout(function():void { centerTextBack.visible = false }, 2000);
				
				centerTextBack.mouseEnabled = false;
				
 				center.useHandCursor = center.buttonMode = center.mouseEnabled = true;
				center.addEventListener(MouseEvent.MOUSE_OVER, function(event:MouseEvent):void { clearTimeout(centerTimer); centerTextBack.visible = true; });
				center.addEventListener(MouseEvent.MOUSE_OUT, function(event:MouseEvent):void { centerTimer = setTimeout(function():void { centerTextBack.visible = false }, 750); }); */ 
			}
		
			/////////////////
			var tipLabel:TextField = new TextField();
			tipLabel.embedFonts = true;
			tipLabel.antiAliasType = AntiAliasType.ADVANCED;
			tipLabel.defaultTextFormat = new TextFormat("HelveticaBold", 10 + (2*stage.stageWidth/400), 0x000000, true, null, false, null, null, TextFormatAlign.CENTER, 5, 5, null, 4);
			tipLabel.multiline = false;
			tipLabel.wordWrap = true;
			var drawtipLabel:Function = function(event:MouseEvent=null):void {
                if (event) {
                    tipLabel.text = "labelURL: " + config.labelURL.length() + "  X: " + event.localX + " Y:" + event.localY + " f:" + francisDebug + " ";
                    
                    //for (var i:int = 0; i < pointDetails.point.length(); i++) {
                    //for (var i:int = 0; i < 10; i++) {
                    //  tipLabel.appendText(pointDetails.point[i].@name);
                    //}
                    //tipLabel.appendText(pointDetails.point[0].@name);

                    tipLabel.width = stage.stageWidth-4;
                    tipLabel.height = (tipLabel.textHeight + 4) * 2;
                }
			};
			drawtipLabel();			
			tipLabel.x = 2;
			tipLabel.y = stage.stageHeight - 25 - 25 - 25;
			addChild(tipLabel);
			stage.addEventListener(MouseEvent.MOUSE_MOVE, drawtipLabel);			
        }
		
		private function updateHash(event:Event):void
		{
			var hash:String = "";
			for (var overlayName:String in slidersByOverlay) {
				if (hash != "") hash += "&";
				var slider:Slider = slidersByOverlay[overlayName] as Slider;
				hash += overlayName + "=" + slider.getLabelRange().join(":");
			}
			if (hash != "") {
				ExternalInterface.call('setHash', hash);
			}
		}
		
		/** this is in its own function so that the closure scope is correct 
		 * (doing this inside a loop where overlay and slider were modified messed things up) */
		private function overlaySliderGlue(overlay:Overlay, slider:Slider):void
		{
			slider.aboveColor = overlay.aboveColor;
			slider.belowColor = overlay.belowColor;				
			slider.addEventListener(Slider.RANGE_CHANGED, function(event:Event):void {
				overlay.setRange(slider.getRange());
			});
			overlay.setRange(slider.getRange());
		}
		
				
	}
}
