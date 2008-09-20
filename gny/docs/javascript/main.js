function changeInvolvedType(){
	if(get('radInvolvedType_web').checked != false){
		get('txtInvolvedEmail').value="";
		get('txtInvolvedEmail').disabled = true;
		get('txtInvolvedLink').disabled = false;		
		setFocus('txtInvolvedLink');		
	}else{
		get('txtInvolvedLink').value="";
		get('txtInvolvedLink').disabled = true;		
		get('txtInvolvedEmail').disabled = false;				
		setFocus('txtInvolvedEmail');
	}
}

function popup_map(link){
	document.open(link.href, 'name', 'width=400,height=400');
}


function setupGame (){
    	sPost = "mode=get";
		var oAjax = new Ajax.Request("/ajax/game.php", {method: 'post',  postBody: sPost,  onComplete: setupGameCallback});
		
}

function setupGameCallback(oResponse){

 	var oResult = eval('(' + oResponse.responseText + ')');

	if (oResult != false) {

	    //link
	    $('aLink1').href = oResult['link'];
	    $('aLink2').href = oResult['link'];	
	    $('aGoogle1').href = 'http://www.google.com/search?q=' + oResult['by_line'];
	    $('aGoogle2').href = 'http://www.google.com/search?q=' + oResult['by_line'];
	    
	    //hash id
	    $('hidGameHash').value = oResult['id'];	    	 
	    
	    //clear the map search
	    $('txtSearchMap').value = '';

        //description
        var sDescriptionRaw = oResult['description'];
	    var sDescriptionHtml = replaceAll(oResult['description'], '\n', '<br/>');

        var sDescriptionHtml = gameHighlight(sDescriptionHtml);
        $('divGameGroupText').innerHTML = sDescriptionHtml;	    
        $('txtGameDetail').value = sDescriptionRaw;
        $('hTitle1').innerHTML = oResult['by_line'];
        $('hTitle2').innerHTML = oResult['by_line'];        
        $('txtGameTags').value = oResult['category'];

        //reset fields
        $('hidZoomLevel').value = 2;


        //set focus to text
        setFocus('divGameGroupText');
        
	}else{
	    alert('Sorry, somehting went wrong');
    }

    hideGameDetail();

}

function gameHighlight(sText){

    //good
    sText = replaceAll(sText, ' residents association', '<span class="highlightgood"> residents association</span>');
    sText = replaceAll(sText, ' Residents Association', '<span class="highlightgood"> Residents Association</span>');    
    sText = replaceAll(sText, ' community', '<span class="highlightgood"> community</span>');
    sText = replaceAll(sText, ' Community', '<span class="highlightgood"> Community</span>');    
    sText = replaceAll(sText, ' neighbourhood', '<span class="highlightgood"> neighbourhood</span>');
    sText = replaceAll(sText, ' Neighbourhood', '<span class="highlightgood"> Neighbourhood</span>');    
    sText = replaceAll(sText, ' neighborhood', '<span class="highlightgood"> neighborhood</span>');
    sText = replaceAll(sText, ' Neighborhood', '<span class="highlightgood"> Neighborhood</span>');    
    sText = replaceAll(sText, ' residents', '<span class="highlightgood"> residents</span>');	    
    sText = replaceAll(sText, ' Residents', '<span class="highlightgood"> Residents</span>');	        
    sText = replaceAll(sText, ' street', '<span class="highlightgood"> street</span>');
    sText = replaceAll(sText, ' Street', '<span class="highlightgood"> Street</span>');    
    sText = replaceAll(sText, ' road', '<span class="highlightgood"> road</span>');
    sText = replaceAll(sText, ' Road', '<span class="highlightgood"> Road</span>');    
    sText = replaceAll(sText, ' City', '<span class="highlightgood"> City</span>');    
    sText = replaceAll(sText, ' city', '<span class="highlightgood"> city</span>');
    sText = replaceAll(sText, ' town', '<span class="highlightgood"> town</span>');    
    sText = replaceAll(sText, ' Town', '<span class="highlightgood"> Town</span>');        
    sText = replaceAll(sText, ' Hamlet', '<span class="highlightgood"> Hamlet</span>');            
    sText = replaceAll(sText, ' hamlet', '<span class="highlightgood"> hamlet</span>');                
    sText = replaceAll(sText, ' village ', '<span class="highlightgood"> village</span>');  
    sText = replaceAll(sText, ' Village', '<span class="highlightgood"> Village</span>');          
    sText = replaceAll(sText, ' local', '<span class="highlightgood"> local</span>');    
    sText = replaceAll(sText, ' Local', '<span class="highlightgood"> Local</span>');        
    sText = replaceAll(sText, ' county', '<span class="highlightgood"> county</span>');            
    sText = replaceAll(sText, ' County', '<span class="highlightgood"> County</span>');                
    sText = replaceAll(sText, ' Neighbourhood Watch', '<span class="highlightgood"> Neighbourhood Watch</span>');      
    sText = replaceAll(sText, ' neighbourhood watch', '<span class="highlightgood"> neighbourhood watch</span>');          

    //bad
    sText = replaceAll(sText, ' global', '<span class="highlightbad"> global</span>');
    sText = replaceAll(sText, ' Global', '<span class="highlightbad"> Global</span>');
    sText = replaceAll(sText, ' national', '<span class="highlightbad"> national</span>');    
    sText = replaceAll(sText, ' National', '<span class="highlightbad"> National</span>');        
    sText = replaceAll(sText, ' National', '<span class="highlightbad"> National</span>');
    sText = replaceAll(sText, ' globe', '<span class="highlightbad"> globe</span>');            

    return sText;
}

