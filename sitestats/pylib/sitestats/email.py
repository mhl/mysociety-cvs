#
# email.py: Sends emails giving statistics on mySociety sites
# Copyright (c) 2009 UK Citizens Online Democracy. All rights reserved.
# Email: louise@mysociety.org; WWW: http://www.mysociety.org/
#
# $Id: email.py,v 1.1 2009-06-01 18:16:30 louise Exp $
#

from piwik import Piwik
from django.template.loader import render_to_string
import common
 
def common_base_measures(format):
    """Returns the text for a common base measures email in text/html"""
    
    piwik = Piwik()
    sites = piwik.sites()
    for site_info in sites: 
        print site_info['name']
        
     # rendered = render_to_string('common_base_measures.html', { 'foo': 'bar' })
    
def base_measure_stats():
    stats =  {'piwik'  : ['unique_visitors', 
                          'visits', 
                          'bounce_rate', 
                          'percent_visits_from_search', 
                          'percent_visits_from_sites',
                          'pageviews_per_visit', 
                          'time_per_visit'], 
              'google' : []}
    return stats
    
def get_common_base_measures(site_id, piwik, google):
    this_week_end = common.end_of_current_week()
    previous_week_end = common.end_of_previous_week()
    data = {}
    
    piwik_statistics = base_measure_stats()['piwik']
    for statistic in piwik_statistics:
        method = getattr(piwik, statistic)
        data[statistic] = {}
        data[statistic]['current'] = method(date=this_week_end)
        data[statistic]['previous'] = method(date=previous_week_end)
        
    return data