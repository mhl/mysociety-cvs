function deleteGroup(sGroupName, iGroupId){
	
	if(confirm("Delete " + sGroupName + "? (permanent)") == true){
		postBackForm('frmGroups', 'delete', iGroupId);
	}

}

function disableGroup(sGroupName, iGroupId){
	
	if(confirm("Disable " + sGroupName + "? It will be marked 'unconfimed' and hidden on the site.") == true){
		postBackForm('frmGroups', 'disable', iGroupId);
	}
	
}

function enableGroup(sGroupName, iGroupId){
	
	if(confirm("Enable " + sGroupName + "? It will be marked as confirmed and become visable on the site.") == true){
		postBackForm('frmGroups', 'enable', iGroupId);
	}
	
}

function editGroup(iGroupId){
	
	postBackForm('frmGroups', 'edit', iGroupId);
	
}