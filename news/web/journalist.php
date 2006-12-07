<?php
/*
 * journalist.php:
 * news ui journalist add/edit page.
 * 
 * Copyright (c) 2006 UK Citizens Online Democracy. All rights reserved.
 * Email: louise.crow@gmail.com. WWW: http://www.mysociety.org
 *
 * $Id: journalist.php,v 1.1 2006-12-07 15:58:55 louise Exp $
 * 
 */

require_once "../conf/general";
require_once "../../phplib/news.php";
require_once "../../phplib/utility.php";
require_once "../../phplib/validate.php";

require_once "../phplib/page.php";
require_once "../phplib/news.php";

$newspaper_id = trim(get_http_var('nid', true));
$journalist_id = trim(get_http_var('id', true));

if (!$newspaper_id) $newspaper_id = trim(get_http_var('newspaper_id', true));

if ($newspaper_id == '') {
    header('Location: /');
    exit();
}

$newspaper = news_get_newspaper($newspaper_id);


if (!$newspaper['name']){
        page_header("NeWs - Newspaper not found");
        print '<h2>Newspaper not found</h2>';
        print 'This newspaper could not be found';
        exit();
}


if (is_numeric($journalist_id)){
	$header = $newspaper['name'] . " - Update journalist information";
}else{
	$header = $newspaper['name'] .  " - Add journalist information";
}
page_header("NeWs - " . $header);
print '<h2>' . $header . '</h2>';
if (get_http_var('update')){
	
        $journalist = array();
        if (is_numeric( get_http_var('id'))){
                $journalist['id'] = get_http_var('id');
        }

        $journalist['newspaper_id'] = get_http_var('newspaper_id');
        $journalist['name'] = get_http_var('name');
        $journalist['email'] = get_http_var('email');
        $journalist['telephone'] = get_http_var('telephone');
        $journalist['fax'] = get_http_var('fax');
        $journalist['interests'] = get_http_var('interests');
	
	$errors = validate_data($journalist);
	
	if (sizeof($errors)) {
	
		print journalist_form($journalist, $newspaper_id, $errors);
	}else{
		#send the update 
		$journalist_id = news_publish_journalist_update('website',$journalist);
	
		$journalist = news_get_journalist($journalist_id);
		print journalist_display($journalist);
	}
}else{
	if (is_numeric($journalist_id)){
                $journalist = news_get_journalist($journalist_id);
		
		if (!$journalist['name']){
			# there was an id submitted in the params
			# but it's not found in the database
			print "Journalist not found";
			exit();
		}
        }else{
		$journalist = NULL;
	}

	print journalist_form($journalist, $newspaper_id);
}
print '<a href="../newspaper?id=' . $newspaper_id . '">Back to ' . $newspaper['name'] . '</a>';
page_footer();


/* validate_data
 * Validate the form fields */
function validate_data($journalist){

        $errors = array();
        if ( !$journalist['name'] ){
                $errors['name'] = 'Please enter the journalist\'s name';
        }
        if ( $journalist['email'] && !validate_email($journalist['email'])){
                $errors['email'] = 'Please enter a valid email address';
        }
        if ($journalist['telephone'] && !preg_match('#\d#', $journalist['telephone'])){
                $errors['telephone'] = 'Please enter a valid telephone number';
        }
        if ($journalist['fax'] && !preg_match('#\d#', $journalist['fax'])){
                $errors['fax'] = 'Please enter a valid fax number';
        }

	return $errors;
}

/* journalist_display
 * Generate an HTML listing of the info about a journalist */

function journalist_display($journalist){
        $ret = '<div id="one-journalist-info-box">';
	$ret .= '<h3 id="small-heading">Updated!</h3>';	
	$ret .= '<b>Name:</b> ' . $journalist['name'] . '<br />';
	$ret .= '<b>Email:</b> ' . $journalist['email'] . '<br />';
	$ret .= '<b>Telephone:</b> ' . $journalist['telephone'] . '<br />';
	$ret .= '<b>Fax:</b> ' . $journalist['fax'] . '<br />';
	$ret .= '<b>Interests:</b> ' . $journalist['interests'] . '<br />';	
	$ret .= '</div>';
	return $ret;
}

/* journalist_form
 * Generate an HTML form for a journalist */

function journalist_form($journalist, $newspaper_id, $errors = array()){

	$ret = '<div id="one-journalist-info-box">';
	$ret .= '<form action="../journalist" name="journalist" class="login" method="POST" accept-charset="utf-8">';
	$journalist_fields = array('name', 'email', 'telephone', 'fax', 'interests' );
        $ret .= '<table>';
	foreach ($journalist_fields as $fieldname){
		
		if (isset($journalist)){
			$ret .= journalist_field($fieldname, $journalist, $errors);
		}else{
			$ret .= journalist_field($fieldname, $journalist, $errors);
		}
	}
	$ret .= '<tr><td colspan=2>';
	if (isset($journalist)){
		$newspaper_id = $journalist['newspaper_id'];
		$ret .= '<input type="hidden" name="id" value="' . $journalist['id'] . '">';
	}	
	$ret .= '<input type="hidden" name="newspaper_id" value="' . $newspaper_id . '">';
	$ret .= '<input type="hidden" name="update" value="true">';
	$ret .= '<input type="submit" value="Update">';
	$ret .= '</td></tr></table>';
	$ret .= '</form>';
	$ret .= '</div>';
	return $ret;
}

/* journalist_field
 * Generates a field for the journalist form */
function journalist_field($fieldname, $journalist=NULL, $errors){
	$ret = '<tr><td>' . ucwords($fieldname) . '</td><td> <input type="text" name="' . $fieldname . '" ';
	if (isset($journalist)){
                $ret .= ' value="' . $journalist[$fieldname] . '" ';
        }
	if (array_key_exists($fieldname, $errors)){
		$ret .= ' class="error" ';
	}
	$ret .= '>';
	if (array_key_exists($fieldname, $errors)){
        	$ret .= ' <span class="errortext">'. $errors[$fieldname] . '</span>';
        }
	$ret .= '</td></tr>';
        return $ret;
}

?>