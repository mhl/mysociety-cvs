package com.stamen.utils
{
	public class MathUtils
	{
	    public static function random(min:Number, max:Number):Number
	    {
	        return min + Math.random() * (max - min);
	    }

	    public static function bound(value:Number, min:Number, max:Number):Number
	    {
	        if (!isFinite(value)) value = 0;
	        return Math.min(max, Math.max(min, value));
	    }

	    public static function normalize(value:Number, min:Number, max:Number, bound:Boolean=false):Number
	    {
	        if (bound)
	            value = MathUtils.bound(value, min, max);
	        return (value - min) / (max - min);
	    }

        public static function quantize(value:Number, divisor:Number, f:Function=null):Number
        {
            if (f == null) f = Math.floor;
            return f(value / divisor) * divisor;
        }
        
        public static function map(value:Number, minA:Number, maxA:Number, minB:Number, maxB:Number, bound:Boolean=false):Number
        {
            return minB + (maxB - minB) * normalize(value, minA, maxA, bound);
        }
	}
}
