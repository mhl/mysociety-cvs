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