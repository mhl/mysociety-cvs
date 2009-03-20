/*
 * $Id: LinearProjection.as,v 1.1 2009-03-20 02:08:56 allens Exp $
 */

package com.modestmaps.geo
{
	import flash.geom.Point;
	import com.modestmaps.geo.Transformation;
	import com.modestmaps.geo.AbstractProjection; 
	 
	public class LinearProjection extends AbstractProjection
	{
	    function LinearProjection(zoom:Number, T:Transformation)
	    {
	        super(zoom, T);
	    }
	    
	   /*
	    * String signature of the current projection.
	    */
	    override public function toString():String
	    {
	        return 'Linear('+zoom+', '+T.toString()+')';
	    }
	    
	   /*
	    * Return raw projected point.
	    */
	    override protected function rawProject(point:Point):Point
	    {
	        return new Point(point.x, point.y);
	    }
	    
	   /*
	    * Return raw unprojected point.
	    */
	    override protected function rawUnproject(point:Point):Point
	    {
	        return new Point(point.x, point.y);
	    }
	}
}