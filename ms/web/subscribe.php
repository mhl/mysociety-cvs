<?

// Quick script for easier newsletter subscribes, by Francis 2004-11-25 

include "wordpress/wp-blog-header.php";
include "wordpress/wp-content/themes/mysociety/header.php"; 

function send_email ($from) {
    $to = "news-request@lists.mysociety.org";
    $subject = "Subscribe";
    $message = "Subscribing from web form.";

    $headers =
     "From: $from\r\n" .
     "X-Mailer: PHP/" . phpversion();

    $success = mail ($to, $subject, $message, $headers);
    return $success;
}

// Far from foolproof, but better than nothing.
function validate_email ($string) {
    if (!ereg('^[-!#$%&\'*+\\./0-9=?A-Z^_`a-z{|}~]+'.
        '@'.
        '[-!#$%&\'*+\\/0-9=?A-Z^_`a-z{|}~]+\.'.
        '[-!#$%&\'*+\\./0-9=?A-Z^_`a-z{|}~]+$', $string)) {
        return false;
    } else {
        return true;
    }
}


$ok = false;
$email = $_POST["subv"];
if ($email == "your e-mail address") {
    print "<p><font color=#ff0000>Please enter your e-mail address</font></p>";
} else if (!validate_email($email)) {
    print "<p><font color=#ff0000>Please enter a valid e-mail address</font></p>";
} else {
    $ok = true;
}

if (!$ok) {

?>
<p>
<form method="post" action="/subscribe.php">
Subscribe for occasional <strong>mySociety news updates</strong> 
<input type="text" name="subv" value="your e-mail address" onfocus="this.value=''" />
<input type="submit" name="sub" value="go!" />
</form>
</p>

<?
} else {
    if (send_email($email)) {
        print "<p><b>Thanks!</b>  Now check your email. In a few minutes you will
        get a message telling you how to confirm your subscription.</p>";
    } else {
        print "<p>Sorry, there was a problem subscribing you.</p>";
    }
}

?>
<p><a href="/">Return to mySociety homepage</a>

<?php include "wordpress/wp-content/themes/mysociety/footer.php"; ?>
