<?
/*
 * index.php:
 * Admin pages for NeWs.
 * 
 * Copyright (c) 2006 UK Citizens Online Democracy. All rights reserved.
 * Email: louise.crow@gmail.com. WWW: http://www.mysociety.org
 *
 * $Id: news-admin.php,v 1.1 2006-12-05 13:59:08 louise Exp $
 * 
 */

require_once "../conf/general";
require_once "../phplib/news.php";
require_once "../phplib/admin-news.php";
require_once "../../phplib/admin.php";


$pages = array(
    new ADMIN_PAGE_NEWS_NEWSPAPERS,
);

admin_page_display("NeWs", $pages, new ADMIN_PAGE_NEWS_NEWSPAPERS);

?> 