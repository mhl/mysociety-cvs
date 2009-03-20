/*
 * vim:et sts=4 sw=4 cindent:
 * $Id: RGBA.as,v 1.1 2009-03-20 02:08:57 allens Exp $
 */

package com.stamen.graphics.color
{
	import com.stamen.graphics.color.*;
	
	public class RGBA extends RGB
	{
		// 0 - 1
		protected var _alpha:Number = 1.0;
	
		public static function black(alpha:Number=1.0):RGBA
		{
			return RGBA.fromRGB(RGB.black(), alpha);
		}
	
		public static function white(alpha:Number=1.0):RGBA
		{
			return RGBA.fromRGB(RGB.white(), alpha);
		}
	
		public static function grey(lightness:Number, alpha:Number=1.0):RGBA
		{
			return RGBA.fromRGB(RGB.grey(lightness), alpha);
		}
	
		public static function random(alpha:Number=1.0):RGBA
		{
			var rgb:RGB = RGB.random();
			return RGBA.fromRGB(rgb, alpha);
		}

		public static function fromRGB(rgb:RGB, alpha:Number):RGBA
		{
			return new RGBA(rgb.red, rgb.green, rgb.blue, alpha);
		}
	
		public static function fromHex(hex:*):RGBA
		{
	        if (typeof hex == 'string') hex = parseInt(hex, 16);
	        else hex = Number(hex);
	
			var alpha:Number = (hex & 0xFF000000) >>> 24;
			hex = hex & 0x00FFFFFF;
			var rgb:RGB = RGB.fromHex(hex);
			return RGBA.fromRGB(rgb, alpha);
		}
	
		public function RGBA(red:Number=0, green:Number=0, blue:Number=0, alpha:Number=1.0)
		{
			super(red, green, blue);
			_alpha = alpha;
		}
	
	    override public function clone():IColor
	    {
	        return new RGBA(red, green, blue, _alpha);
	    }
	
	    override public function quantize(q:uint, f:Function=null):RGB
	    {
	        return super.quantize(q, f).toRGBA(alpha);
	    }
	    
	    override public function blend(color:IColor, amount:Number=0.5, asRGB:Boolean=false):IColor
	    {
	        if (asRGB)
	        {
                var parts:Array = _blend(color.toRGBA(), amount);
                return new RGBA(parts[0], parts[1], parts[2], parts[3]);
            }
            else
            {
                return super.blend(color, amount, false);
            }
	    }

		override public function get alpha():Number
		{
			return _alpha;
		}

		override public function set alpha(alpha:Number):void
		{
			_alpha = alpha;
		}

		public function get rgb():RGB
		{
			return new RGB(red, green, blue);
		}
	
		public function set rgb(rgb:RGB):void
		{
			red = rgb.red;
			green = rgb.green;
			blue = rgb.blue;
		}

        override public function toRGB():RGB
        {
            return rgb;
        }

        override public function toRGBA(alpha:Number=1.0):RGBA
        {
            return clone() as RGBA;
        }
        
		override public function toArray():Array
        {
            return [red, green, blue, alpha];
        }
	}
}