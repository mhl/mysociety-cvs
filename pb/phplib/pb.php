<?php
/*
 * pb.php:
 * General purpose functions specific to PledgeBank.  This must
 * be included first by all scripts to enable error logging.
 * This is only used by the web page PHP scripts, command line ones 
 * use pbcli.php.
 * 
 * Copyright (c) 2005 UK Citizens Online Democracy. All rights reserved.
 * Email: francis@mysociety.org; WWW: http://www.mysociety.org
 *
 * $Id: pb.php,v 1.82 2007-08-10 03:02:02 matthew Exp $
 * 
 */

// Load configuration file
require_once "../conf/general";
// Some early config files - put most config files after language negotiation below
require_once "../../phplib/error.php";
require_once "../../phplib/locale.php";
require_once 'page.php';

// Googlebot is crawling all our domains for different languages/codes at 
// a high rate, which in combination is too much for our server.
$lockfilehandle = null;
if (array_key_exists('HTTP_USER_AGENT', $_SERVER) && stristr($_SERVER['HTTP_USER_AGENT'], "Googlebot")) {
    $lockfilehandle = fopen("../conf/general", "rw");
    if ($lockfilehandle)
        flock($lockfilehandle, LOCK_SH);
}

/* Output buffering: PHP's output buffering is broken, because it does not
 * affect headers. However, it's worth using it anyway, because in the common
 * case of outputting an HTML page, it allows us to clear any output and
 * display a clean error page when something goes wrong. Obviously if we're
 * displaying an error, a redirect, an image or anything else this will break
 * horribly.*/
ob_start();

/* pb_handle_error NUMBER MESSAGE
 * Display a PHP error message to the user. */
function pb_handle_error($num, $message, $file, $line, $context) {
    if (OPTION_PB_STAGING) {
        while (ob_get_level()) {
            ob_end_clean();
        }
        ob_start(); // since page header writes content length, must be in ob_
        page_header(_("Sorry! Something's gone wrong."), array('override'=>true));
        print("<strong>$message</strong> in $file:$line");
        page_footer(array('nolocalsignup'=>true));
    } else {
        /* Nuke any existing page output to display the error message. */
        while (ob_get_level()) {
            ob_end_clean();
        }
        /* Message will be in log file, don't display it for cleanliness */
        $err = p(_('Please try again later, or <a href="mailto:team&#64;pledgebank.com">email us</a> for help resolving the problem.'));
        if ($num & E_USER_ERROR) {
            $err = "<p><em>$message</em></p> $err";
        }
        ob_start(); // since page header writes content length, must be in ob_
        pb_show_error($err);
    }
}
err_set_handler_display('pb_handle_error');

# Extract language and country from URL.
# OPTION_WEB_HOST . OPTION_WEB_DOMAIN - default
# xx . OPTION_WEB_DOMAIN - xx is an ISO 639-1 country code
# xx . yy . OPTION_WEB_DOMAIN - xx is a country code, yy a language code (either aa or aa-bb)
$domain_lang = null;
$domain_country = null;
$re_lang = '(..(?:-..)?)';
if (OPTION_WEB_HOST == 'www') {
    if (preg_match("#^(?:[^.]+|www)\.$re_lang\.#", strtolower($_SERVER['HTTP_HOST']), $m))
        $domain_lang = $m[1];
} else {
    if (preg_match('#^'.OPTION_WEB_HOST."(?:-[^.]+)?\.$re_lang\.#", strtolower($_SERVER['HTTP_HOST']), $m))
        $domain_lang = $m[1];
    elseif (preg_match("#^(?:[^.]+)\.$re_lang\.".OPTION_WEB_HOST.'\.#', strtolower($_SERVER['HTTP_HOST']), $m))
        $domain_lang = $m[1];
}
if (OPTION_WEB_HOST == 'www') {
    if (preg_match('#^([^.]+)\.#', strtolower($_SERVER['HTTP_HOST']), $m))
        $domain_country = strtoupper($m[1]);
} else {
    if (preg_match('#^'.OPTION_WEB_HOST.'-([^.]+)\.#', strtolower($_SERVER['HTTP_HOST']), $m))
        $domain_country = strtoupper($m[1]);
    elseif (preg_match('#^([^.]+)\.(?:..(?:-..)?\.)?'.OPTION_WEB_HOST.'\.#', strtolower($_SERVER['HTTP_HOST']), $m))
        $domain_country = strtoupper($m[1]);
    else
        $domain_country = OPTION_WEB_HOST; # e.g. for interface.pledgebank.com
}

