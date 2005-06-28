<?
// all.php:
// List all pledges.
//
// Copyright (c) 2005 UK Citizens Online Democracy. All rights reserved.
// Email: francis@mysociety.org. WWW: http://www.mysociety.org
//
// $Id: list.php,v 1.4 2005-06-28 22:31:05 matthew Exp $

require_once "../phplib/pb.php";
require_once '../phplib/fns.php';

require_once '../../phplib/importparams.php';

define('PAGE_SIZE', 50);

$err = importparams(
            array('offset', '/^(0|[1-9]\d*)$/', '', 0),
            array('sort', '/^(title|target|date|name|ref|creationtime|percentcomplete)$/', '', 'default'),
            array('type', '/^[a-z_]*$/', '', 'open')
        );
if ($err) {
    err(_('Illegal offset or sort parameter passed'));
}

page_header(_("All Pledges"), array('id'=>'all'));

if ($q_type == 'failed') {
    $open = '<'; $succeeded = '<';
    if ($q_sort == "default") $q_sort = "creationtime";
} elseif ($q_type == 'succeeded_closed') {
    $open = '<'; $succeeded = '>=';
    if ($q_sort == "default") $q_sort = "creationtime";
} elseif ($q_type == 'succeeded_open') {
    $open = '>='; $succeeded = '>=';
    if ($q_sort == "default") $q_sort = "date";
} else {
    $open = '>='; $succeeded = '<';
    if ($q_sort == "default") $q_sort = "percentcomplete";
}

$ntotal = db_getOne("
                select count(id)
                from pledges
                where pin is null
                    and confirmed
                    and date $open pb_current_date()
                    AND (SELECT count(*) FROM signers WHERE signers.pledge_id = pledges.id) $succeeded target
                    and pb_pledge_prominence(id) <> 'backpage'");
if ($ntotal < $q_offset) 
    $q_offset = $ntotal - PAGE_SIZE;

$sort_phrase = $q_sort;
if ($q_sort == 'creationtime' || $q_sort == 'created') {
    $sort_phrase .= " DESC";
}
if ($q_sort == 'percentcomplete') {
    $sort_phrase = "( 
                (SELECT count(*) FROM signers WHERE signers.pledge_id = pledges.id)::numeric
                / target) DESC";
}
$qrows = db_query("
        SELECT *, (SELECT count(*) FROM signers
                    WHERE signers.pledge_id = pledges.id) AS signers
            FROM pledges 
            WHERE confirmed 
            AND date $open pb_current_date() 
            AND pin IS NULL
            AND (SELECT count(*) FROM signers WHERE signers.pledge_id = pledges.id) $succeeded target 
            AND pb_pledge_prominence(id) <> 'backpage'
            ORDER BY $sort_phrase LIMIT ? OFFSET $q_offset", PAGE_SIZE);
/* PG bug: mustn't quote parameter of offset */

if ($q_type == 'open') {
    print h2(_("Pledges which need signers"));
} elseif ($q_type == 'succeeded_open') {
    print h2(_("Successful pledges, open to new signers"));
} elseif ($q_type == 'succeeded_closed') {
    print h2(_("Successful pledges, closed to new signers"));
} elseif ($q_type == 'failed') {
    print h2(_("Failed pledges"));
} 
$viewsarray = array('open'=>_('Open pledges'), 'succeeded_open'=>_('Successful open pledges'), 
    'succeeded_closed'=>_('Successful closed pledges'), 'failed' => _('Failed pledges'));
$views = "";
foreach ($viewsarray as $s => $desc) {
    if ($q_type != $s) $views .= "<a href=\"/list/$s\">$desc</a>"; else $views .= $desc;
    if ($s != 'failed') $views .= ' | ';
}

$sort = ($q_sort) ? '&amp;sort=' . $q_sort : '';
$off = ($q_offset) ? '&amp;offset=' . $q_offset : '';
$prev = '<span class="greyed">&laquo; '._('Previous page').'</span>'; $next = '<span class="greyed">'._('Next page').' &raquo;</span>';
if ($q_offset > 0) {
    $n = $q_offset - PAGE_SIZE;
    if ($n < 0) $n = 0;
    $prev = "<a href=\"all?offset=$n$sort\">&laquo; "._('Previous page')."</a>";
}
if ($q_offset + PAGE_SIZE < $ntotal) {
    $n = $q_offset + PAGE_SIZE;
    $next = "<a href=\"all?offset=$n$sort\">"._('Next page')." &raquo;</a>";
}
$navlinks = '<p align="center">' . $views . "</p>\n";
if ($ntotal > 0) {
    $navlinks .= '<p align="center" style="font-size: 89%">' . _('Sort by'). ': ';
    $arr = array(
                 'creationtime'=>_('Start date'), 
                 /* 'target'=>_('Target'), */
                 'date'=>_('Deadline'), 
                 'percentcomplete' => _('Percent signed'), 
                 );
    # Removed as not useful (search is better for these): 'ref'=>'Short name',
    # 'title'=>'Title', 'name'=>'Creator'
    foreach ($arr as $s => $desc) {
        if ($q_sort != $s) $navlinks .= "<a href=\"?sort=$s$off\">$desc</a>"; else $navlinks .= $desc;
        if ($s != 'percentcomplete') $navlinks .= ' | ';
    }
    $navlinks .= '</p> <p align="center">';
    $navlinks .= $prev . ' | '._('Pledges'). ' ' . ($q_offset + 1) . ' &ndash; ' . 
        ($q_offset + PAGE_SIZE > $ntotal ? $ntotal : $q_offset + PAGE_SIZE) . ' of ' .
        $ntotal . ' | ' . $next;
    $navlinks .= '</p>';
}
print $navlinks;

if ($ntotal > 0) {
    $c = 0;
    while (list($id) = db_fetch_row($qrows)) {
        $pledge = new Pledge(intval($id));
        $arr = array('class'=>"pledge-".$c%2, 'href' => $pledge->url_main() );
        if ($q_type == 'succeeded_closed' || $q_type == 'failed') $arr['closed'] = true;
        $pledge->render_box($arr);
        $c++;
    }
    if ($ntotal > PAGE_SIZE)
        print "<br style=\"clear: both;\">$navlinks";
} else {
    print p(_('There are currently none.'));
}

page_footer();

?>
