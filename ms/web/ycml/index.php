<?
// index.php:
// Initial constituent email gathering for Your Constituency Mailing List.
//
// Copyright (c) 2005 UK Citizens Online Democracy. All rights reserved.
// Email: matthew@mysociety.org. WWW: http://www.mysociety.org
//
// $Id: index.php,v 1.5 2005-05-20 08:17:48 francis Exp $

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
        text-align: left;
        vertical-align: middle;
    }
    h1 {
        text-align: center;
        font-size: 250%;
        margin: 0;
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
        if (strlen(trim(get_http_var('name'))) < 1) {
            $errors[] = "Please enter your name";
        }
        if (!validate_email(get_http_var('email'))) {
            $errors[] = "Please enter your email address";
        }
        if (!validate_postcode(trim(get_http_var('postcode')))) {
            $errors[] = "Please enter a postcode, like  BS3 1QP";
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
    <p style="font-size:100%; text-align:center">
    <b>Thank you!</b>  We'll email you when we've built the site and your new
    MP is ready to start.
    </p>

    <p style="font-size:150%; padding:1em; text-align:center">Meanwhile, why not <a href="http://www.ivotedforyoubecause.com">tell
    your new MP why you voted the way you did?</a>
<?
        $done = true;
    } 
    
    if (!$done) {
?>
<table border=0><tr><td>
<img alt="" src="shoup.gif"></td>

    <td>
    <h1>Your constituency mailing list</h1>
<p align="center">a <a href="http://www.mysociety.org/">
<img style="vertical-align:middle; border: none;" alt="mySociety" src="../mysociety_sm.gif"></a>
project
</p>

<?
    if (sizeof($errors)) {
        print '<p></p><div id="errors"><ul><li>';
        print join ('</li><li>', array_values($errors));
        print '</li></ul></div>';
    } else {
?>

<p><em>"So, the voting is over. The politicians vanish to Westminster, and
everything carries on as before, right?"</em></p>

<p>Wrong. Between elections the internet is really starting to challenge
politics as usual. As part of this change, we'd like to put you in
touch with your new MP. Not for a specific purpose, but in order to
hear what they're working on, to debate their thoughts in a safe,
friendly environment, and generally to build better, more useful
relationships between constituents and their MPs.</p>

<p>If you enter your details below, we'll add you to a queue of other
people in your constituency. When enough have signed up, your MP will
get sent an email. It'll say '20 of your constituents would like to
hear what you're up to - hit reply to let them know'. If they don't
reply, nothing will happen, until they get an email which says there
are now 100 people; 200 people; 500 people - until it is nonsensical
not to reply and start talking.</p>

<p>When your MP replies, it won't be one-way spam, and it won't be an
inbox-filling free-for-all. Instead, each email will have a link at
the bottom, which will take you straight to a forum where the first
post will contain the MP's email. There'll be no tiresome login - you
can just start talking about what they've said. Safe, easy and
democratic.</p>

<p><strong>Sign up now</strong>, and when the site is finished, you'll already
be on the list.</p>


<? } ?>
    <form method="post" action="./">
        <input type="hidden" name="posted" id="posted" value="1">
        <label for="name">Name:</label>
        <input type="text" name="name" id="name" value="<?=htmlspecialchars(get_http_var('name'))?>" size="20">
        <br><label for="email">Email:</label>
        <input type="text" name="email" id="email" value="<?=htmlspecialchars(get_http_var('email'))?>" size="30">
        <br><label for="postcode">Postcode:</label> 
        <input type="text" name="postcode" id="postcode" value="<?=htmlspecialchars(get_http_var('postcode'))?>" size="10">
        <input type="submit" class="submit" value="Sign up">
        <br><em>(for example OX1 3DR)</em>
    </form>
    </td></tr>
    </table>
<? 
    } 

// Print footer
?>
</body></html>

