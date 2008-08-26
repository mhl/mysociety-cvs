jQuery(function() {
	
	// Add a default value for the categories dropdown
	jQuery("#cat").prepend('<option value=""></option>');
	if ( !location.href.match(/&cat=([0-9]+)/) ) {
		jQuery("#cat")[0].selectedIndex = 0;
	}
	
	/*jQuery("#clear").click(
		function() {
			jQuery("#s, #t").attr("value", "");
			jQuery("#cat")[0].selectedIndex = 0;
			return false;
		}
	);*/
	
	jQuery("#toggle").change(
		function() {
			jQuery("#posts td input[type=checkbox]").each(
				function() {
					jQuery(this)[0].checked = jQuery("#toggle")[0].checked;
				}
			);
			
			if ( jQuery(this)[0].checked ) {
				jQuery(this).attr("title", "Select no posts");
			} else {
				jQuery(this).attr("title", "Select all posts");
			}
		}
	);
});