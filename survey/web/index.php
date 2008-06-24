<?php
/*
 * index.php:
 * For surveying demographic information etc. from our users.
 * 
 * Copyright (c) 2008 UK Citizens Online Democracy. All rights reserved.
 * Email: francis@mysociety.org; WWW: http://www.mysociety.org
 *
 * $Id: index.php,v 1.3 2008-06-24 16:41:21 francis Exp $
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

if (get_http_var('querydone')) {
    $user_code = get_http_var('user_code');
    $signature = get_http_var('auth_signature');
    $verified = auth_verify_with_shared_secret($user_code, OPTION_SURVEY_SECRET, $signature);
    if (!$verified)
        err("Signature wasn't verified.");
    $already_done = db_getOne('select count(*) from survey_done where user_code = ?', array($user_code));
    print $already_done ? 1 : 0;
    return;
} elseif (get_http_var('allownewsurvey')) {
    // called from test scripts, to let another survey happen
    $user_code = get_http_var('user_code');
    $signature = get_http_var('auth_signature');
    $verified = auth_verify_with_shared_secret($user_code, OPTION_SURVEY_SECRET, $signature);
    if (!$verified)
        err("Signature wasn't verified.");
    db_do('delete from survey_done where user_code = ?', array($user_code));
    db_commit();
    return;
} else {
    # Get input fields
    $site = $_POST['sourceidentifier'];
    $user_code = $_POST['user_code'];
    $signature = $_POST['auth_signature'];
    $return_url = $_POST['return_url'];
    # ... make sure none of those values are logged
    unset($_POST['user_code']);
    unset($_POST['auth_signature']);
    unset($_POST['return_url']);
    #print "<pre>"; print_r($_POST); print "</pre>";

    # Start transaction
    db_connect();

    # Check to see if really from one of our sites
    $verified = auth_verify_with_shared_secret($user_code, OPTION_SURVEY_SECRET, $signature);
    if (!$verified)
        err("Signature wasn't verified.");

    # See if already there
    $already_done = db_getOne('select count(*) from survey_done where user_code = ?', array($user_code));
    if ($already_done) {
        err("Done already");
    }
    db_query('insert into survey_done (user_code) values (?)', array($user_code));

    # Make arbitary key for storing actual data against
    $batch = auth_random_token();

    # Store the survey record
    foreach ($_POST as $key => $value) {
        db_query('insert into data_item (batch, site, key, value, whenstored)
        values (?, ?, ?, ?, now())', array($batch, $site, $key, $value));
    }
    db_commit();

    # Redirect back out
    header('Location: ' . $return_url);
}

