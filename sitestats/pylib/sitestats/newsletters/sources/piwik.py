#
# piwik.py: Interfaces with the piwik (http://piwik.org/) API to 
# extract website analytics data
#
# Copyright (c) 2009 UK Citizens Online Democracy. All rights reserved.
# Email: louise@mysociety.org; WWW: http://www.mysociety.org/
#
# $Id: piwik.py,v 1.12 2009-06-18 17:48:11 louise Exp $
#

import urllib
import simplejson
import mysociety
import re

class Piwik:
    '''Interfaces with the Piwik API'''
    
    def __init__(self, params={}):
        self.api_key = mysociety.config.get('PIWIK_API_KEY')
        self.base_url = mysociety.config.get('PIWIK_BASE_URL')
        self.default_period = 'week'
        self.default_date = 'yesterday'
        self.default_format = 'JSON'
        self.referrers = {}
        self.providers = {}
        self.visit_summaries = {}
        self.referring_sites = {}
        self.results_to_keep = None

    def prior_date(self, params):
        '''Workaround for a limitation in the params piwik accepts. It won't return a number of periods back 
        from any given date so, rewrite params so that a request with a date 'prior4' - the four intervals before 
        the previous four - is rewritten to a request for 'previous8' with a filter on the number of result 
        structures to be returned'''
        if params.has_key('date') and isinstance(params['date'], basestring) and params['date'].startswith('prior'):
            self.results_to_keep = int(re.search('\d+', params['date']).group(0))
            params['date'] = 'previous%s' % (self.results_to_keep * 2)
            return True
        else:
            return False
    
    def filter_for_prior(self, result):
        periods = result.keys()
        periods.sort()
        periods = periods[:self.results_to_keep]
        prior_result = {}
        for period in periods:
            prior_result[period] = result[period]
        self.results_to_keep = None
        return prior_result      
              
    def __api_result(self, params, result_type):
        prior_date =  self.prior_date(params)          
        query_url = self.base_url + '&' + urllib.urlencode(params)
        response = urllib.urlopen(query_url)
        result = simplejson.loads(response.read())
        if type(result) == type({}) and result.has_key('result') and result['result'] == 'error':
            message = "Error returned from piwik. Message: %s, query %s" % (result['message'], query_url)
            raise Exception, message
        if prior_date:
            result = self.filter_for_prior(result)
        return result
        
    def __default_params(self):
        return {'token_auth' : self.api_key, 'format': self.default_format}
        
    def __get_visit_summaries_api_result(self, site_id, date, period):
        params = self.__default_params()
        visit_params = { 'method': 'VisitsSummary.get', 
                         'idSite': site_id, 
                         'date': date, 
                         'period': period }
        params.update(visit_params)
        result = self.__api_result(params, result_type='structure')
        return result
        
    def __get_value_from_nested_hash(self, hash, key):
        '''Either get the value associated with the key in a simple hash, or in a hash of hashes, sum the 
        values associated with the key in the sub hashes. '''
        value = None
        if hash.has_key(key):
            value = hash[key]
        else:
            value = sum([sub_hash[key] for sub_hash_key, sub_hash in hash.items()])
        return value
    
    def __key(self, site_id, period, date): 
        return "%s_%s_%s" % (site_id, period, date)
        
    def __visit_summaries_api_result(self, key, site_id, date, period):
        period = period or self.default_period
        date = date or self.default_date
        summary_key = self.__key(site_id, period, date)
        # get the summary containing this data if we don't have it
        if (not self.visit_summaries.has_key(summary_key)):
            self.visit_summaries[summary_key] = self.__get_visit_summaries_api_result(site_id, date, period)
        value = self.__get_value_from_nested_hash(self.visit_summaries[summary_key], key)
        return value
        
    def __provider_api_result(self, method, site_id, date, period):
        params = self.__default_params()
        referrer_params = { 'method': 'Provider.' + method, 
                            'idSite': site_id, 
                            'date': date or self.default_date, 
                            'period': period or self.default_period }    
        params.update(referrer_params)
        return self.__api_result(params, result_type='structure')
        
    def __sites_api_result(self, method, site_id=None):
        params = self.__default_params()
        site_params = { 'method': 'SitesManager.' + method }
        if site_id:
            site_params['idSite'] = site_id
        params.update(site_params)
        return self.__api_result(params, result_type='structure')

    def __referrer_api_result(self, method, site_id, date, period, sort_by=None, order=None):
        params = self.__default_params()
        referrer_params = { 'method': 'Referers.' + method, 
                            'idSite': site_id, 
                            'date': date or self.default_date, 
                            'period': period or self.default_period }    
        if sort_by:
            referrer_params['filter_sort_column'] = sort_by
        if order:
            referrer_params['filter_sort_order'] = order
        params.update(referrer_params)
        return self.__api_result(params, result_type='structure')

    def __percent_of_visits(self, number_of_visits, site_id, period, date):
        visits = self.visits(site_id, period, date)
        return self.__percent(number_of_visits, visits)
    
    def top_referrers(self, site_id, period=None, date=None, limit=10):
        '''Returns the top n referrers to the site in the period'''
        sort_by = 'nb_visits'
        order = 'desc'
        key = self.__key(site_id, period, date)
        if not self.referring_sites.has_key(key):
          self.referring_sites[key] = self.__referrer_api_result('getWebsites', site_id, date, period, sort_by, order)
        if limit:
            sites = self.referring_sites[key][:limit]
        else:
            sites = self.referring_sites[key]
        names = [site['label'] for site in sites]
        return names
        
    def visits_from_referrer(self, site_id, referrer, period=None, date=None):
        '''Number of visits coming from a referring site in the period'''
        key = self.__key(site_id, period, date)
        if not self.referring_sites.has_key(key):
            self.referring_sites[key] = self.__referrer_api_result('getWebsites', site_id, date, period)
        return self.__get_label_val(self.referring_sites[key], referrer, 'nb_visits')
        
    def percent_visits_from_referrer(self, site_id, referrer, period=None, date=None):
        '''Percentage of visits coming from a referring site in the period'''
        referrer_visits = self.visits_from_referrer(site_id, referrer, period, date)
        return self.__percent_of_visits(referrer_visits, site_id, period, date)

    def percent_visits_from_search(self, site_id, period=None, date=None):
        '''Returns the percentage of visits coming from search engines in the period'''
        search_visits = self.visits_from_search(site_id, period, date)
        return self.__percent_of_visits(search_visits, site_id, period, date)
        
    def percent_visits_from_sites(self, site_id, period=None, date=None):
        '''Returns the percentage of visits coming from websites in the period'''
        site_visits = self.visits_from_sites(site_id, period, date)
        return self.__percent_of_visits(site_visits, site_id, period, date)

    def percent_visits_from_direct_access(self, site_id, period=None, date=None):
        '''Returns the percentage of visits coming from direct access in the period'''
        direct_visits = self.visits_from_direct_access(site_id, period, date)
        return self.__percent_of_visits(direct_visits, site_id, period, date)

    def percent_visits_from_parliament(self, site_id, period=None, date=None):
        '''Returns the percentage of visits coming from direct access in the period'''
        parliament_visits = self.visits_from_parliament(site_id, period, date)
        return self.__percent_of_visits(parliament_visits, site_id, period, date)
        
    def visits_from_search(self, site_id, period=None, date=None):
        '''Returns the number of visits coming from search engines in the period'''
        return self.__get_visits_from('Search Engines', site_id, period, date)

    def visits_from_sites(self, site_id, period=None, date=None):
        '''Returns the number of visits coming from websites in the period'''
        return self.__get_visits_from('Websites', site_id, period, date)

    def visits_from_direct_access(self, site_id, period=None, date=None):
        '''Returns the number of visits coming from direct access in the period'''
        return self.__get_visits_from('Direct Entry', site_id, period, date) 
    
    def visits_from_parliament(self, site_id, period=None, date=None):
        '''Returns the number of visits coming from the Parliamentary domain in the period'''     
        return self.__get_visits_from_provider('Parliament', site_id, period, date)
    
    def visitors_from_parliament(self, site_id, period=None, date=None):
        '''Returns the number of visitors coming from the Parliamentary domain in the period'''  
        return self.__get_visitors_from_provider('Parliament', site_id, period, date)
    
    def __get_visits_from_provider(self, source, site_id, period, date):
        return self.__get_provider_data(site_id, date, period, source, 'nb_visits')

    def __get_visitors_from_provider(self, source, site_id, period, date):
        key = 'sum_daily_nb_uniq_visitors'
        if period == 'day':
            key = 'nb_uniq_visitors'
        return self.__get_provider_data(site_id, date, period, source, key)
        
    def __get_provider_data(self, site_id, date, period, source, value):
        key = self.__key(site_id, period, date)
        if (not self.providers.has_key(key)):
            self.providers[key] = self.__provider_api_result('getProvider', site_id, date, period)
        return self.__get_label_val(self.providers[key], source, value)   
     
    def __get_visits_from(self, source, site_id, period, date):
        key = self.__key(site_id, period, date)
        if (not self.referrers.has_key(key)):
            self.referrers[key] = self.__referrer_api_result('getRefererType', site_id, date, period)
        return self.__get_label_val(self.referrers[key], source, 'nb_visits')

    def __get_label_val(self, data, label, key):
        """If 'data' is a list of hashes, get the value keyed by 'key' from the hash where the value for the key 
        label is 'label'. If 'data' is a hash, operate recursively for every list of hashes in the hash values and 
        return the summed values. """
        # dict keyed on dates of lists of values
        if isinstance(data, dict):
            return sum([self.__get_label_val(subhash, label, key) for subhash in data.values()])
        # lists of values
        else:
            for item in data:
                if item['label'] == label:
                    return item[key]  
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
        return self.__visit_summaries_api_result('nb_visits', site_id, date, period)
        
    def bounces(self, site_id, period=None, date=None):
        '''Returns the bounce count for the site in the period'''
        return self.__visit_summaries_api_result('bounce_count', site_id, date, period)

    def unique_visitors(self, site_id, period=None, date=None):
        '''Returns the unique visitors for a site in the period'''
        return self.__visit_summaries_api_result('nb_uniq_visitors', site_id, date, period)
 
    def actions(self, site_id, period=None, date=None):
        '''Returns the bounce count for a site in the period'''
        return self.__visit_summaries_api_result('nb_actions', site_id, date, period)
    
    def total_time(self, site_id, period=None, date=None):
        '''Returns the total time spent on a site in the period'''
        return self.__visit_summaries_api_result('sum_visit_length', site_id, date, period)
    
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
