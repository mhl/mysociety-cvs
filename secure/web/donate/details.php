<?php
/*
 * details.php:
 * page for gathering UKCOD donor info.
 * 
 * Copyright (c) 2006 UK Citizens Online Democracy. All rights reserved.
 * Email: louise@mysociety.org. WWW: http://www.mysociety.org
 *
 * $Id: details.php,v 1.1 2007-01-09 15:48:24 louise Exp $
 * 
 */

require_once "../../conf/general";
require_once "../../../phplib/utility.php";
require_once "../../../phplib/validate.php";
require_once "../../../phplib/db.php";

$giftaid = trim(get_http_var('giftaid', true));
if ($giftaid == '') {
    header('Location: /');
    exit();
}

print page_header();

$donor = array();

if (get_http_var('donor_submit')){

	#validate the data
    $donor_fields = array("title", "firstname", "surname", "address1", "address2","town", "county", "postcode", "country", "giftaid");
	
	foreach ($donor_fields as $donor_field){
		$donor[$donor_field] = get_http_var($donor_field);
	}

	$errors = validate_data($donor);

	if (sizeof($errors)) {
		print donor_form($donor, $errors);
	}else{
		#store a record
		$donor_ref = save_donor_info($donor);
		print payment_options($donor_ref);
	}
}else{
    $donor['giftaid'] = $giftaid;
	print donor_form($donor);
}

print page_footer();

/* Functions
 * */

/* save_donor_info
 * Stores donor name, address to the DB */
function save_donor_info($donor){
    $giftaid_val = "f";
    if( $donor['giftaid'] == "Yes" ){
	    $giftaid_val = "t";
	}
	
	db_query("insert into donor 
                 	(title, firstname, surname, address1, address2, town, county, 
	        	 postcode, country, giftaid) 
                 values (?,?,?,?,?,?,?,?,?,?)", 
	array(	$donor['title'], 
		$donor['firstname'], 
		$donor['surname'], 
		$donor['address1'], 
		$donor['address2'], 	
		$donor['town'],
		$donor['county'], 
		$donor['postcode'], 
		$donor['country'], 
		$giftaid_val));

	db_commit();
	$donor_ref = db_getOne("select currval('donor_id_seq')");
 	return $donor_ref;
}

/* donor_form
 * Generates the donor information form for name, address */
function donor_form($donor, $errors = array()){

	$ret = "<h2>Donate to mySociety by BACs or Standing Order</h2>";
	$ret .= "Required fields are marked with a *";
    $ret .= "<form action=\"details\" method=\"post\">";
	$ret .= "<fieldset>";
	$ret .= "<legend>Your details</legend>";
	$ret .= "<div class=\"formrow\">";
	$ret .= donor_field("Title", "title", true, $donor, $errors, 5, 5);
	$ret .= "</div>";
	$ret .= "<div class=\"formrow\">";
	$ret .= donor_field("First name", "firstname", true, $donor, $errors, 20, 20);
	$ret .= "</div>";
	$ret .= "<div class=\"formrow\">";
	$ret .= donor_field("Surname", "surname", true, $donor, $errors, 30, 30);
	$ret .= "</div>";
	$ret .= "<div class=\"formrow\">";
	$ret .= donor_field("House number and street", "address1", true, $donor, $errors, 60, 60);
	$ret .= "</div>";
	$ret .= "<div class=\"formrow\">";
	$ret .= donor_field("Address", "address2", false, $donor, $errors, 60, 60);
	$ret .= "</div>";

 	$ret .= "<div class=\"formrow\">";
	$ret .= donor_field("Town", "town", true, $donor, $errors, 30, 30);
	$ret .= "</div>";

	$ret .= "<div class=\"formrow\">";
	$ret .= donor_field("County", "county", false, $donor, $errors, 30, 30);
	$ret .= "</div>";

	$ret .= "<div class=\"formrow\">";
	$ret .= donor_field("Postcode", "postcode", true, $donor, $errors, 8, 8);
	$ret .= "</div>";

	$ret .= "<div class=\"formrow\">";
	$ret .= donor_field("Country", "country", true, $donor, $errors, 60, 60);
	$ret .= "</div>";

	$ret .= "</fieldset>";
	$ret .= "<input type=\"hidden\" name=\"giftaid\" id=\"giftaid\" value=" . $donor['giftaid'] . ">";
	$ret .= '<input type="hidden" name="donor_submit" value="true">';
	$ret .= "<p align=\"right\"><input type=\"submit\" value=\"submit\"></p>";
	$ret .= "</form>";

	return $ret; 
}

