#
# google.py: Interfaces with google to extract blog posts and news
# articles with mentions of mySociety sites.
# Copyright (c) 2009 UK Citizens Online Democracy. All rights reserved.
# Email: louise@mysociety.org; WWW: http://www.mysociety.org/
#
# $Id: google.py,v 1.1 2009-06-03 17:01:43 louise Exp $
#
import urllib

class AppURLopener(urllib.FancyURLopener):
    version = "sitestats/google.py v1.0"

urllib._urlopener = AppURLopener()

import mysociety
import re
from sitestats.newsletters import common

class Google:
    '''Interfaces with google'''

    def __init__(self, params={}):
        self.base_blog_search_url = mysociety.config.get('BASE_BLOG_SEARCH_URL')
        self.base_news_search_url = mysociety.config.get('BASE_NEWS_SEARCH_URL')
        self.default_period = 'week'
    
    def _date_params(self, period, end_date):
        if end_date == None:
            end_date = common.end_of_current_week()
        if period == None:
            period = self.default_period
        if period == 'week':
            start_date = common.start_of_week(end_date)
        else:
            raise NotImplementedError, period + ' interval not implemented in date_params'
        params = { 'as_mind' : start_date.day, 
                   'as_minm' : start_date.month, 
                   'as_miny' : start_date.year, 
                   'as_maxd' : end_date.day,
                   'as_maxm' : end_date.month, 
                   'as_maxy' : end_date.year,
                   'as_drrb' : 'b' }
        return params
 
    def _parse_news_results(self, html):
        attributes = {}
        return attributes 
        
    def _parse_results(self, html):
        results_count = re.compile("Results <b>\d+</b> (?:-|&ndash;) <b>\d+</b> of (?:about)?\s?<b>((\d|,)+)</b>")
        match = results_count.search(html)
        if match:
            attributes = { 'results' : int(match.group(1))} 
        else:
            no_results = re.compile('did not match any documents')
            match = no_results.search(html)
            if match:
                attributes = {'results' : 0 }
            else:
                print html
                raise Exception, "Can't find number of results"
        return attributes
    
    def _get_results(self, base_url, params, period=None, date=None):
        date_params = self._date_params(period, date)     
        params.update(date_params)
        query_url = base_url + '?' + urllib.urlencode(params)
        response = urllib.urlopen(query_url)
        results_page = response.read()
        result_attributes = self._parse_results(results_page)
        result_attributes['url'] = query_url
        return result_attributes
        
    def _query(self, site_name):
        site_name = site_name.lower()
        queries = { 'fixmystreet'    : 'NeighbourhoodFixIt OR FixMyStreet', 
                    'writetothem'    : 'faxyourmp OR writetothem'}
        return queries.get(site_name, site_name)
    
    def blogs(self, site_name, period=None, date=None):
        params = { 'as_q' : self._query(site_name) }
        result_attributes = self._get_results(self.base_blog_search_url, params, period, date)
        return result_attributes
    
    def news(self, site_name, period=None, date=None):
        params = { 'q' : self._query(site_name) }
        result_attributes = self._get_results(self.base_news_search_url, params, period, date)
        return result_attributes      