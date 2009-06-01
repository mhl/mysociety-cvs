#
# piwik.py: Interfaces with the piwik (http://piwik.org/) API to 
# extract website analytics data
#
# Copyright (c) 2009 UK Citizens Online Democracy. All rights reserved.
# Email: louise@mysociety.org; WWW: http://www.mysociety.org/
#
# $Id: piwik.py,v 1.1 2009-06-01 15:04:38 louise Exp $
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
    
    def __api_result(self, params, result_type):
        query_url = self.base_url + '&' + urllib.urlencode(params)
        response = urllib.urlopen(query_url)
        result = simplejson.loads(response.read())
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
        return self.__api_result(params, result_type='simple')
    
    def __sites_api_result(self, method, site_id=None):
        params = self.__default_params()
        site_params = { 'method': 'SitesManager.' + method }
        if site_id:
            site_params['idSite'] = site_id
        params.update(site_params)
        return self.__api_result(params, result_type='structure')

    def unique_visitors(self, site_id, period=None, date=None):
        '''Returns the unique visitors for a site in the period'''
        return self.__visit_api_result('getUniqueVisitors', site_id, date, period)

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
        return float(total_time) / float(visits)

    def pageviews_per_visit(self, site_id, period=None, date=None):
        '''Returns the number of pageviews per visit to a site in the period'''
        actions = self.actions(site_id, period, date)
        visits = self.visits(site_id, period, date)
        return float(actions) / float(visits)
        
    def bounce_rate(self, site_id, period=None, date=None):
        '''Returns the bounce rate for the site in the period'''
        bounces = self.bounces(site_id, period, date)
        visits = self.visits(site_id, period, date)
        return float(bounces) / float(visits)
    
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
        return site_list