#
# email.py: Sends emails giving statistics on mySociety sites
# Copyright (c) 2009 UK Citizens Online Democracy. All rights reserved.
# Email: louise@mysociety.org; WWW: http://www.mysociety.org/
#
# $Id: email.py,v 1.2 2009-06-02 18:14:24 louise Exp $
#

import sys
from piwik import Piwik
from google import Google
from formatting import render_table, format_cell_value
import common

def render_common_base_measures(format, piwik, google, date=None):
    """Returns the text for a common base measures email in text/html"""
    sites = piwik.sites()
    stats = base_measure_stats()
    rows = []
    stat_totals = {}
    for site_info in sites: 
        row = [site_info['name']]
        row += [ format_cell_value(format, cell) for cell in get_common_base_measures(site_info, piwik, google, stat_totals, date)]
        rows.append(row)

    headers = ['site']
    totals = []
    for (header, stat, unit, need_total) in stats['piwik'] + stats['google']:
        headers.append(header)
        total_val = stat_totals.get(header)
        if need_total:
            totals.append(total_val)
        else:
            totals.append('')
    rendered = render_table(format, headers, rows, totals)
        
    return rendered
    
def base_measure_stats():
    """Returns a dictionary keyed by data source whose values are lists of tuples. Each tuple consists of the name of a
    statistic to be gathered, the method on the source class to use to get it, the units string to be used in displaying it, 
    and whether a total should be generated for this statistic."""
    stats =  {'piwik'  : [('unique visitors', 'unique_visitors', '', False), 
                          ('visits', 'visits', '', False),
                          ('bounce rate', 'bounce_rate', '%', False), 
                          ('% from search', 'percent_visits_from_search', '%', False),
                          ('% from sites', 'percent_visits_from_sites', '%', False),
                          ('page views/visit', 'pageviews_per_visit', '', False),
                          ('time/visit', 'time_per_visit', 's', False)], 
              'google' : [('news articles', 'news', '', True), 
                          ('blog posts', 'blogs', '', True)]}
    return stats
    
def get_piwik_source_base_measures(site_id, piwik, statistics, row, totals, date):
    this_week_end = date or common.end_of_current_week()
    previous_week_end = common.end_of_previous_week(this_week_end)
    for header, statistic, unit, need_total in statistics:
        method = getattr(piwik, statistic)
        current = method(site_id=site_id, date=this_week_end)
        previous = method(site_id=site_id, date=previous_week_end)
        percent_change = common.percent_change(current, previous)
        cell_info = {'current_value'  : current, 
                     'percent_change' : percent_change, 
                     'unit'           : unit}
        row.append(cell_info)
        if need_total:
            total = totals.get(header, 0)
            totals[header] = total + current_count
    return row

def get_google_source_base_measures(site_name, google, statistics, row, totals, date):
    this_week_end = date or common.end_of_current_week()
    previous_week_end = common.end_of_previous_week(this_week_end)
    for header, statistic, unit, need_total in statistics:
        method = getattr(google, statistic)
        current_data = method(query=site_name, date=this_week_end)
        previous_data = method(query=site_name, date=previous_week_end)
        current_count = current_data['results']
        previous_count = previous_data['results']
        percent_change = common.percent_change(current_count, previous_count)
        cell_info = {'current_value'  : current_count, 
                     'percent_change' : percent_change, 
                     'unit'           : unit, 
                     'link'           : current_data['url']}
        row.append(cell_info)
        if need_total:
            total = totals.get(header, 0)
            totals[header] = total + current_count
    return row
    
def get_common_base_measures(site_info, piwik, google, totals, date=None):
    stats = base_measure_stats()
    row = []
    get_piwik_source_base_measures(site_info['id'], piwik, stats['piwik'], row, totals, date)
    get_google_source_base_measures(site_info['name'], google, stats['google'], row, totals, date)
    return row