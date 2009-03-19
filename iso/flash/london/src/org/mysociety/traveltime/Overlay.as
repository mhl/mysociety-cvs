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
 * @version $Id: Overlay.as,v 1.1 2009-03-19 20:05:07 allens Exp $
 */
 package org.mysociety.traveltime
{
	import flash.display.Bitmap;
	import flash.display.BitmapData;
	import flash.display.Loader;
	import flash.geom.Point;
	import flash.geom.Rectangle;
	import flash.utils.Dictionary;
	
	public class Overlay
	{	
		public var name:String;
		
		public var originalData:BitmapData;
		
 		public var belowMask:Bitmap;
		public var aboveMask:Bitmap; 
		
		private var minGrey:uint;
		private var maxGrey:uint;
		
		public var belowColor:uint;
		public var aboveColor:uint;

		// debugging
/* 		private var mapped:Dictionary = new Dictionary(true);
		private var reverseMapped:Dictionary = new Dictionary(true);
		private var mapKeys:Array = []; */
		
		/**
		 * greyOfMin and greyOfMax are the (8-bit) grey pixel values of 
		 * the minimum and maximum data value represented in the given image.
		 * 
		 * When the image loads then the pixels may be changed such that 
		 * minGrey and maxGrey are in the correct order (simplifying the 
		 * rest of the code, I hope). 
		 */
		public function Overlay(loader:Loader, name:String, greyOfMin:uint, greyOfMax:uint, belowColor:uint=0x593737, aboveColor:uint=0xff593737)
		{
			
			this.name = name;
			
			// !!! these may switch when the image is loaded...		
			this.minGrey = greyOfMin;
			this.maxGrey = greyOfMax;

			this.aboveColor = aboveColor;
			this.belowColor = belowColor;

			var bm:Bitmap = loader.content as Bitmap;
			originalData = bm.bitmapData.clone();


			// transform images that are the 'wrong' way around:
			// e.g. 255 to 55 --> 0 to 200
			//originalData.lock();	
			if (maxGrey < minGrey) {
				for (var i:int = 0; i < originalData.width; i++) {
					for (var j:int = 0; j < originalData.width; j++) {
						var color:uint = originalData.getPixel(i,j);
						// e.g. 255
						var grey:uint = color & 0x000000ff;
						var saved:uint = grey;
						if (grey != 0) {
							// e.g. 255 - 55 = 200
							// e.g. 255 - 255 = 0
							grey = minGrey - grey;
/* 							if (!mapped[saved]) {
								mapKeys.push(saved);
								mapped[saved] = grey;
								reverseMapped[grey] = saved;
							} */
							color = 0xff000000 | grey << 16 | grey << 8 | grey;
							originalData.setPixel(i,j,color);
						}
					}
				}
				var temp:uint = maxGrey; // e.g. 55
				maxGrey = minGrey; // e.g. 255
				minGrey = temp;    // e.g. 55
				maxGrey -= minGrey; // e.g. 200
				minGrey = 0;
			}
			//originalData.unlock();
	
/* 			mapKeys.sort(Array.NUMERIC);
			for each (var key:uint in mapKeys) {
				trace(key + " --> " + mapped[key]);
			}
			trace("minGrey: " + minGrey);
			trace("maxGrey: " + maxGrey); */
	
 			belowMask = new Bitmap(new BitmapData(bm.width, bm.height, true, 0x00000000));
			aboveMask = new Bitmap(new BitmapData(bm.width, bm.height, true, 0x00000000));
		}
		
		
		/** takes range between 0 and 1 and scales between minGrey and maxGrey
		 * before calling threshold() */
		public function setRange(range:Array):void
		{
			var lower:Number = range[0];
			var upper:Number = range[1];
			
			lower *= Number(maxGrey - minGrey);
			upper *= Number(maxGrey - minGrey);
			
			lower += minGrey;
			upper += minGrey;
			
			threshold(lower, upper);		
		}
		
		public function threshold(luint:uint=0x00, uuint:uint=0xff):void
		{
//			trace(luint + " to " + uuint + " --> " + reverseMapped[luint] + " to " + reverseMapped[uuint]);
			
			// set all pixels in below/above overlays to this color
	 		var clearColor:uint = 0x00000000;
	
			// perform thresholding using this opertation
	 		var aboveOp:String = '>';
	 		var belowOp:String = '<';
				
			/* we use this mask to pick out the grey value
			 * 
			 * (it's private because if we change it then we need to
			 * modify the threshold function below to take 32 bit values
			 * instead of 8 bit greys) 
			 */
			var aboveBitMask:uint = 0x000000ff;
			var belowBitMask:uint = 0x000000ff;
			
			// clear masks (TODO: quicker call?)		
			aboveMask.bitmapData.fillRect(new Rectangle(0,0,aboveMask.bitmapData.width,aboveMask.bitmapData.height), clearColor);
	 		belowMask.bitmapData.fillRect(new Rectangle(0,0,belowMask.bitmapData.width,belowMask.bitmapData.height), clearColor);

			var bitmapData:BitmapData = aboveMask.bitmapData;
			// if originalData pixel is above uuint, set aboveMask to red (or aboveColor)
 	  		bitmapData.threshold(originalData,
								   new Rectangle(0,0,originalData.width,originalData.height),
								   new Point(),
								   aboveOp,
								   uuint,
								   aboveColor, 
								   aboveBitMask, 
								   false);
			  
			bitmapData = belowMask.bitmapData;
			// if originalData pixel is below luint, set aboveMask to red (or belowColor)
	  		bitmapData.threshold(originalData,
								   new Rectangle(0,0,originalData.width,originalData.height),
								   new Point(),
								   belowOp,
								   luint, 
								   belowColor, 
								   belowBitMask, 
								   false);			
		} 
		
	}
	

}