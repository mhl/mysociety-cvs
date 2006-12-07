<?php
/*
 * index.php:
 * newsdemo index page.
 * 
 * Copyright (c) 2006 UK Citizens Online Democracy. All rights reserved.
 * Email: louise.crow@gmail.com. WWW: http://www.mysociety.org
 *
 * $Id: index.php,v 1.2 2006-12-07 15:55:17 louise Exp $
 * 
 */

require_once "../../phplib/utility.php";
require_once "../phplib/news.php";
require_once "../phplib/page.php";
$heading = "Contact your local newspaper";
page_header("NeWs - " . $heading);
print h2($heading);
index_page();
page_footer();

function index_page(){
?>
<form id="search" accept-charset="utf-8" action="/search" method="get"><div id="search-box">
<p><label for="q"><?=_('Type your town, postcode or the name of the paper you want to find') ?>:</label>
<input type="text" id="q" name="q" size="25" value=""> <input type="submit" value="<?=_('Go') ?>"></p>
</div></form>

<?
}
?>