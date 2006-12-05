<?php
/*
 * NeWs.php:
 * General purpose functions specific to NeWs.  This must
 * be included first by all scripts to enable error logging.
 * 
 * Copyright (c) 2006 UK Citizens Online Democracy. All rights reserved.
 * Email: louise.crow@gmail.com; WWW: http://www.mysociety.org
 *
 * $Id: news.php,v 1.1 2006-12-05 13:32:21 louise Exp $
 * 
 */

require_once '../../phplib/error.php';
require_once '../../phplib/utility.php';
require_once 'page.php';

// HTML shortcuts
function p($s) { return "<p>$s</p>\n"; }
function h2($s) { return "<h2>$s</h2>\n"; }
function h3($s) { return "<h3>$s</h3>\n"; }
function strong($s) { return "<strong>$s</strong>"; }
function dt($s) { print "<dt>$s</dt>\n"; }
function dd($s) { print "<dd>$s</dd>\n"; }
function li($s) { return "<li>$s</li>\n"; }

/* news_handle_error NUMBER MESSAGE
 * Display a PHP error message to the user. */
function news_handle_error($num, $message, $file, $line, $context) {
    if (OPTION_NEWS_STAGING) {
        page_header(_("Sorry! Something's gone wrong."));
        print("<strong>$message</strong> in $file:$line");
        page_footer();
    } else {
        /* Nuke any existing page output to display the error message. */
        /* Message will be in log file, don't display it for cleanliness */
        $err = 'Please try again later, or <a href="mailto:team@mysociety.org">email us</a> for help resolving the problem.';
        if ($num & E_USER_ERROR) {
            $err = "<p><em>$message</em></p> $err";
        }
        news_show_error($err);
    }
}
err_set_handler_display('news_handle_error');

/* news_show_error MESSAGE
 * General purpose eror display. */
function news_show_error($message) {
    page_header(_("Sorry! Something's gone wrong."), array('override'=>true));
    print _('<h2>Sorry!  Something\'s gone wrong.</h2>') .
        "\n<p>" . $message . '</p>';
    page_footer();
}

/* news_general_heading
 * General heading */
function news_general_heading(){
    print "<h2>News Demo</h2>";
}

/* news_pretty_distance DISTANCE  [AWAY]
 * Given DISTANCE in km, return a text string
 * describing the DISTANCE in human-readable form. Specificy AWAY as false to not put
 * "away" at the end of the string, or round distances less than 1 km */
function news_pretty_distance($distance, $away = true) {
    $dist_miles = round($distance / 1.609344, 0);
    if ($away && $dist_miles < 1)
        return _('less than 1 mile away');
    else
        return sprintf(($away ? ngettext('%d mile away', '%d miles away', $dist_miles)
            : ngettext('%d mile', '%d miles', $dist_miles)), $dist_miles);
}

?>
