#
# fms_api.py: Interfaces with FixMyStreet to extract site statistics.
# Copyright (c) 2009 UK Citizens Online Democracy. All rights reserved.
# Email: louise@mysociety.org; WWW: http://www.mysociety.org/
#
# $Id: fms_api.py,v 1.1 2009-07-01 10:39:42 louise Exp $
#

import mysociety
import urllib
import simplejson
import source

class FMSApi(source.Source):
    '''Interfaces with FixMyStreet'''
    
    def __init__(self, params={}):
        self.base_url = mysociety.config.get('BASE_FMS_API_URL')
        
    def __api_result(self, entity, subtype, params):
        query_url = self.base_url + '/json/' + entity + '/' + subtype + '?' + urllib.urlencode(params)
        response = urllib.urlopen(query_url)
        result = simplejson.loads(response.read())
        return result
        
    def num_reports(self, start_date, end_date):
        params = {'start_date': start_date, 
                  'end_date'  : end_date}
        result = self.__api_result('problems', 'new', params)
        return len(result)