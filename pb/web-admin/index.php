<?
/*
 * index.php:
 * Admin pages for PledgeBank.
 * 
 * Copyright (c) 2005 UK Citizens Online Democracy. All rights reserved.
 * Email: francis@mysociety.org. WWW: http://www.mysociety.org
 *
 * $Id: index.php,v 1.18 2007-09-22 11:18:03 francis Exp $
 * 
 */

# Don't redirect to promesobanko.com etc. See pb.php.
global $no_language_redirects;
$no_language_redirects = true;

require_once "../conf/general";
require_once "../phplib/admin-pb.php";
require_once "../../phplib/template.php";
require_once "../../phplib/admin-phpinfo.php";
require_once "../../phplib/admin-serverinfo.php";
require_once "../../phplib/admin-configinfo.php";
require_once "../../phplib/admin-embed.php";
require_once "../../phplib/admin.php";
require_once '../../services/Ratty/phplib/admin-ratty.php';

$pages = array(
    new ADMIN_PAGE_PB_LATEST,
    new ADMIN_PAGE_PB_MAIN,
    new ADMIN_PAGE_PB_STATS,
    new ADMIN_PAGE_EMBED('pbcsv', 'User CSV File', "person.csv"),
    null,
    new ADMIN_PAGE_RATTY(
        'pb-abuse',
	'Contact form abuse',
	'These rules apply to messages submitted through contact forms on PledgeBank. Currently only the Contact the Creator one.',
	<<<EOF
All abuses of the rules will simply be blocked for now.
EOF
    ),
    null, // space separator on menu
    new ADMIN_PAGE_SERVERINFO,
    new ADMIN_PAGE_CONFIGINFO,
    new ADMIN_PAGE_PHPINFO,
);

admin_page_display(str_replace("http://", "", OPTION_BASE_URL), $pages, new ADMIN_PAGE_PB_SUMMARY);

?>
