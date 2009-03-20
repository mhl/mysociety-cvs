/*
 * vim:et sts=4 sw=4 cindent:
 * $Id: HSVA.as,v 1.1 2009-03-20 02:08:57 allens Exp $
 */

package com.stamen.graphics.color
{
	import com.stamen.graphics.color.*;
	
	public class HSVA extends HSV
	{
		// 0 - 1
		protected var _alpha:Number = 1.0;
	
		public static function black(alpha:Number=1):HSVA
		{
			return HSVA.fromHSV(HSV.black(), alpha);
		}
	
		public static function white(alpha:Number=1):HSVA
		{
			return HSVA.fromHSV(HSV.white(), alpha);
		}
	
		public static function grey(lightness:Number, alpha:Number=1):HSVA
		{
			return HSVA.fromHSV(HSV.grey(lightness), alpha);
		}
	
		public static function random(alpha:Number=1):HSVA
		{
			var hsv:HSV = HSV.random();
			return HSVA.fromHSV(hsv, alpha);
		}

		public static function fromHSV(hsv:HSV, alpha:Number=1):HSVA
		{
			return new HSVA(hsv.hue, hsv.sat, hsv.value, alpha);
		}

		public static function fromHex(hex:*):HSVA
		{
            var rgba:RGBA = RGBA.fromHex(hex);
            return HSVA.fromHSV(rgba.rgb.toHSV(), rgba.alpha); 
		}
	
		public function HSVA(hue:Number=0, sat:Number=0, value:Number=0, alpha:Number=1.0)
		{
			super(hue, sat, value);
			_alpha = alpha;
		}
	
	    override public function clone():IColor
	    {
	        return new HSVA(hue, sat, value, _alpha);
	    }
	
	    override public function blend(color:IColor, amount:Number=0.5, asHSV:Boolean=false):IColor
	    {
            var parts:Array = _blend(color.toHSVA(), amount);
            return new HSVA(parts[0], parts[1], parts[2], parts[3]);
	    }

		override public function get alpha():Number
		{
			return _alpha;
		}

		override public function set alpha(alpha:Number):void
		{
			_alpha = alpha;
		}

		public function get hsv():HSV
		{
			return new HSV(hue, sat, value);
		}
	
		public function set hsv(hsv:HSV):void
		{
			hue = hsv.hue;
			sat = hsv.sat;
			value = hsv.value;
		}
	}	
}