# Check for promesobanko.com etc.
$top_domain_lang = null;
$top_domain_domain = null;
foreach ($language_domains as $k => $v) {
    if (preg_match('#\.'.$v.'$#', $_SERVER['HTTP_HOST'])) {
        $top_domain_lang = $k;
        $top_domain_domain = $v;
        break;
    }
}
if (!$domain_lang) {
    $domain_lang = $top_domain_lang;
}

# Language negotiation
locale_negotiate_language(OPTION_PB_LANGUAGES, $domain_lang);
locale_change();
locale_gettext_domain(OPTION_PB_GETTEXT_DOMAIN);

# Redirect to promesobanko.com etc. if appropriate
if ($lang && array_key_exists($lang, $language_domains)
        && $lang != $top_domain_lang) {
    $url = pb_domain_url(array('country' => $domain_country, 'lang' => $lang));
    #print $url;exit;
    header('Location: ' . $url);
    exit;
}

# Do includes after language negotiation, so translated globals
# are translated in them
require_once 'microsites.php';
microsites_for_locale();
require_once '../../phplib/countries.php';
require_once '../../phplib/db.php';
require_once '../../phplib/stash.php';
require_once "../../phplib/utility.php";
require_once "../../phplib/gaze.php";

$site_country = null;
if ($domain_country) {
    if (array_key_exists('UK', $countries_code_to_name)) 
        err('UK in countries_code_to_name');
    if ($domain_country == 'UK')
        $domain_country = 'GB';
    if (array_key_exists($domain_country, $countries_code_to_name)) {
        if (!get_http_var('rss')) {
            $url = pb_domain_url(array());
            setcookie('country', $domain_country, 0, '/', 
                $top_domain_lang ? '.'.$top_domain_domain : '.'.OPTION_WEB_DOMAIN);
            header('Location: ' . $url);
            exit;
        }
        $site_country = $domain_country;
    }
} 

/* Find country for this IP address. If we're being called through the
 * accelerator it will have made up an X-GeoIP-Country: header which will
 * contain this information; otherwise, we must call out to Gaze. */
$ip_country = null;
if (array_key_exists('HTTP_X_GEOIP_COUNTRY', $_SERVER)) {
    $ip_country = $_SERVER['HTTP_X_GEOIP_COUNTRY'];
    if ($ip_country == 'none')
        $ip_country = null;
} else {
    $ip_country = gaze_get_country_from_ip($_SERVER['REMOTE_ADDR']);
    if (rabx_is_error($ip_country) || !$ip_country)
        $ip_country = null;
}
/* Ensure it's a country we know about. */
if (!array_key_exists($ip_country, $countries_code_to_name))
    $ip_country = null;


# Decide which country or microsite to use
$microsite = null;

if (array_key_exists(strtolower($_SERVER['HTTP_HOST']), $microsites_from_extra_domains)) {
    $microsite = $microsites_from_extra_domains[strtolower($_SERVER['HTTP_HOST'])];
} elseif (array_key_exists(strtolower($domain_country), $microsites_list)) {
    $microsite = strtolower($domain_country);
}
if (!$site_country) {
    $site_country = isset($_COOKIE['country']) ? $_COOKIE['country'] : null;
    if (!array_key_exists($site_country, $countries_code_to_name))
        $site_country = null;
}

if (!$site_country)
    $site_country = $ip_country;

# Without this, would go to 'Global' (only global pledges)
if ($site_country == null && $microsite == null)
    $microsite = "everywhere";

/* POST redirects */
stash_check_for_post_redirect();

/* Date which PledgeBank application believes it is */
$pb_today = db_getOne('select ms_current_date()');
$pb_timestamp = db_getOne('select ms_current_timestamp()');
$pb_time = strtotime(substr($pb_timestamp, 0, 19));

/* pb_show_error MESSAGE
 * General purpose error display. */
function pb_show_error($message) {
    header('HTTP/1.0 500 Internal Server Error');
    page_header(_("Sorry! Something's gone wrong."), array('override'=>true));
    print h2(_('Sorry! Something\'s gone wrong.')) .
        "\n<p>" . $message . '</p>';
    page_footer(array('nolocalsignup'=>true));
}



