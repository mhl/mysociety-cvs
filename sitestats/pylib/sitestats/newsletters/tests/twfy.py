import unittest
from sitestats.newsletters.models.twfy import TWFYNewsletter
from sitestats.newsletters.models.newsletter import *
from sitestats.newsletters import common
from tests import example_dir
from datetime import date

class MockPiwik:

    def __init__(self, test_date):
        self.test_date = test_date
        
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

    def sites_without_twfy(self):
        return [{ 'id'             : 1, 
                  'name'           : 'PledgeBank', 
                  'main_url'       : 'http://www.pledgebank.com',
                  'ts_created'     : "2008-06-10 18:29:58", 
                  'feedburnerName' : 'Piwik' }]
    
              
    def visits(self, site_id, period=None, date=None):
        if date == 'previous1':
            return 33
        elif date == 'previous4':
             return 91
        elif date == 'prior4':
            return 76
        else:
            return 44

    def unique_visitors(self, site_id, period=None, date=None):
        if date == 'previous1':
            return 22
        elif date == 'previous4':
             return 98
        elif date == 'prior4':
             return 77
        else: 
            return 55

    def pageviews_per_visit(self, site_id, period=None, date=None):
        if date == 'previous1':
            return 11
        elif date == 'previous4':
             return 97
        elif date == 'prior4':
             return 78
        else:
            return 66

    def bounce_rate(self, site_id, period=None, date=None):
        if date == 'previous1':
            return 77
        elif date == 'previous4':
             return 96
        elif date == 'prior4':
              return 79
        else:
            return 88

    def time_per_visit(self, site_id, period=None, date=None):
        if date == 'previous1':
            return 12
        elif date == 'previous4':
             return 95
        elif date == 'prior4':
             return 79
        else:
            return 23

    def percent_visits_from_search(self, site_id, period=None, date=None):
        if date == 'previous1':
            return 34
        elif date == 'previous4':
             return 94
        elif date == 'prior4':
             return 80
        else:
            return 45

    def percent_visits_from_sites(self, site_id, period=None, date=None):
        if date == 'previous1':
            return 56
        elif date == 'previous4':
             return 93
        elif date == 'prior4':
             return 81
        else:
            return 67

    def percent_visits_from_direct_access(self, site_id, period=None, date=None):
        if date == 'previous1':
            return 12
        elif date == 'previous4':
             return 13
        elif date == 'prior4':
             return 23
        else:
            return 43

    def percent_visits_from_parliament(self, site_id, period=None, date=None):
        if date == 'previous1':
            return 22
        elif date == 'previous4':
             return 23
        elif date == 'prior4':
             return 9
        else:
            return 33

    def visitors_from_parliament(self, site_id, period=None, date=None):
        if date == 'previous1':
            return 24
        elif date == 'previous4':
             return 25
        elif date == 'prior4':
             return 3
        else:
            return 12
            
class TWFYNewsletterTests(unittest.TestCase):

    def setUp(self):
        self.test_date = date(2009,10,1)
        self.sources = {'piwik'  : MockPiwik(self.test_date)}
        self.twfy = TWFYNewsletter()

    def testShouldRaiseErrorIfTWFYNotFound(self):
        self.sources['piwik'].sites = self.sources['piwik'].sites_without_twfy
        self.assertRaises(NewsletterException, self.twfy.render, 'html', self.sources)
        
    def testDataRetrievedForUniqueVisitors(self):
        data = self.twfy.get_traffic_data('unique_visitors', self.sources, date=self.test_date)
        expected_data = [22, 
                         {'percent_change' : '-60%', 'previous_value' : 55}, 
                         98,
                         {'percent_change' : '+27%', 'previous_value' : 77}] 
        self.assertEqual(expected_data, data, 'get_data produces correct results for unique_visitors example')
        
    def testRenderedToHTMLTemplateCorrectly(self):
        html = self.twfy.render('html', self.sources, date = self.test_date).strip()
        expected_html = open(example_dir() + 'twfy.html').read().strip()
        self.assertEqual(expected_html, html, 'render produces correct output in HTML for example data')
        
    def testRenderedToTextTemplateCorrectly(self):
        text = self.twfy.render('text', self.sources, date = self.test_date).strip()
        expected_text = open(example_dir() + 'twfy.txt').read().strip()
        self.assertEqual(expected_text, text, 'render produces correct output in text for example data')