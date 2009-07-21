import unittest
from sitestats.newsletters.models import CommonBaseMeasuresNewsletter
from sitestats.newsletters import common
from tests import example_dir
from newsletter import  newsletter_date

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

    def blogs(self, site_name, site_url, period=None, date=None):
        if date == common.end_of_current_week():
            return {'url'     : 'http://test.host', 
                    'resultcount' : 78}
        else:
            return {'url'     : 'http://test.host', 
                    'resultcount' : 89}

    def news(self, site_name, site_url, period=None, date=None):
        if date == common.end_of_current_week():
            return {'url'     : 'http://test.host', 
                    'resultcount' : 98}
        else:
            return {'url'     : 'http://test.host', 
                    'resultcount' : 87}

class CommonBaseMeasuresNewsletterTests(unittest.TestCase):

    def setUp(self):
        self.sources = {'piwik'  : MockPiwik(),
                        'google' : MockGoogle()}
        self.base_measures = CommonBaseMeasuresNewsletter()
    
    def testDataRetrieved(self):
        
        base_measures = self.base_measures.get_data(self.sources['piwik'].sites()[1], self.sources, {})
        expected_base_measures = [{'current_value': 22, 'percent_change': '-60%', 'unit': ''}, 
                                  {'current_value': 33, 'percent_change': '-25%', 'unit': ''}, 
                                  {'current_value': 77, 'percent_change': '-11%', 'unit': '%'}, 
                                  {'current_value': 34, 'percent_change': '-11%', 'unit': '%'}, 
                                  {'current_value': 56, 'percent_change': '-11%', 'unit': '%'}, 
                                  {'current_value': 11, 'percent_change': '-83%', 'unit': ''}, 
                                  {'current_value': 12, 'percent_change': '-48%', 'unit': 's'}, 
                                  {'current_value': 98, 'link': 'http://test.host', 'percent_change': '+13%', 'unit': ''}, 
                                  {'current_value': 78, 'link': 'http://test.host', 'percent_change': '-12%', 'unit': ''}] 
        self.assertEqual(expected_base_measures, base_measures, 'get_data produces correct results for example')

    def testCommonRenderedToHTMLTemplateCorrectly(self):
        html = self.base_measures.render('html', self.sources, date=newsletter_date()).strip()
        expected_html = open(example_dir() + 'base_measures.html').read().strip()
        self.assertEqual(expected_html, html, 'render produces correct output in HTML for example data')

    def testCommonRenderedToTextTemplateCorrectly(self):
        text = self.base_measures.render('text', self.sources, date=newsletter_date()).strip()
        expected_text = open(example_dir() + 'base_measures.txt').read().strip()
        self.assertEqual(expected_text, text, 'render produces correct output in text for example data')

