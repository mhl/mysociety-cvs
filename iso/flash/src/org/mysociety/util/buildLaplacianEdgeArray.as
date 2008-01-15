package org.mysociety.util
{
	public function buildLaplacianEdgeArray(v:int=1):Array
	{
/* 		return [ -1,  -1,  -1,  -1,  -1,
			     -1,  -1,  -1,  -1,  -1, 
			     -1,  -1,  24,  -1,  -1, 
			     -1,  -1,  -1,  -1,  -1, 
			     -1,  -1,  -1,  -1,  -1 ]; */
/* 		return [ -4,  -4,  -4,  -4,  -4,
			     -4,  -4,  -4,  -4,  -4, 
			     -4,  -4,  96,  -4,  -4, 
			     -4,  -4,  -4,  -4,  -4, 
			     -4,  -4,  -4,  -4,  -4 ]; */
/*   		return [ -v,  -v,  -v,  -v,  -v,
			     -v,  -v,  v*2,  -v,  -v, 
			     -v,  v*2, v*12, v*2,  -v, 
			     -v,  -v,  v*2,  -v,  -v, 
			     -v,  -v,  -v,  -v,  -v ]; */
			      
/*    		return [ 0,  v,  v,  v,  0,
			     v,  v,  2*v,  v,  v, 
			     v,  2*v, -v*24, 2*v,  v, 
			     v,  v,  2*v,  v,  v, 
			     0,  v,  v,  v,  0 ]; */
     		return [ -v,  -v,  -v,  -v,  -v,
			     -v,  -v,  -v,  -v,  -v, 
			     -v,  -v, v*24, -v,  -v, 
			     -v,  -v,  -v,  -v,  -v, 
			     -v,  -v,  -v,  -v,  -v ]; 

/*      		return [   0,  0,  -v/4,  0,  0,
				     0,  -v/4,  -v/2,  -v/4,  0, 
				     -v/4, -v/2, v*4, -v/2,  -v/4, 
				     0,  -v/4,  -v/2,  -v/4,  0, 
				     0,  0,  -v/4,  0,  0 ]; */ 

			      
/*  		return [ -v,  -v,  -v,  -v,
			     -v,  v*3, v*3, -v, 
			     -v,  v*3, v*3, -v, 
			     -v,  -v,  -v,  -v  ]; */			     
/*    		return [ -v,  -v,  -v,  
			     -v, v*8,  -v,  
			     -v,  -v,  -v ]; */
	}	
}