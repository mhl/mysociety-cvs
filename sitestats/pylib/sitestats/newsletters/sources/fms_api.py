#
# fms_api.py: Interfaces with FixMyStreet to extract site statistics.
# Copyright (c) 2009 UK Citizens Online Democracy. All rights reserved.
# Email: louise@mysociety.org; WWW: http://www.mysociety.org/
#
# $Id: fms_api.py,v 1.3 2009-07-01 15:34:44 louise Exp $
#

import mysociety
import urllib
import simplejson
import source

class FMSApi(source.Source):
    '''Interfaces with FixMyStreet'''
    
    def __init__(self, params={}):
        self.base_url = mysociety.config.get('BASE_FMS_API_URL')
        self.data = {}
        
    def __api_result(self, entity, subtype, params):
        query_url = self.base_url + '/json/' + entity + '/' + subtype + '?' + urllib.urlencode(params)
        response = urllib.urlopen(query_url)
        result =  response.read()
        result = simplejson.loads(result)
        return result
    
    def __get_data(self, entity, subtype, start_date, end_date): 
        key = "%s_%s_%s_%s" % (entity, subtype, start_date, end_date)
        if not self.data.has_key(key):
             params = {'start_date': start_date, 
                       'end_date'  : end_date}
             self.data[key] = self.__api_result(entity, subtype, params)
        return self.data[key]

    def num_reports(self, start_date, end_date):
        problems = self.__get_data('problems', 'new', start_date, end_date)
        return len(problems)
        
    def num_fixes(self, start_date, end_date):
        problems = self.__get_data('problems', 'fixed', start_date, end_date)
        return len(problems)
    
    def __key_counts(self, key, data):
        counts = {}
        for item in data:
            value = item[key]
            counts[value] = counts.setdefault(value, 0) + 1
        return counts    
        
    def service_counts(self, start_date, end_date):
        problems = self.__get_data('problems', 'new', start_date, end_date)
        return self.__key_counts('service', problems)

    def category_counts(self, start_date, end_date):
        problems = self.__get_data('problems', 'new', start_date, end_date)
        return self.__key_counts('category', problems)
    
    def council_counts(self, start_date, end_date):
        problems = self.__get_data('problems', 'new', start_date, end_date)
        council_counts = {}
        for problem in problems:
            councils = problem['council']
            council_list = councils.split(' and ')
            for council in council_list:
                council_counts[council] = council_counts.setdefault(council, 0) + 1
        return council_counts
        
    def top_councils(self, start_date, end_date, limit=10):
        council_counts = self.council_counts(start_date, end_date)
        return self.get_top_n(council_counts, limit=limit, keep_values=True)
        
    def top_categories(self, start_date, end_date, limit=10):
        category_counts = self.category_counts(start_date, end_date)
        return self.get_top_n(category_counts, limit=limit, keep_values=True)     
            