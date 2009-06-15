#
# piwik.py: Interfaces with the piwik (http://piwik.org/) API to 
# extract website analytics data
#
# Copyright (c) 2009 UK Citizens Online Democracy. All rights reserved.
# Email: louise@mysociety.org; WWW: http://www.mysociety.org/
#
# $Id: piwik.py,v 1.4 2009-06-15 17:28:11 louise Exp $
#

import urllib
import simplejson
import mysociety

class Piwik:
    '''Interfaces with the Piwik API'''
    
    def __init__(self, params={}):
        self.api_key = mysociety.config.get('PIWIK_API_KEY')
        self.base_url = mysociety.config.get('PIWIK_BASE_URL')
        self.default_period = 'week'
        self.default_date = 'yesterday'
        self.default_format = 'JSON'
        self.referrers = {}
    
    def __api_result(self, params, result_type):
        query_url = self.base_url + '&' + urllib.urlencode(params)
        response = urllib.urlopen(query_url)
        result = simplejson.loads(response.read())
        if type(result) == type({}) and result.has_key('result') and result['result'] == 'error':
            message = "Error returned from piwik. Message: %s, query %s" % (result['message'], query_url)
            raise Exception, message
        if result_type == 'simple':
            value = result['value']
        else:
            value = result
        return value
        
    def __default_params(self):
        return {'token_auth' : self.api_key, 'format': self.default_format}
        
    def __visit_api_result(self, method, site_id, date, period):
        params = self.__default_params()
        visit_params = { 'method': 'VisitsSummary.' + method, 
                         'idSite': site_id, 
                         'date': date or self.default_date, 
                         'period': period or self.default_period }
        params.update(visit_params)
        result = self.__api_result(params, result_type='simple')
        return int(result)
    
    def __sites_api_result(self, method, site_id=None):
        params = self.__default_params()
        site_params = { 'method': 'SitesManager.' + method }
        if site_id:
            site_params['idSite'] = site_id
        params.update(site_params)
        return self.__api_result(params, result_type='structure')

    def __referrer_api_result(self, method, site_id, date, period):
        params = self.__default_params()
        referrer_params = { 'method': 'Referers.' + method, 
                            'idSite': site_id, 
                            'date': date or self.default_date, 
                            'period': period or self.default_period }    
        params.update(referrer_params)
        return self.__api_result(params, result_type='structure')
        
    def unique_visitors(self, site_id, period=None, date=None):
        '''Returns the unique visitors for a site in the period'''
        return self.__visit_api_result('getUniqueVisitors', site_id, date, period)

    def percent_visits_from_search(self, site_id, period=None, date=None):
        '''Returns the percentage of visits coming from search engines in the period'''
        search_visits = self.visits_from_search(site_id, period, date)
        visits = self.visits(site_id, period, date)
        return self.__percent(search_visits, visits)
        
    def percent_visits_from_sites(self, site_id, period=None, date=None):
        '''Returns the percentage of visits coming from websites in the period'''
        site_visits = self.visits_from_sites(site_id, period, date)
        visits = self.visits(site_id, period, date)
        return self.__percent(site_visits, visits)
        
    def visits_from_search(self, site_id, period=None, date=None):
        '''Returns the number of visits coming from search engines in the period'''
        return self.__get_visits_from('Search Engines', site_id, period, date)

    def visits_from_sites(self, site_id, period=None, date=None):
        '''Returns the number of visits coming from websites in the period'''
        return self.__get_visits_from('Websites', site_id, period, date)
  
    def __get_visits_from(self, source, site_id, period, date):
        key = "%s_%s_%s" % (site_id, period, date)
        if (not self.referrers.has_key(key)):
            self.referrers[key] = self.__referrer_api_result('getRefererType', site_id, date, period)
        for referrer in self.referrers[key]:
            if referrer['label'] == source:
                return referrer['nb_visits']
        return 0

    def __fraction(self, numerator, denominator):
        if numerator == 0:
            return 0
        fraction = float(numerator) / float(denominator)
        return fraction
    
    def __percent(self, numerator, denominator): 
        fraction = self.__fraction(numerator, denominator)
        percentage = fraction * 100
        return int(round(percentage, 0))
        
    def visits(self, site_id, period=None, date=None):
        '''Returns the visits to a site in the period'''
        return self.__visit_api_result('getVisits', site_id, date, period)
        
    def bounces(self, site_id, period=None, date=None):
        '''Returns the bounce count for a site in the period'''
        return self.__visit_api_result('getBounceCount', site_id, date, period)
        
    def actions(self, site_id, period=None, date=None):
        '''Returns the bounce count for a site in the period'''
        return self.__visit_api_result('getActions', site_id, date, period)
    
    def total_time(self, site_id, period=None, date=None):
        '''Returns the total time spent on a site in the period'''
        return self.__visit_api_result('getSumVisitsLength', site_id, date, period)
    
    def time_per_visit(self, site_id, period=None, date=None):
        '''Returns the time spent per visit to a site in the period'''
        total_time = self.total_time(site_id, period, date)
        visits = self.visits(site_id, period, date)
        time_per_visit = self.__fraction(total_time, visits)
        return int(round(time_per_visit, 0))

    def pageviews_per_visit(self, site_id, period=None, date=None):
        '''Returns the number of pageviews per visit to a site in the period'''
        actions = self.actions(site_id, period, date)
        visits = self.visits(site_id, period, date)
        pageviews_per_visit = self.__fraction(actions, visits)
        return round(pageviews_per_visit, 1)
        
    def bounce_rate(self, site_id, period=None, date=None):
        '''Returns the bounce rate for the site in the period'''
        bounces = self.bounces(site_id, period, date)
        visits = self.visits(site_id, period, date)
        bounce_fraction = self.__fraction(bounces, visits)
        return self.__percent(bounces, visits)
    
    def site_ids(self):
        '''Returns a list of site ids'''
        site_id_lists = self.__sites_api_result('getAllSitesId')
        site_ids = [ int(site_id_list[0]) for site_id_list in site_id_lists ]
        return site_ids
        
    def site(self, site_id):
        '''Given a site id, returns a hash of information about the site in the form
        { 'id' : 1, 
          'name' : 'PledgeBank', 
          'main_url' : 'http://www.pledgebank.com',
          'ts_created': "2008-06-10 18:29:58", 
          'feedburnerName' : 'Piwik' }
        '''
        sites_list = self.__sites_api_result('getSiteFromId', site_id)
        site_info = sites_list[0]
        site_info['id'] = int(site_info['idsite'])
        del site_info['idsite']
        return site_info
        
    def sites(self):
        '''Returns a list of hashes of site information as returned by site()'''
        site_list = [self.site(site_id) for site_id in self.site_ids()]
        site_list.sort(lambda x, y: cmp(x['name'].lower, y['name'].lower()))
        site_list.reverse()
        return site_list