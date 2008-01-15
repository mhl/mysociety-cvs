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
 * @version $Id: Intersection.as,v 1.1 2008-01-15 03:01:01 tcarden Exp $
 */
package org.mysociety.traveltime
{
	import flash.display.Bitmap;
	import flash.display.BitmapData;
	import flash.display.Sprite;
	import flash.events.Event;
	import flash.geom.Point;
	import flash.geom.Rectangle;
	
	/** takes the given array of bitmaps and (whenever intersect is called) 
	 * makes itself white where they are transparent and transparent where they are opaque 
	 * (technically I suspect this isn't an intersection, but a NOT) */
	public class Intersection extends Sprite
	{
		private var intersection:Bitmap;
		private var bitmaps:Array;
		
		public function Intersection(bitmaps:Array)
		{
			this.bitmaps = bitmaps;
			var bm1:Bitmap = bitmaps[0] as Bitmap;
			intersection = new Bitmap(new BitmapData(bm1.width, bm1.height, true, 0xffffffff));
			addChild(intersection);
			cacheAsBitmap = true; // seems to be needed to use this as a mask, infuriatingly
			intersect();
		}

		public function intersect(event:Event=null):void
		{		
			//trace('intersecting');
			var area:Rectangle = new Rectangle(0,0,intersection.width,intersection.height);
	 		intersection.bitmapData.fillRect(area, 0xffffffff);
			for each (var bitmap:Bitmap in bitmaps) {
				intersection.bitmapData.threshold(bitmap.bitmapData, area, new Point(), '==', 0xff000000, 0x00000000, 0xff000000, false);
			}
		}									   
		
	}
}