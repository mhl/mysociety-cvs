<?php
/*
 * index.php:
 * Admin page for demographic survey.
 * 
 * Copyright (c) 2008 UK Citizens Online Democracy. All rights reserved.
 * Email: francis@mysociety.org; WWW: http://www.mysociety.org
 *
 * $Id: index.php,v 1.2 2008-06-10 16:06:22 francis Exp $
 * 
 */

require_once "../conf/general";
require_once "../../phplib/error.php";
require_once "../../phplib/db.php";
require_once "../../phplib/utility.php";
require_once "../../phplib/auth.php";

function survey_handle_error($num, $message, $file, $line, $context) {
    print("<strong>$message</strong> in $file:$line");
    return;
}
err_set_handler_display('survey_handle_error');

db_connect();

$number_surveys_done = db_getOne('select count(*) from survey_done');
$number_surveys_done = db_getOne('select count(*) from survey_done');
$last_date = db_getOne('select max(whenstored) from data_item');

?>

<h1>Survey admin interface</h1>

<p>
    <strong>Number of surveys done:</strong> <?= $number_surveys_done ?>
    <br><strong>Date of last survey:</strong> <?= $last_date ?>
</p>


