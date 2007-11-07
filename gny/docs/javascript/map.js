//dirty global vars
var map;
var iBuffer_height = 0.1
var iBuffer_width = 0.26

var iBuffer_mini_height = 0.2
var iBuffer_mini_width = 0.2

// A Rectangle is a simple overlay that outlines a lat/lng bounds on the
// map. It has a border of the given weight and color and can optionally
// have a semi-transparent background color.
function Rectangle(bounds, opt_weight, opt_color) {
  this.bounds_ = bounds;
  this.weight_ = opt_weight || 5;
  this.color_ = opt_color || '#EF2C2C';
}
Rectangle.prototype = new GOverlay();

// Creates the DIV representing this rectangle.
Rectangle.prototype.initialize = function(map) {
  // Create the DIV representing our rectangle
  var div = document.createElement("div");
  div.style.border = this.weight_ + "px solid " + this.color_;
  div.style.position = "absolute";

  // Our rectangle is flat against the map, so we add our selves to the
  // MAP_PANE pane, which is at the same z-index as the map itself (i.e.,
  // below the marker shadows)
  map.getPane(G_MAP_MAP_PANE).appendChild(div);
  this.map_ = map;
  this.div_ = div;
}

// Remove the main DIV from the map pane
Rectangle.prototype.remove = function() {
  this.div_.parentNode.removeChild(this.div_);
}

// Copy our data to a new Rectangle
Rectangle.prototype.copy = function() {
  return new Rectangle(this.bounds_, this.weight_, this.color_,
                       this.backgroundColor_, this.opacity_);
}

// Redraw the rectangle based on the current projection and zoom level
Rectangle.prototype.redraw = function(force) {
  // We only need to redraw if the coordinate system has changed
  if (!force) return;

  // Calculate the DIV coordinates of two opposite corners of our bounds to
  // get the size and position of our rectangle
  var c1 = this.map_.fromLatLngToDivPixel(this.bounds_.getSouthWest());
  var c2 = this.map_.fromLatLngToDivPixel(this.bounds_.getNorthEast());

  // Now position our DIV based on the DIV coordinates of our bounds
  this.div_.style.width = Math.abs(c2.x - c1.x) + "px";
  this.div_.style.height = Math.abs(c2.y - c1.y) + "px";
  this.div_.style.left = (Math.min(c2.x, c1.x) - this.weight_) + "px";
  this.div_.style.top = (Math.min(c2.y, c1.y) - this.weight_) + "px";
}

function addRectangle(){

	//get the map's bounds
	oBounds = map.getBounds();
	oSouthWestPoint = oBounds.getSouthWest();
	oNorthEastPoint = oBounds.getNorthEast();	

	if(get('hidMiniMap').value == 1){
		iWidthBuffer = ((oSouthWestPoint.x - oNorthEastPoint.x) * -1) * iBuffer_mini_width;
		iHeightBuffer = ((oSouthWestPoint.y - oNorthEastPoint.y) * -1) * iBuffer_mini_height;
	}else{
		iWidthBuffer = ((oSouthWestPoint.x - oNorthEastPoint.x) * -1) * iBuffer_width;
		iHeightBuffer = ((oSouthWestPoint.y - oNorthEastPoint.y) * -1) * iBuffer_height;		
	}	

	iSouthWestY = oSouthWestPoint.y + iHeightBuffer;
	iSouthWestX = oSouthWestPoint.x + iWidthBuffer;	
	iNorthEastY = oNorthEastPoint.y - iHeightBuffer
	iNorthEastX = oNorthEastPoint.x - iWidthBuffer

    rectBounds = new GLatLngBounds(
        new GLatLng(iSouthWestY, iSouthWestX),
        new GLatLng(iNorthEastY, iNorthEastX));

	//clear any existing rectangles
	map.clearOverlays();
	
	//add the new one						
    map.addOverlay(new Rectangle(rectBounds));

	//save data
	if(get('hidSaveMapData').value == 1){
		get('hidLongBottomLeft').value =  iSouthWestX
		get('hidLatBottomLeft').value = iSouthWestY
		get('hidLongTopRight').value = iNorthEastX
		get('hidLatTopRight').value = iNorthEastY
		get('hidZoomLevel').value = map.getZoom();	

		oCenter = map.getCenter();
		get('hidLatCentroid').value = oCenter.lat();
		get('hidLongCentroid').value = oCenter.lng();
	}

}

function load(nCenterLong, nCenterLat, iZoom, bFullMap) {
  if (GBrowserIsCompatible()) {

    map = new GMap2(document.getElementById("divMap"));
    map.setCenter(new GLatLng(nCenterLat, nCenterLong), iZoom);

	if(get('hidMiniMap').value == 0){
	    map.addControl(new GLargeMapControl());
	}else{
		map.disableDragging();
	}

	//add default rectangle
	addRectangle();
	
	//redraw rectangle on zoom etc
	GEvent.addListener(map, 'zoomend', addRectangle);
	GEvent.addListener(map, 'dragstart', function(){map.clearOverlays();});		
	GEvent.addListener(map, 'dragend', addRectangle);	
	GEvent.addListener(map, 'movestart', function(){map.clearOverlays();});		
	GEvent.addListener(map, 'moveend', addRectangle);	
	
  }
}

function searchMap(){
	
	sSearch = get('txtSearchMap').value;
	if(sSearch != ''){
		
		//hide any warnings
		hideWarning();
		setControlWarning(get('txtSearchMap'), false);		
		
		//show spinny thing
		get('btnMapSearch').style.display = "none";
		get('imgMapLoading').style.display = "inline";
		
		var geocoder = new GClientGeocoder();
		geocoder.getLatLng(sSearch, searchmapCallback);
	}else{
		showWarning('Please enter a location');
		setControlWarning(get('txtSearchMap'), true);		
		setFocus('txtSearchMap');		
	}
	
}

function searchmapCallback(oResponse){

	get('btnMapSearch').style.display = "inline";
	get('imgMapLoading').style.display = "none";
	
	if (oResponse) {
		map.setCenter(oResponse, 13);
	}else{
		showWarning('Sorry, we couldent find any results for <em>' + get('txtSearchMap').value + '</em>');
		setControlWarning(get('txtSearchMap'), true);
		setFocus('txtSearchMap');
	}
}

function submitMapSearch(oEvent){

	bReturn = cancelTextboxSubmit(oEvent);

	if(bReturn == false){
		searchMap();
		return false;
	}else{
		return true;
	}
	
}


	
