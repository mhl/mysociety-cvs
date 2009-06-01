import sys
import unittest
sys.path.append("../../../pylib")
from sitestats import email
from sitestats import piwik
from sitestats import common

class DummyPiwik:
    
    def visits(site_id, date):
        if date == common.end_of_current_week():
            return '33'
        else:
            return '44'
            
    def unique_visitors(site_id, date):
        if date == common.end_of_current_week():
            return '22'
        else: 
            return '55'
    
    def pageviews_per_visit(site_id, date):
        if date == common.end_of_current_week():
            return '11'
        else:
            return '66'
            
    def bounce_rate(site_id, date):
        if date == common.end_of_current_week():
            return '77'
        else:
            return '88'
    
    def time_per_visit(site_id, date):
        if date == common.end_of_current_week():
            return '12'
        else:
            return '23'
    
    def percent_visits_from_search(site_id, date):
        if date == common.end_of_current_week():
            return '34'
        else:
            return '45'

    def percent_visits_from_sites(site_id, date):
        if date == common.end_of_current_week():
            return '56'
        else:
            return '67'
                                    
class EmailTests(unittest.TestCase):
    
    def testCommonBaseMeasures(self):
        base_measures = email.get_common_base_measures(1, DummyPiwik(), None)
        expected_base_measures = {'visits' :
                                    {'current'  : '33', 
                                     'previous' : '44'}, 
                                  'unique_visitors' :
                                    {'current'  : '22', 
                                     'previous' : '55'}, 
                                  'pageviews_per_visit' :
                                    {'current'  : '11', 
                                     'previous' : '66'},
                                  'bounce_rate' :
                                    {'current'  : '77', 
                                     'previous' : '88'},
                                  'time_per_visit' :
                                    {'current'  : '12', 
                                     'previous' : '23'},
                                  'percent_visits_from_search':
                                    {'current'  : '34', 
                                     'previous' : '45'},
                                   'percent_visits_from_sites':
                                     {'current'  : '56', 
                                      'previous' : '67'} }
                                                            
        self.assertEqual(expected_base_measures, base_measures, 'get_common_base_measures produces correct results for example')

def main():
    unittest.main()

if __name__ == '__main__':
    main()
