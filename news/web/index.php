<?php
/*
 * index.php:
 * newsdemo index page.
 * 
 * Copyright (c) 2006 UK Citizens Online Democracy. All rights reserved.
 * Email: louise.crow@gmail.com. WWW: http://www.mysociety.org
 *
 * $Id: index.php,v 1.1 2006-12-05 13:25:18 louise Exp $
 * 
 */

require_once "../../phplib/utility.php";
require_once "../phplib/news.php";
require_once "../phplib/page.php";

page_header("Index page for news demo");
news_general_heading();
index_page();
page_footer();

function index_page(){
?>
<form id="search" accept-charset="utf-8" action="/search" method="get">
<p><label for="q"><?=_('Search') ?>:</label>
<input type="text" id="q" name="q" size="25" value=""> <input type="submit" value="<?=_('Go') ?>"></p>
</form>

<?
}
?>