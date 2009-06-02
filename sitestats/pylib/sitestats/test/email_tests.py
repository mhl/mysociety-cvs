import sys
import unittest
sys.path.append("../../../pylib")
from datetime import date

from sitestats import email
from sitestats import piwik
from sitestats import google
from sitestats import common


class MockPiwik:
    
    def sites(self):
        return [{ 'id'             : 1, 
                  'name'           : 'PledgeBank', 
                  'main_url'       : 'http://www.pledgebank.com',
                  'ts_created'     : "2008-06-10 18:29:58", 
                  'feedburnerName' : 'Piwik' }, 
                { 'id'             : 2, 
                  'name'           : 'TheyWorkForYou', 
                  'main_url'       : 'http://www.theyworkforyou.com', 
                  'ts_created'     : "2008-06-10 18:29:58", 
                  'feedburnerName' : 'Piwik' }]
                  
    def visits(self, site_id, period=None, date=None):
        if date == common.end_of_current_week():
            return 33
        else:
            return 44
            
    def unique_visitors(self, site_id, period=None, date=None):
        if date == common.end_of_current_week():
            return 22
        else: 
            return 55
    
    def pageviews_per_visit(self, site_id, period=None, date=None):
        if date == common.end_of_current_week():
            return 11
        else:
            return 66
            
    def bounce_rate(self, site_id, period=None, date=None):
        if date == common.end_of_current_week():
            return 77
        else:
            return 88
    
    def time_per_visit(self, site_id, period=None, date=None):
        if date == common.end_of_current_week():
            return 12
        else:
            return 23
    
    def percent_visits_from_search(self, site_id, period=None, date=None):
        if date == common.end_of_current_week():
            return 34
        else:
            return 45

    def percent_visits_from_sites(self, site_id, period=None, date=None):
        if date == common.end_of_current_week():
            return 56
        else:
            return 67
                                    
class MockGoogle:
    
    def blogs(self, query, period=None, date=None):
        if date == common.end_of_current_week():
            return {'url'     : 'http://test.host', 
                    'results' : 78}
        else:
            return {'url'     : 'http://test.host', 
                    'results' : 89}
            
    def news(self, query, period=None, date=None):
        if date == common.end_of_current_week():
            return {'url'     : 'http://test.host', 
                    'results' : 98}
        else:
            return {'url'     : 'http://test.host', 
                    'results' : 87}
                                            
class EmailTests(unittest.TestCase):
    
    def setUp(self):
        self.piwik = MockPiwik()
        self.google = MockGoogle()    
        
    def testCommonBaseMeasuresDataRetrieved(self):
        base_measures = email.get_common_base_measures(self.piwik.sites()[1], self.piwik, self.google, {})
        expected_base_measures = [{'current_value': 22, 'percent_change': '-60%', 'unit': ''}, 
                                  {'current_value': 33, 'percent_change': '-25%', 'unit': ''}, 
                                  {'current_value': 77, 'percent_change': '-13%', 'unit': '%'}, 
                                  {'current_value': 34, 'percent_change': '-24%', 'unit': '%'}, 
                                  {'current_value': 56, 'percent_change': '-16%', 'unit': '%'}, 
                                  {'current_value': 11, 'percent_change': '-83%', 'unit': ''}, 
                                  {'current_value': 12, 'percent_change': '-48%', 'unit': 's'}, 
                                  {'current_value': 98, 'link': 'http://test.host', 'percent_change': '+13%', 'unit': ''}, 
                                  {'current_value': 78, 'link': 'http://test.host', 'percent_change': '-12%', 'unit': ''}] 
        self.assertEqual(expected_base_measures, base_measures, 'get_common_base_measures produces correct results for example')

    def testCommonBaseMeasuresRenderedToHTMLTemplateCorrectly(self):
        html = email.render_common_base_measures('html', self.piwik, self.google).strip()
        expected_html = open('base_measures.html').read().strip()
        self.assertEqual(expected_html, html, 'render_common_base_measures produces correct output in HTML for example data')

    def testCommonBaseMeasuresRenderedToTextTemplateCorrectly(self):
        text = email.render_common_base_measures('text', self.piwik, self.google).strip()
        expected_text = open('base_measures.txt').read().strip()
        self.assertEqual(expected_text, text, 'render_common_base_measures produces correct output in text for example data')

def main():
    unittest.main()

if __name__ == '__main__':
    main()
