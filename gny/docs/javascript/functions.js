function get(sControl){	
	return document.getElementById(sControl);
}

function postBackForm(sForm, sPostbackCommand, sPostbackArgument) {

	if(sPostbackCommand){

		get("_postback_command").value = sPostbackCommand;
	}
	
	if(sPostbackArgument){
		get("_postback_argument").value = sPostbackArgument;
	}
	
    var oForm 	
    oForm = get(sForm);
	oForm.submit();
}

function setFocus(sID) {
	if(get(sID).disabled != true){
    	get(sID).focus();
	}
}

function cancelTextboxSubmit(oEvent) {
	
	var bReturn = true;
	
	if(!oEvent){ 
		oEvent=window.event;
	}
	
	if (oEvent.keyCode == 13) {
		bReturn = false;
	}
	
	return bReturn;
	
}

function showWarning (sWarnings) {

    var sWarningHtml = '';

	if(sWarnings.indexOf('\n') > 0){
        var aWarnings = sWarnings.split('\n');
        sWarningHtml += '<ul>'
	    for (var i=0;i<aWarnings.length -1;i++) {
	       if (aWarnings[i]!= ''){
    	       sWarningHtml += '<li>' + aWarnings[i] + '</li>';
    	   }
        }
        sWarningHtml += '</ul>'
	}else{
	   sWarningHtml = sWarnings;
	}
    var oWarning;
    oWarning = get('divWarning');
    
    oWarning.innerHTML = sWarningHtml;
    window.scroll(0,0);    
    oWarning.style.display = 'block' 
  
}

function hideWarning (){
    oWarning = get('divWarning');
	oWarning.style.display = 'none'
    oWarning.innerHTML = '';
}

function setControlWarning (oControl, bState){

    if(bState == true){
        oControl.className += ' error';
    } else {
        oControl.className = oControl.className.replace('error', '' );
    }

}