<?php
/*
 * emailform.php:
 * Email Form for contacting site administrators.
 * 
 * Copyright (c) 2007 UK Citizens Online Democracy. All rights reserved.
 * Email: angie@mysociety.org; WWW: http://www.mysociety.org
 *
 * $Id: emailform.php,v 1.3 2007-11-05 17:02:10 angie Exp $
 * 
 */


// Load configuration file
require_once "../conf/general";

function get_emailform_config () {

/* setup the fields that are wanted on the contact form, 
 *    this will be dynamically built using emailform_entry_output,
 * it will also be checked by emailform_test_message, if you want to add another field stick it in here.
 */

    $emailformfields = array (
        '01' => array ('label' => 'Email Address', 'inputname' => 'emailaddy', 'inputtype' => 'text', 'size' => '30', 'validate' => "emailaddress", 'required' => 1, 'emailoutput' => 'sender'),
        '02' => array ('label' => 'Name', 'inputname' => 'name', 'inputtype' => 'text', 'size' => '30', 'spamcheck' => "1", 'required' => 1),
        '03' => array ('label' => 'Subject', 'inputname' => 'subject', 'inputtype' => 'text', 'size' => '30', 'spamcheck' => "1", 'emailoutput' => 'subject'),
        '04' => array ('label' => 'Message', 'inputname' => 'notjunk', 'inputtype' => 'textarea', 'size' => '10,29', 'spamcheck' => "1", 'required' => 1),
        '07' => array ('label' => '', 'inputname' => 'send', 'inputtype' => 'submit', 'value' => 'Send us your thoughts'),
    );


    return $emailformfields;
}


function fyr_display_emailform () {
    $sendnow = 0;
    $messages = '';
    if (isset($_POST['action'])  && $_POST['action']== 'testmess') {
        $messages = emailform_test_message();
        if ($messages) {
            emailform_display($messages);
            return;
        } else {
            if (emailform_send_message()) {
                $messages['messagesent'] = 'Thanks, your message has been sent to ' . OPTION_WEB_DOMAIN;
            } else {
                $messages['messagenotsent'] = 'Sorry, there was a problem';
            }
            emailform_display($messages);
        }
    } else {
        emailform_display($messages);
    }
}

function emailform_display ($messages) {
    if ($messages) {
        if (isset($messages['messagesent'])) {
            print '<p class="alertsuccess">' . $messages['messagesent']  . '</p>';
        } else {
            print '<p class="warning">';
            foreach ($messages as $inp => $mess) {
                print '' . $mess . '<br />';
            }
            print '</p>';
        }
    }
    // load up the config
    $emailformfields = get_emailform_config();
    
    print '<form action="about-contactresponse" accept-charset="utf8" method="post">';
    print '<input name="action" type="hidden" value="testmess" />';
    
    foreach ($emailformfields as $row => $defs) {
        $input = '';
        $value='';
        if(isset($defs['value'])) {$value = $defs['value'];}
        if(isset($_POST[$defs['inputname']])) {$value = $_POST[$defs['inputname']];}
        $htmlvalue = htmlentities($value, ENT_QUOTES, 'UTF-8');
        //$htmlvalue = mb_convert_encode($value,'HTML-ENTITIES','UTF-8');
        //$htmlvalue = $value;
        
        if ($defs['inputtype'] == 'text') {
            $input = '<input type="text" name="' . $defs['inputname'] . '" id="' . $defs['inputname'] . '" size="' . $defs['size'] . '" value="' . $htmlvalue . '" />';
        }
        if ($defs['inputtype'] == 'textarea') {
            $sizes = explode(",", $defs['size']);
            $input = '<textarea name="' . $defs['inputname'] . '" id="' . $defs['inputname'] . '" rows="' . $sizes[0] . '" cols="' . $sizes[1] . '">' . $htmlvalue . '</textarea>';
        }
        if ($defs['inputtype'] == 'submit') {
            $input = '<input name="' . $defs['inputname'] . '" id="' . $defs['inputname'] . '" type="submit" value="' . $defs['value'] . '" />';
        }
        if ($defs['inputtype'] == 'radio') {
            $radiovalues = $defs['values'];
            foreach ($radiovalues as $radvalue) {
                $checked = ($value == $radvalue) ? ' checked' : '';
                $input .= '<input name="' . $defs['inputname'] . '" id="' . $defs['inputname'] . '" type="radio" value="' . $radvalue . '" ' . $checked . ' /> ' . $radvalue . '<br/>';
            }
        }
        $label = $defs['label'];
        if (isset($defs['required']) && $defs['required']) {
            if (isset($errors[$defs['inputname']])) {
                $label .= ' <span class="alert">(required)</span>';
            } else {$label .= ' (required)';}
        }
        
        $out = '<p><label for="' . $defs['inputname'] . '">' . $label .  '</label>' . $input . '</p>';
        print $out;
    }
    print '</form>';
}


function emailform_test_message () {
    $emailformfields = get_emailform_config();
    $errors = array ();
    foreach ($emailformfields as $row => $defs) {
        if (isset($defs['required']) && $defs['required'] && !$_POST[$defs['inputname']]) {
            $errors[$defs['inputname']] = "Please enter your " . $defs['label'];
        }
        if (isset($defs['spamcheck']) && $defs['spamcheck']) {
            $ermess = emailform_test_spam($defs['inputname']);
            if ($ermess) {
                $errors[$defs['inputname']] = $defs['label'] . $ermess;
            }
            
        }
        if (isset($defs['validate']) && $defs['validate'] == 'emailaddress') {
            if (! validate_email($_POST[$defs['inputname']]) ) {
                $ermess = 'email address is not correct';
                if ($ermess) {
                    $errors[$defs['inputname']] = $ermess;
                }
            }
        }
        
        
    }
    return $errors;
}

function emailform_test_spam ($inputname) {
    $searchpat = '/(?:<\/?\w+((\s+\w+(\s*=\s*(?:\".*?\\\"|.*?|[^">\s]+))?)+\s*|\s*)\/?>|\[\/url\])/s';
    if (isset($_POST[$inputname]) && preg_match($searchpat, $_POST[$inputname])) {
        return " contains HTML or spam";
    }
}


function emailform_send_message () {
    // we could put the testing of the message in here, but not doing so allows us to test that messages can be sent without having to check everything first.
    $sendto = OPTION_CONTACT_EMAIL;
    $emailformfields = get_emailform_config();
    $mailbody = '';
    $subject = 'no subject';
    $sender = '';
    $messagesent = 0;
    foreach ($emailformfields as $row => $defs) {
    // loop through emailformfields and fill in the mail body
        if (isset($defs['emailoutput']) && isset($_POST[$defs['inputname']])) {
            // this value goes into the subject or sender    
            if ($defs['emailoutput'] == 'subject') {
                $subject = 'Message from ' . OPTION_WEB_DOMAIN . ': '. $_POST[$defs['inputname']];
            }
            if ($defs['emailoutput'] == 'sender') {
                $sender = $_POST[$defs['inputname']];
            }
        } else {
            if (isset($_POST[$defs['inputname']]) && $defs['inputtype'] != 'submit') {
                $mailbody .= $defs['label'] . ': ' . $_POST[$defs['inputname']] . "\n\n";
            }
        }
    }
    if ($sender && $mailbody) {
        $from = 'From: ' . $sender;
        $messagesent = mail($sendto, $subject, $mailbody, $from);
    }
    if ($messagesent) {return 1;}
    return 0;
}

function emailform_response_output() {

}


?>
