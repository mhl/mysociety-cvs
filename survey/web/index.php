<?php
/*
 * index.php:
 * For surveying demographic information etc. from our users.
 * 
 * Copyright (c) 2008 UK Citizens Online Democracy. All rights reserved.
 * Email: francis@mysociety.org; WWW: http://www.mysociety.org
 *
 * $Id: index.php,v 1.1 2008-05-27 18:56:41 francis Exp $
 * 
 */

require_once "../conf/general";
require_once "../../phplib/error.php";
require_once "../../phplib/db.php";
require_once "../../phplib/utility.php";
require_once "../../phplib/utility.php";

function survey_handle_error($num, $message, $file, $line, $context) {
    print("<strong>$message</strong> in $file:$line");
    return;
}
err_set_handler_display('survey_handle_error');

# Get input fields
$site = $_POST['sourceidentifier'];
$user_code = "hello"; # XXX
$signature = $_POST['auth_signature'];
print "<pre>"; print_r($_POST); print "</pre>";

# Check to see if really from one of our sites
$verified = auth_verify_with_shared_secret($user_code, OPTION_SURVEY_SECRET, $signature);
if (!$verified)
    err("Signature wasn't verified.");

# Store the survey record
db_connect();
foreach ($_POST as $key => $value) {
    db_query('insert into data_item (user_code, site, key, value, whenlogged)
    values (?, ?, ?, ?, now())', array($user_code, $site, $key, $value));
}
db_commit();

#header('Location: ' . $url);