function showGameDetail(){
    $('divGameChoose').style.display = 'none';    
    $('divGameDetail').style.display = 'block';
    setFocus('txtGameDetail');
}

function hideGameDetail(){
    $('divGameChoose').style.display = 'block';
    $('divGameDetail').style.display = 'none';
    
}

function gameSetTag(sTag){
    var sComma = '';
    if($('txtGameTags').value != ''){
        sComma = ', ';
    }
    $('txtGameTags').value = $('txtGameTags').value + sComma + sTag
}

function validateGame(){

    var sWarnings = '';

    //detail
    if($('txtGameDetail').value == '' || $('txtGameDetail').value == false){
        sWarnings += "Please enter a brief description for this group\n";
    }

    //map zoom
    if(parseInt($('hidZoomLevel').value) < parseInt($('hidMaxMapZoom').value)){
        sWarnings += "Sorry, that group covers too large an area.We are currently only mapping small local groups, like an email list for a street town. Please adjust the map or cancel and try another group.'\n";        
    }

    if(sWarnings == ''){

        //save the group
        sPost = "mode=save";
        sPost += ("&hash=" + $('hidGameHash').value); 
        sPost += ("&long_bottom_left=" + $('hidLongBottomLeft').value); 
        sPost += ("&lat_bottom_left=" + $('hidLatBottomLeft').value); 
        sPost += ("&long_top_right=" + $('hidLongTopRight').value); 
        sPost += ("&lat_top_right=" + $('hidLatTopRight').value); 
        sPost += ("&lat_centroid=" + $('hidLatCentroid').value); 
        sPost += ("&long_centroid=" + $('hidLongCentroid').value); 
        sPost += ("&zoom_level=" + $('hidZoomLevel').value);                                                        
        sPost += ("&game_detail=" + escape($('txtGameDetail').value));                                                                
        sPost += ("&game_tags=" + escape($('txtGameTags').value));         
        sPost += ("&category_id=" + $('ddlCategory').value);    
        sPost += ("&name=" + escape($('hidName').value));                            
        sPost += ("&email=" + escape($('hidEmail').value));                                    

		var oAjax = new Ajax.Request("/ajax/game.php", {method: 'post',  postBody: sPost,  onComplete: gameSavedCallback});
        
    }else{
        showWarning(sWarnings);
    }
    
}

function gameNotLocal(){
    	var oAjax = new Ajax.Request("/ajax/game.php", {method: 'post',  postBody: "mode=notlocal&hash=" + $('hidGameHash').value,  onComplete: gameSavedCallback});
}

//games saved callback
function gameSavedCallback(oResponse){
    
var oResult = eval('(' + oResponse.responseText + ')');

 	var oResult = eval('(' + oResponse.responseText + ')');

    if(oResult == true){
        hideGameDetail();
        setupGame();
    }else{
        alert('Sorry, something went wrong saving this group. Please try again, or click cancel and pick another group')
    }

}