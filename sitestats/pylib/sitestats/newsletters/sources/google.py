#
# google.py: Interfaces with google to extract blog posts and news
# articles with mentions of mySociety sites.
# Copyright (c) 2009 UK Citizens Online Democracy. All rights reserved.
# Email: louise@mysociety.org; WWW: http://www.mysociety.org/
#
# $Id: google.py,v 1.4 2009-06-30 09:26:55 louise Exp $
#
import urllib
import feedparser
import mysociety
import re
from sitestats.newsletters import common
import source

class AppURLopener(urllib.FancyURLopener):
    version = "sitestats/google.py v1.0"

urllib._urlopener = AppURLopener()

class GoogleResult:
    
    def __init__(self, title, content, link):
        self.title = title
        self.content = content
        self.link = link
    
class Google(source.Source):
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
                   'as_drrb' : 'b', 
                   'output'  : 'atom', 
                   'num'     : 1000, 
                   'scoring' : 'r' }
        return params
        
    def _parse_results(self, url):
        content = urllib.urlopen(url).read()
        feed = feedparser.parse(content)
        results = []
        for entry in feed['entries']:
            result = GoogleResult(link=entry['link'], 
                                  content=entry['content'][0]['value'], 
                                  title=entry['title'])
            results.append(result)
        attributes = {'resultcount' : len(feed['entries']), 
                      'results'     : results}
        return attributes
    
    def _get_results(self, base_url, params, period=None, date=None):
        date_params = self._date_params(period, date)     
        params.update(date_params)
        query_url = base_url + '?' + urllib.urlencode(params)
        result_attributes = self._parse_results(query_url)
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