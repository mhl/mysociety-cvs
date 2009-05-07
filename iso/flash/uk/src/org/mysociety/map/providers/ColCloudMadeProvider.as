package org.mysociety.map.providers
{
	import com.modestmaps.core.Coordinate;
	import com.modestmaps.mapproviders.OpenStreetMapProvider;
	
	public class ColCloudMadeProvider extends OpenStreetMapProvider
	{
		public var subdomains:Array = ['a.', 'b.', 'c.', ''];

		public function ColCloudMadeProvider()
		{
			super();
		}

		override public function getTileUrls(coord:Coordinate):Array
		{
			var worldSize:int = Math.pow(2, coord.zoom);
			if (coord.row < 0 || coord.row >= worldSize) {
				return [];
			}
			coord = sourceCoordinate(coord);
			var server:String = subdomains[int(coord.row + coord.column) % 4];
			var url:String = 'http://' + server + 'col.mysociety.org/cloudmade-tiles/' + [ coord.zoom, coord.column, coord.row ].join('/') + '.png'; 
			return [ url ];
		}

		override public function toString():String
		{
			return 'MS-CLOUDMADE';
		}
	}
}
