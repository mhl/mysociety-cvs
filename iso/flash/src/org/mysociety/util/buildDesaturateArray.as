
package org.mysociety.util
{
	public function buildDesaturateArray(s:Number=0):Array
	{
		var rwgt:Number = 0.3086;
		var gwgt:Number = 0.6094;
		var bwgt:Number = 0.0820;
		var ca:Number = (1.0-s)*rwgt + s;
		var cb:Number = (1.0-s)*rwgt;
		var cc:Number = (1.0-s)*rwgt;
		var cd:Number = (1.0-s)*gwgt;
		var ce:Number = (1.0-s)*gwgt + s;
		var cf:Number = (1.0-s)*gwgt;
		var cg:Number = (1.0-s)*bwgt;
		var ch:Number = (1.0-s)*bwgt;
		var ci:Number = (1.0-s)*bwgt + s;
		return [
		    ca,     cd,     cg,      0.0,	0.0,
	        cb,     ce,     ch,      0.0,	0.0,
    		cc,     cf,     ci,      0.0,	0.0,
	        0.0,    0.0,    0.0,     1.0,	0.0,
		];
	}	
}
