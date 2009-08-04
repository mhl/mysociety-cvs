<?php
/*
Plugin Name: Ultimate Category Excluder
Plugin URI: http://www.planetmike.com/plugins/ultimate-category-excluder/
Description: Easily exclude categories from your front page, feeds, and archives.
Author: Michael Clark
Version: 0.3
Author URI: http://www.planetmike.com
*/

add_action('admin_menu', 'ksuce_admin_menu');
add_filter('pre_get_posts','ksuce_exclude_categories');

function ksuce_admin_menu() {
	add_options_page( 'Ultimate Category Excluder Options', 'Category Exclusion', 9, basename(__FILE__), 'ksuce_options_page');
}

function ksuce_options_page() {
	if( $_POST[ 'ksuce' ] ) {
		$message = ksuce_process();
	}
	$options = ksuce_get_options();
	?>
	<div class="wrap">
		<h2>Ultimate Category Excluder Options</h2>
		<?php echo $message ?>
		<p>Use this page to select the categories you wish to exclude and where you would like to exclude them from.</p>
	<form action="options-general.php?page=ultimate-category-excluder.php" method="post">
	<table class="widefat">
		<thead>
			<tr>
				<th scope="col">Category</th>
				<th scope="col">Exclude from Main Page?</th>
				<th scope="col">Exclude from Feeds?</th>
				<th scope="col">Exclude from Archives?</th>
			</tr>
		</thead>
		<tbody id="the-list">
	<?php
		//print_r( get_categories() );
		$cats = get_categories();
		$alt = 0;
		foreach( $cats as $cat ) {
			?>
			<tr<?php if ( $alt == 1 ) { echo ' class="alternate"'; $alt = 0; } else { $alt = 1; } ?>>
				<th scope="row"><?php echo $cat->cat_name; //. ' (' . $cat->cat_ID . ')'; ?></th>
				<td>
					<input type="checkbox" name="exclude_main[]" value="-<?php echo $cat->cat_ID ?>" <?php if ( in_array( '-' . $cat->cat_ID, $options['exclude_main'] ) ) { echo 'checked="true" '; } ?>/>
				</td>
				<td><input type="checkbox" name="exclude_feed[]" value="-<?php echo $cat->cat_ID ?>" <?php if ( in_array( '-' . $cat->cat_ID, $options['exclude_feed'] ) ) { echo 'checked="true" '; } ?>/></td>
				<td><input type="checkbox" name="exclude_archives[]" value="-<?php echo $cat->cat_ID ?>" <?php if ( in_array( '-' . $cat->cat_ID, $options['exclude_archives'] ) ) { echo 'checked="true" '; } ?>/></td>
			</tr>			
		<?php
		}
	?>
	</table>
	<p class="submit"><input type="submit" value="Update" /></p>
	<input type="hidden" name="ksuce" value="true" />
	</form>
	</div><?php
}

function ksuce_process() {
	//echo '<pre>'; print_r( $_POST );
	if( !$_POST[ 'exclude_main' ] ) {
		$_POST[ 'exclude_main' ] = array();
	}
	if( !$_POST[ 'exclude_feed' ] ) {
		$_POST[ 'exclude_feed' ] = array();
	}
	if( !$_POST[ 'exclude_archives' ] ) {
		$_POST[ 'exclude_archives' ] = array();
	}
	$options['exclude_main'] = $_POST[ 'exclude_main' ];
	$options['exclude_feed'] = $_POST[ 'exclude_feed' ];
	$options['exclude_archives'] = $_POST[ 'exclude_archives' ];
	update_option('ksuceExcludes', $options);
	
	$message = "<div class='updated'><p>Excludes successfully updated</p></div>";
	return $message;
}

function ksuce_get_options(){
	$defaults = array();
	$defaults['exclude_main'] = array();
	$defaults['exclude_feed'] = array();
	$defaults['exclude_archives'] = array();

	$options = get_option('ksuceExcludes');
	if (!is_array($options)){
		$options = $defaults;
		update_option('ksuceExcludes', $options);
	}

	return $options;
}

function ksuce_exclude_categories($query) {
	$options = ksuce_get_options();
	if ($query->is_home) {
		$query->set('cat', implode( ', ', $options[ 'exclude_main' ] ) );
	}
	if ($query->is_feed) {
		$query->set('cat', implode(', ', $options[ 'exclude_feed' ] ) );
	}
	if ($query->is_archive) {
		$query->set('cat', implode(', ', $options[ 'exclude_archives' ] ) );
	}

	return $query;
}

?>
