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

function popup_map(sUrl){
	document.open(sUrl,'name', 'width=400,height=400');
}