/* donor_field
 * Generates a text input field for the donor form */
function donor_field($label, $fieldname, $required, $donor, $errors, $length, $maxlength){

	$ret = "<label for=\"" . $fieldname . "\">" . $label;
	if ($required == true){
		$ret .= " <span class=\"required\">*</span>";
	}
	$ret .= "</label> ";
    $ret .= "<input name=\"" . $fieldname ."\" type=\"text\" ";
	$ret .= "id=\"" . $fieldname . "\" size=\"" . $length . "\" ";
	$ret .= " maxlength=\"" . $maxlength . "\"";
    if ( array_key_exists($fieldname, $donor)){
		$ret .= " value=\"" . $donor[$fieldname] . "\" ";
    }
	if (array_key_exists($fieldname, $errors)){
		$ret .= ' class="error" ';
	}
	$ret .= '>';
	if (array_key_exists($fieldname, $errors)){
        $ret .= ' <span class="errortext">'. $errors[$fieldname] . '</span>';
    }
	$ret .= '<br />';
    return $ret;
}

/* validate_data
 * Checks the donor form data */
function validate_data($donor){

	$errors = array();
    if ( !$donor['title'] ){
        $errors['title'] = 'Please enter your title';
    }
 	if ( !$donor['firstname'] ){
        $errors['firstname'] = 'Please enter your first name';
    }
    if ( !$donor['surname'] ){
        $errors['surname'] = 'Please enter your surname';
    }
    if ( !$donor['address1'] ){
        $errors['address1'] = 'Please enter your house number and street';
    }
    if ( !$donor['town'] ){
        $errors['town'] = 'Please enter your town';
    }
    if ( !$donor['postcode'] ){
        $errors['postcode'] = 'Please enter your postcode';
    }
    if ( !$donor['country'] ){
        $errors['country'] = 'Please enter your country';
    }

	return $errors;
}

/* payment_options
 * Shows the options once the donor form is filled out*/
function payment_options($donor_ref){
	$ret = "<h2>Thanks!</h2>";
	$ret .=  "<p>You can now ";
	$ret .= '<a href="standing_order.cgi/' . $donor_ref . '">download a standing order mandate</a> ';
	$ret .= ' or send payment by BACs.</p>'; 
    $ret .= '<h3>BACs Information</h3>';
    $ret .= '<p><strong>Bank:</strong> HSBC Holborn Circus, 31 Holborn, EC1N 2HR <br /> ';
    $ret .= '<strong>Account:</strong> UK Citizens Online Democracy, sort code 40-03-28, account number 31546341<br />';
    $ret .= '<strong>Please quote reference:</strong> ' . $donor_ref . '</p>';
	return $ret;
}

function page_header(){
  header('Content-Type: text/html; charset=utf-8');
?>

<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">
<html lang="en">
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8">
<title>Donate - mySociety</title>
<link rel="stylesheet" href="global.css" type="text/css" media="screen">
</head>

<body>
<div class="top">
<div class="masthead"><a href="http://www.mysociety.org/"><img border="0" src="/mslogo.gif" alt="mySociety.org"></a></div>
</div>

<div class="page-body">
<div class="menu">
&nbsp;<a href="http://www.mysociety.org/">News</a>&nbsp;|
&nbsp;<a href="http://www.mysociety.org/faq">FAQ</a> &nbsp;|
&nbsp;<a href="http://www.mysociety.org/projects">Projects</a>&nbsp;|
&nbsp;<a href="http://www.mysociety.org/category/developers">Developers' Blog</a>&nbsp;|
&nbsp;<a href="http://www.mysociety.org/moin.cgi">Wiki</a> |
&nbsp;<a href="http://www.mysociety.org/volunteertasks">Volunteer</a> |
&nbsp;<a href="https://secure.mysociety.org/admin/lists/mailman/listinfo/">Email Lists</a> |
&nbsp;<a href="http://www.mysociety.org/contact">Contact</a>
</div>

<div id="betteritemdiv">
<?
}

function page_footer(){
	$ret = "</div>";
	$ret .= "</div>";
	$ret .= "</body>";
	$ret .= "</html>";
	return $ret; 
}
?>