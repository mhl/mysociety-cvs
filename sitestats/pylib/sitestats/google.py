#
# google.py: Interfaces with google to extract blog posts and news
# articles with mentions of mySociety sites.
# Copyright (c) 2009 UK Citizens Online Democracy. All rights reserved.
# Email: louise@mysociety.org; WWW: http://www.mysociety.org/
#
# $Id: google.py,v 1.1 2009-06-01 15:04:38 louise Exp $
#
import urllib
from datetime import date, timedelta
import mysociety
import re

class Google:
    '''Interfaces with google'''

    def __init__(self, params={}):
        self.base_blog_search_url = mysociety.config.get('BASE_BLOG_SEARCH_URL')
        self.base_news_search_url = mysociety.config.get('BASE_NEWS_SEARCH_URL')
        self.default_period = 'week'
    
    def _date_params(self, period, end_date):
        if end_date == None:
            end_date = date.today()
        if period == None:
            period = self.default_period
        if period == 'week':
            start_date = end_date - timedelta(days=7)
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
        results_count = re.compile("Results <b>\d+</b> (?:-|&ndash;) <b>\d+</b> of about\s?<b>((\d|,)+)</b>")
        match = results_count.search(html)
        if match == None:
            raise Exception, "Can't find number of results"
        attributes = { 'results' : match.group(1)} 
        return attributes
    
    def _get_results(self, base_url, params, period=None, end_date=None):
        date_params = self._date_params(period, end_date)     
        params.update(date_params)
        query_url = base_url + '?' + urllib.urlencode(params)
        response = urllib.urlopen(query_url)
        results_page = response.read()
        result_attributes = self._parse_results(results_page)
        result_attributes['url'] = query_url
        return result_attributes
        
    def blogs(self, query, period=None, end_date=None):
        params = { 'as_q' : query }
        result_attributes = self._get_results(self.base_blog_search_url, params, period, end_date)
        return result_attributes
    
    def news(self, query, period=None, end_date=None):
        params = { 'q' : query }
        result_attributes = self._get_results(self.base_news_search_url, params, period, end_date)
        return result_attributes      