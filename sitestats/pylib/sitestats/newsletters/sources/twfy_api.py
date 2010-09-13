#
# twfy_api.py: Interfaces with TheyWorkForYou to extract site statistics.
# Copyright (c) 2009 UK Citizens Online Democracy. All rights reserved.
# Email: louise@mysociety.org; WWW: http://www.mysociety.org/
#
# $Id: twfy_api.py,v 1.7 2010-09-13 09:02:12 louise Exp $
#

import mysociety
import urllib
import simplejson
import source
import re

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
        result = response.read()
        result = simplejson.loads(result, encoding='latin_1')
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
        
    def top_email_subscriptions(self, start_date, end_date, limit=10, keep_values=True):
        params = {'start_date': start_date, 
                  'end_date'  : end_date}
        result = self.__api_result('getAlerts', params)
        criteria_counts = {}
        for alert_hash in result["alerts"]:
            criteria_counts[alert_hash['criteria']] = int(alert_hash['count'])
        return self.get_top_n(criteria_counts, limit, keep_values)
        
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
    
    def next_version_gid(self, gid):
        version = re.sub("(\d\d\d\d-\d\d-\d\d)(.)(\..*)", self.next_version, gid)
        return version
        
    def next_version(self, match):
        char_index = ord(match.group(2))
        return match.group(1) + chr(char_index + 1) + match.group(3)
    
    def page_title(self, gid, page_type, sub_type):
        result = []
        params = {'gid' : gid }
        # print "looking for %s" % gid
        if sub_type != '':
            params['type'] = sub_type

        if page_type in ['debates', 'debate']:
            api_function = 'getDebates'
        else:
            api_function = 'getWrans'

        try:
            result = self.__api_result(api_function, params)
        # TODO: API can return blank page. Should fix in TWFY API
        except ValueError:
            return None
	if 'redirect' in result:
            gid = result['redirect']
            params['gid'] = gid
            try:
                result = self.__api_result(api_function, params)
            except ValueError:
                return None
        title = self.__title_from_debate_list(result, gid, page_type)
        if title:
            return title
        return None

    def __title_from_debate_list(self, data, gid, page_type):
        for debate_hash in data:  
            if debate_hash['gid'] == gid:
                # Looking at a speech in a debate
                if page_type == 'debate':
                    return self.__debate_title_from_speech(debate_hash) 
                else:
                    return debate_hash['body']
        return None
                
    def __speaker_from_debate(self, data):
        """Get the speaker from a hash of debate info"""
        if data.has_key('speaker'):
            return data['speaker'].get('first_name', '') + ' ' + data['speaker'].get('last_name', '') 
        return None
    
    def __parent_gid_from_debate(self, data):
        """Get the parent gid from a hash of debate info"""
        if data.has_key('listurl'):
            listurl = data['listurl']
            match = re.search('\?id=(.*?)(&|$|#)', listurl)
            if match:
                return match.group(1)
        return None
    
    def __debate_title_from_speech(self, data):
        """Construct a title for a speech in a debate"""
        parent_gid = self.__parent_gid_from_debate(data)
        speaker = self.__speaker_from_debate(data)
        if parent_gid and speaker:
            debate_title = self.page_title(parent_gid, 'debates', 'commons')
            if debate_title: 
                return "%s speaking in %s" % (speaker, debate_title)
        return None
                
