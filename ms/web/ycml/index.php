<?
// index.php:
// Initial constituent email gathering for Your Constituency Mailing List.
//
// Copyright (c) 2005 UK Citizens Online Democracy. All rights reserved.
// Email: matthew@mysociety.org. WWW: http://www.mysociety.org
//
// $Id: index.php,v 1.1 2005-05-05 01:01:00 francis Exp $

require_once '../../../phplib/importparams.php';
require_once '../../../phplib/utility.php';

require_once "../../conf/general";
require_once "DB.php";

// Connect to database
$vars = array('hostspec'=>'HOST', 'port'=>'PORT', 'database'=>'NAME', 'username'=>'USER', 'password'=>'PASS');
$connstr = array('phptype'=>'pgsql');
foreach ($vars as $k => $v) {
    if (defined('OPTION_YCML_DB_' . $v)) {
        $connstr[$k] = constant('OPTION_YCML_DB_' . $v);
    }
}
$ycmldb = DB::connect($connstr);
if (DB::isError($ycmldb)) {
    die($ycmldb->getMessage());
}

// Print header
?>

<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">
<html lang="en"><head><title>Your constituency mailing list</title>
<style type="text/css"><!--
    table {
        width: 100%; height: 100%;
    }
    p {
        line-height: 1.4;
    }
    body, html {
        font-family: Georgia, serif;
        margin: 1em 0 0 0; padding: 0;
        color: #000000;
        background-color: #ffffff;
    }
    td {
        text-align: center;
        vertical-align: middle;
    }
    div#votingmachine {
        text-align: left;
        margin: 0 auto;
        padding-left: 418px;
        background: url("shoup.gif") no-repeat top left #ffffff;
        width: 408px;
        height: 658px;
    }
    h1 {
        text-align: center;
        font-size: 250%;
        margin: 0;
        width: 1px;
    }
    form {
        display: table;
        padding-top: 0em;
        padding-left: 3em;
    }
    label {
        font-weight: bold;
        display: block;
    }
    .submit {
    }
    input {
    }
    #errors {
        margin: 0 auto 1em;
        color: #ff0000;
        background-color: #ffcccc;
        border: solid 2px #990000;
        padding-top: 3px;
        padding-bottom: 3px;
    }
    #errors ul {
        padding: 0;
        margin: 0 0 0 1.5em;
    }

--></style></head>
<body>
<?
    $done = false;
    $errors = array();
    if (get_http_var('posted')) {
        if (!validate_postcode(trim(get_http_var('postcode')))) {
            $errors[] = "Please enter a postcode, like  BS3 1QP";
        }
        if (!validate_email(get_http_var('email'))) {
            $errors[] = "Please enter your email address";
        }
        if (strlen(trim(get_http_var('name'))) < 1) {
            $errors[] = "Please enter your name";
        }
    }

    if (get_http_var('posted') && !sizeof($errors)) {
        $query = "insert into constituent (name, email, postcode, creation_time, creation_ipaddr) values (?, ?, ?, current_timestamp, ?)";
        $result = $ycmldb->query($query, array(trim(get_http_var('name')), trim(get_http_var('email')), 
            trim(get_http_var('postcode')), $_SERVER['REMOTE_ADDR']));
       if (DB::isError($result)) {
            die($result->getMessage().': "'.$result->getDebugInfo().'"; query was: ' . $query);
        }
        $ycmldb->commit();
?>
    <p align="center">
    <b>Thank you!</b>  We'll email you when we've built the site and your new
    MP is ready to start.
    </p>
<?
        $done = true;
    } 
    
    if (!$done) {
?>
<table border=0><tr><td><div id="votingmachine">
    <h1>Your constituency mailing list</h1>

<?
    if (sizeof($errors)) {
        print '<p></p><div id="errors"><ul><li>';
        print join ('</li><li>', array_values($errors));
        print '</li></ul></div>';
    } else {
?>
    <p>In the near future, this site will go live, to encourage and enable
    MPs to run email lists for their constituents, and allow those
    constituents to discuss ideas in a way which doesn't bombard them with
    email. <a href="http://www.mysociety.org/cgi-bin/moin.cgi/YourConstituencyMailingList">More information on our website</a>. Sign up if you're interested, and to hear more around launch time:</p>
<? } ?>
    <form method="post" action="./">
        <input type="hidden" name="posted" id="posted" value="1">
        <br><label for="name">Name:</label>
        <input type="text" name="name" id="name" value="<?=htmlspecialchars(get_http_var('name'))?>" size="20">
        <br><label for="email">Email:</label>
        <input type="text" name="email" id="email" value="<?=htmlspecialchars(get_http_var('email'))?>" size="30">
        <br><label for="postcode">Postcode:</label> 
        <input type="text" name="postcode" id="postcode" value="<?=htmlspecialchars(get_http_var('postcode'))?>" size="10">
        <input type="submit" class="submit" value="Go">
        <br><em>(for example OX1 3DR)</em>
    </form>
    </div></td></tr>
    <tr><td style="padding-left: 418px">Being built by <a href="http://www.mysociety.org/">mySociety</a></td></tr>
    </table>
<? 
    } 

// Print footer
?>
</body></html>

