/*
 * vim:et sts=4 sw=4 cindent:
 * $Id: IColor.as,v 1.1 2009-03-20 02:08:57 allens Exp $
 */

package com.stamen.graphics.color
{
	import com.stamen.graphics.color.*;

	public interface IColor
	{
	    function clone():IColor;
        function equals(color:IColor):Boolean;

	    function toHex(withAlpha:Boolean=false):uint;
	    function toArray():Array;
	    function toRGB():RGB;
	    function toRGBA(alpha:Number=1):RGBA;
	    function toHSV():HSV;
	    function toHSVA(alpha:Number=1):HSVA;
	    function toString():String;

	    function blend(color:IColor, amount:Number=0.5, asRGB:Boolean=false):IColor;
	    
        function get hex():uint;
        function get hex32():uint;
	    function get alpha():Number;
	    function set alpha(alpha:Number):void;
	}
}
