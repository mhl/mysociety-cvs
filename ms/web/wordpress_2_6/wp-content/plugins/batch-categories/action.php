<?php

$admin = realpath(dirname(__FILE__) . '/../../../') . '/wp-admin';
chdir($admin);
require_once $admin . '/admin.php';

if ( !current_user_can('level_9') )
	die ( __('Cheatin&#8217; uh?') );

$_POST = stripslashes_deep($_POST);
$_GET = stripslashes_deep($_GET);

// Check if we've been submitted a tag/remove.
if ( !empty($_GET['ids']) ) {
	check_admin_referer('batch_categories-edit');
	
	$cat = intval($_GET['cat']);
	$num = count($_GET['ids']);
	
	if ( !empty($_GET['cat']) )
		$query = '&cat=' . $_GET['cat'];
	if ( !empty($_GET['s']) )
		$query = '&s=' . $_GET['s'];
	if ( !empty($_GET['t']) )
		$query = '&t=' . $_GET['t'];
	
	// We've been told to tag these posts with the given category.
	if ( !empty($_GET['add']) ) {
		foreach ( (array) $_GET['ids'] as $id ) {
			$id = intval($id);
			$cats = wp_get_post_categories($id);
			if ( !in_array($cat, $cats) ) {
				$cats[] = $cat;
				wp_set_post_categories($id, $cats);
			}
		}
		wp_redirect(get_option('siteurl') . "/wp-admin/edit.php?page=batch_categories&done=add&what=" . get_cat_name($cat) . "&num=$num$query");
		die;
	}
	// We've been told to remove these posts from the given category.
	elseif ( !empty($_GET['remove']) ) {
		foreach ( (array) $_GET['ids'] as $id ) {
			$id = intval($id);
			$existing = wp_get_post_categories($id);
			$new = array();
			foreach ( (array) $existing as $_cat ) {
				if ( $cat != $_cat )
					$new[] = $_cat;
			}
			wp_set_post_categories($id, (array) $new);
		}
		wp_redirect(get_option('siteurl') . "/wp-admin/edit.php?page=batch_categories&done=remove&what=" . get_cat_name($cat) . "&num=$num");
		die;
	}
	// We've been told to tag these posts
	elseif ( !empty($_GET['tag']) || !empty($_GET['replace_tags']) ) {
		$tags = $_GET['tags'];
		foreach ( (array) $_GET['ids'] as $id ) {
			$id = intval($id);
			$append = empty($_GET['replace_tags']);
			wp_set_post_tags($id, $tags, $append);
		}
		wp_redirect(get_option('siteurl') . "/wp-admin/edit.php?page=batch_categories&done=tag&what=$tags&num=$num$query");
		die;
	}
	// We've been told to untag these posts
	elseif ( !empty($_GET['untag']) ) {
		$tags = explode(',', $_GET['tags']);
		foreach ( (array) $_GET['ids'] as $id ) {
			$id = intval($id);
			$existing = wp_get_post_tags($id);
			$new = array();
			foreach ( (array) $existing as $_tag ) {
				foreach ( (array) $tags as $tag ) {
					if ( $_tag->name != $tag ) {
						$new[] = $_tag->name;
					}
				}
			}
			wp_set_post_tags($id, $new);
		}
		$tags = join(', ', $tags);
		wp_redirect(get_option('siteurl') . "/wp-admin/edit.php?page=batch_categories&done=untag&what=$tags&num=$num$query");
		die;
	}
}

die("Invalid action.");

?>