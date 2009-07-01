#
# twfy_api.py: Interfaces with TheyWorkForYou to extract site statistics.
# Copyright (c) 2009 UK Citizens Online Democracy. All rights reserved.
# Email: louise@mysociety.org; WWW: http://www.mysociety.org/
#
# $Id: twfy_api.py,v 1.3 2009-07-01 10:39:42 louise Exp $
#

import mysociety
import urllib
import simplejson
import source

class TWFYApi(source.Source):
    '''Interfaces with TheyWorkForYou'''
    
    def __init__(self, params={}):
        self.base_url = mysociety.config.get('BASE_TWFY_API_URL')
        self.api_key = mysociety.config.get('TWFY_API_KEY')
        self.default_params = { 'key' : self.api_key, 'output' : 'js' }
        
    def __api_result(self, method, request_params):
        params = self.default_params
        params.update(request_params)
        query_url = self.base_url + '/api/' + method + '?' + urllib.urlencode(params)
        response = urllib.urlopen(query_url)
        result = simplejson.loads(response.read(), encoding='latin_1')
        if type(result) == type({}) and result.has_key('error') :
            message = "Error returned from twfy_api. Message: %s, query %s" % (result['error'], query_url)
            raise Exception, message
        return result
        
    def email_subscribers_count(self, start_date, end_date):
        params = {'start_date': start_date, 
                  'end_date'  : end_date}
        result = self.__api_result('getAlerts', params)
        total_alerts = 0
        for alert_hash in result["alerts"]:
            total_alerts += int(alert_hash["count"])
        return total_alerts
        
    def top_email_subscriptions(self, start_date, end_date, limit=10):
        params = {'start_date': start_date, 
                  'end_date'  : end_date}
        result = self.__api_result('getAlerts', params)
        criteria_counts = {}
        for alert_hash in result["alerts"]:
            criteria_counts[alert_hash['criteria']] = int(alert_hash['count'])
        return self.get_top_n(criteria_counts, limit)
        
    def person_name(self, person_id):
        params = {'id' : person_id}
        result = self.__api_result('getPerson', params)
        most_recent = result[0]
        return most_recent['full_name']
    
    def top_comment_pages(self, start_date, end_date, limit=10):
        params = {'start_date': start_date, 
                  'end_date'  : end_date}
        result = self.__api_result('getComments', params)
        url_counts = {}
        for comment_hash in result["comments"]:
            page = comment_hash['url'].split('#')[0]
            count = url_counts.setdefault(page, 0)
            url_counts[page] += 1
        return self.get_top_n(url_counts, limit)
    