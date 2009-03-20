/*
 * vim:et sts=4 sw=4 cindent tw=120:
 * $Id: Color.as,v 1.1 2009-03-20 02:08:57 allens Exp $
 */

package com.stamen.graphics.color
{
    import com.stamen.graphics.color.IColor;

    public class Color extends Object
    {
        public static function zerofill(n:Number, len:int, base:uint=10):String
        {
            var nStr:String = n.toString(base);
            var nLen:int = nStr.length;
            while (nStr.length < len)
            {
                nStr = '0'.concat(nStr);
            }
            return nStr;
        }
        
        public static function compare(a:IColor, b:IColor):Boolean
        {
            return (a == b) || (!a && !b) || (a && a.equals(b));
        }
        
        protected function _blend(color:IColor, amount:Number):Array
        {
            var c1:Array = toArray();
            var c2:Array = color.toArray();
            var c3:Array = new Array();

            for (var i:Number = 0; i < c1.length; i++)
                c3[i] = c1[i] + (c2[i] - c1[i]) * amount;

            return c3;
        }

		public function get alpha():Number
		{
			return 1.0;
		}

		public function set alpha(alpha:Number):void
		{
		}

        public function equals(color:IColor):Boolean
        {
            return color && color.hex32 == hex32;
        }

        public function get hex32():uint
        {
            return 0xFF000000;
        }
        
        public function toArray():Array
        {
        	return [];
        }
    }
}
