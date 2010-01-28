<?php
/** WordPress's config file **/
/** http://wordpress.org/   **/

// ** MySQL settings ** //
if (!@include "../conf/general") {
    if (!@include "../../conf/general") {
        if (!@include "../../../conf/general") {
            if (!@include(dirname(__FILE__) . "../../../conf/general")) {
                print "Error including conf/general in wp-config.php on cee.mysociety.org WordPress";
                exit;
            }
        }
    }
}
define('DB_NAME', OPTION_CEE_DB_NAME);     // The name of the database
define('DB_USER', OPTION_CEE_DB_USER);     // Your MySQL username
define('DB_PASSWORD', OPTION_CEE_DB_PASS); // ...and password
define('DB_HOST', OPTION_CEE_DB_HOST);     // 99% chance you won't need to change this value

// Change the prefix if you want to have multiple blogs in a single database.

$table_prefix  = 'wp_';   // example: 'wp_' or 'b2' or 'mylogin_'

// Change this to localize WordPress.  A corresponding MO file for the
// chosen language must be installed to wp-includes/languages.
// For example, install de.mo to wp-includes/languages and set WPLANG to 'de'
// to enable German language support.
define ('WPLANG', '');

$toppath = $_SERVER['DOCUMENT_ROOT']; 
$trimmed = rtrim($toppath, "cee/web");
define('TOP_PATH', $trimmed);

/* Stop editing */

$server = DB_HOST;
$loginsql = DB_USER;
$passsql = DB_PASSWORD;
$base = DB_NAME;

define('ABSPATH', dirname(__FILE__).'/');

// Get everything else
require_once(ABSPATH.'wp-settings.php');
?>
