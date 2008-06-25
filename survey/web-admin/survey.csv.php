<?php
/*
 * survey.csv.php:
 * CVS download of survey results from admin page.
 * 
 * Copyright (c) 2008 UK Citizens Online Democracy. All rights reserved.
 * Email: francis@mysociety.org; WWW: http://www.mysociety.org
 *
 * $Id: survey.csv.php,v 1.1 2008-06-25 11:44:44 francis Exp $
 * 
 */

require_once "../conf/general";
require_once "../../phplib/error.php";
require_once "../../phplib/db.php";
require_once "../../phplib/utility.php";
require_once "../../phplib/auth.php";

function survey_handle_error($num, $message, $file, $line, $context) {
    print("<strong>$message</strong> in $file:$line");
    return;
}
err_set_handler_display('survey_handle_error');

db_connect();

function get_column_names() {
    $columns = array();
    $q = db_query('select key from data_item group by key');
    while ($r = db_fetch_row($q)) {
        $columns[] = $r[0];
    }
    sort($columns);
    return $columns;
}

// Originally (at least) for Live Simply Promise
// Updated to follow RFC better (escape with double quotes, rather than backslash)
function escape_csv($v) {
    $v = str_replace('"', '""', $v);
    return '"'.$v.'"';
}


function all_data_print_row($columns, $values) {
    foreach ($columns as $column) {
        if (array_key_exists($column, $values)) {
            $value = $values[$column];
        } else {
            $value = "";
        }
        print escape_csv($value) . ",";
    }
    print "\n";
}

function csv_all_data() {
    header("Content-Type: application/csv; charset=utf-8");

    // print column headings
    $columns = get_column_names();
    array_unshift($columns, "batch");
    foreach ($columns as $column) {
        print escape_csv($column) . ",";
    }
    print "\n";

    // print data
    $q = db_query('select batch, key, value from data_item order by batch, random()');
    $values = array();
    $lastbatch = "";
    while ($r = db_fetch_row($q)) {
        list($batch, $key, $value) = $r;
        if ($batch != $lastbatch) {
            if ($lastbatch != "")
                all_data_print_row($columns, $values);
            $values = array('batch' => $batch);
            $lastbatch = $batch;
        }
        $values[$key] = $value;
    }
    all_data_print_row($columns, $values);
    sort($columns);
}

csv_all_data();


