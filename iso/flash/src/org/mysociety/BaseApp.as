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
 * @version $Id: BaseApp.as,v 1.2 2008-12-10 18:38:41 francis Exp $
 */
package org.mysociety
{
	import flash.display.Sprite;
	import flash.display.StageAlign;
	import flash.display.StageScaleMode;
	import flash.events.Event;
	import flash.events.HTTPStatusEvent;
	import flash.events.IOErrorEvent;
	import flash.events.ProgressEvent;
	import flash.events.SecurityErrorEvent;
	import flash.net.URLLoader;
	import flash.net.URLRequest;
	import flash.text.AntiAliasType;
	import flash.text.TextField;
	import flash.text.TextFormat;

	public class BaseApp extends Sprite
	{

// Tom Carden embedded Helvetica Neue, which I don't have, so I've aliased it to Bitstream - Francis.
		[Embed(systemFont="Bitstream Vera Sans", fontName="HelveticaNorm", mimeType='application/x-font')]
		public var helvetica:String;
		[Embed(systemFont="Bitstream Vera Sans", fontName="HelveticaBold", fontWeight="bold", mimeType='application/x-font')]
        public var helveticaBold:String;
//		[Embed(systemFont="Helvetica Neue", fontName="HelveticaNorm", mimeType='application/x-font')]
//		public var helvetica:String;
//		[Embed(systemFont="Helvetica Neue", fontName="HelveticaBold", fontWeight="bold", mimeType='application/x-font')]
//		public var helveticaBold:String;

		public var config:XML;

		public function BaseApp()
		{
			// so everything stays where we ask it to
			stage.align = StageAlign.TOP_LEFT;
			stage.scaleMode = StageScaleMode.NO_SCALE;

			var url:String = root.loaderInfo.parameters['configURL'];
			
			if (url) {
				var loader:URLLoader = new URLLoader(new URLRequest(url));
				loader.addEventListener(Event.COMPLETE, onConfigLoaded);
				loader.addEventListener(HTTPStatusEvent.HTTP_STATUS, function(event:Event):void { trace(event.toString()); });
				loader.addEventListener(IOErrorEvent.IO_ERROR, function(event:IOErrorEvent):void { error(event.text); });
				loader.addEventListener(SecurityErrorEvent.SECURITY_ERROR, function(event:SecurityErrorEvent):void { error(event.text); });
				loader.addEventListener(ProgressEvent.PROGRESS, function(event:ProgressEvent):void { progress('configuration', event); });
			}
			else {
				error("No configuration URL found, sorry!");
			}
		}
		
		private function onConfigLoaded(event:Event):void
		{
			config = XML((event.target as URLLoader).data);
			configReady(config);			
		}
		
		public function configReady(config:XML):void
		{
			error("override configReady in your subclass");
		}

		public function clearText():void
		{
			// clean up progress/errors
			if (getChildByName('progress')) {
				removeChild(getChildByName('progress'));
			}
			if (getChildByName('error')) {
				removeChild(getChildByName('error'));
			}
		}		
	
		public function error(text:String):void
		{
			var tf:TextField = getChildByName('error') as TextField; 
			if (!tf) {
				tf = new TextField();
				tf.name = 'error';
				tf.defaultTextFormat = new TextFormat("Helvetica", 14, 0x000000, true);
				tf.background = true;
				tf.backgroundColor = 0xffff00;
				tf.multiline = false;
				tf.wordWrap = false;
				addChild(tf);
			}
/* 			else {
				all.setChildIndex(tf, numChildren-1);
			} */
			tf.text = text;
			tf.width = Math.min(stage.stageWidth, tf.textWidth + 4);
			tf.height = tf.textHeight + 4;
		}


		public function progress(text:String, event:ProgressEvent):void
		{
			var tf:TextField = getChildByName('progress') as TextField; 
			if (!tf) {
				tf = new TextField();
				tf.name = 'progress';
				tf.defaultTextFormat = new TextFormat("Helvetica", 14, 0xffffff, true);
				tf.background = true;
				tf.backgroundColor = 0x404040;
				tf.multiline = false;
				tf.wordWrap = false;
				addChild(tf);
			}
/* 			else {
				if (all.getChildIndex(tf) != numChildren-1) {
					all.setChildIndex(tf, numChildren-1);
				}
			} */
			if (event.bytesTotal && event.bytesTotal > 0 && event.bytesLoaded > 0) {
				tf.text = 'loading ' + text + ': ' + Number(100*event.bytesLoaded/event.bytesTotal).toFixed(0) + '%';
			}
			else if (event.bytesLoaded > 0) {
				tf.text = 'loading ' + text + ': ' + Number(event.bytesLoaded/1000).toFixed(0) + "KB";
			}
			else {
				tf.text = 'loading ' + text + '...';
			}
			tf.width = Math.min(stage.stageWidth, tf.textWidth + 4);
			tf.height = tf.textHeight + 4;
			trace(tf.text);
		}		


		// Processing-style stateful text functions, because I'm tired of writing all these lines:
		
		protected var dtf:TextFormat = new TextFormat("HelveticaNorm", 11, 0x000000, false);
		
		protected function setTextFormat(font:String="HelveticaNorm", size:int=11, color:uint=0x000000, bold:Boolean=false, italic:Boolean=false, underline:Boolean=false, url:String=null, target:String=null, align:String=null):TextFormat
		{
			dtf = new TextFormat(font, size, color, bold, italic, underline, url, target, align);
			return dtf;
		}
		
		protected function getText(t:String, tx:Number=0, ty:Number=0, tw:Number=0, th:Number=0, multiline:Boolean=false):TextField
		{
			t = t.replace(/\\n/g, '\n');
			var tf:TextField = new TextField();
			tf.embedFonts = true;
			tf.antiAliasType = AntiAliasType.ADVANCED;
			tf.wordWrap = multiline;
			tf.multiline = multiline;
			tf.selectable = false;
			tf.mouseEnabled = false;
			if (multiline) {
				dtf.leading = Number(dtf.size) / 4;
			}
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
