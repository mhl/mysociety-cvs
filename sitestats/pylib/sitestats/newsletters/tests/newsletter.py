import unittest
from sitestats.newsletters.models.newsletter import *
from sitestats.newsletters import common
from tests import example_dir
from datetime import date
from sitestats.newsletters.sources.google import GoogleResult

class MockPiwik:
 
    def sites(self):
        return [{ 'id'             : 1, 
                  'name'           : 'PledgeBank', 
                  'main_url'       : 'http://www.pledgebank.com',
                  'ts_created'     : "2008-06-10 18:29:58", 
                  'feedburnerName' : 'Piwik' }, 
                { 'id'             : 2, 
                  'name'           : 'FixMyStreet', 
                  'main_url'       : 'http://www.fixmystreet.com', 
                  'ts_created'     : "2008-06-10 18:29:58", 
                  'feedburnerName' : 'Piwik' },
                { 'id'             : 3, 
                  'name'           : 'TheyWorkForYou', 
                  'main_url'       : 'http://www.theyworkforyou.com', 
                  'ts_created'     : "2008-06-10 18:29:58", 
                  'feedburnerName' : 'Piwik' }]

    def empty_sites(self):
        return []
              
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
   
    def top_referrers(self, site_id, period=None, date=None, limit=None):
       return ['www.writetothem.com', 'en.wikipedia.org']
    
    def upcoming_search_keywords(self, site_id, period=None, date=None, limit=None):
        return ['stuff', 'more stuff']
        
    def percent_visits_from_referrer(self, site_id, referrer, period=None, date=None):
       if date == 'previous1':
           return 1
       elif date == 'previous4':
            return 2
       elif date == 'prior4':
            return 3
       else:
           return 4    
    
    def site_link(self, site_id, period=None, date=None):
        if date == 'previous4':
            return 'http://previous.4.link'
        else:
            return 'http://previous.1.link'   

    def top_roots_and_percent_visits(self, site_id, period=None, date=None, limit=10):
        return [('mp', 92),('mps', 1)] 

    def top_children(self, site_id, root, period=None, date=None, limit=None, exclude=[], include=[]):
        if root == 'mp':
            return ['anne_person', 'bob_person']
        elif root == 'wrans':
            return ['wrans_1', 'wrans_2']
        elif root == 'debates': 
            return ['debate_1', 'debate_2']
            
    def upcoming_children(self, site_id, root, period=None, date=None, limit=None, exclude=[], include=[]):
        if root == 'mp':
            return ['upcoming_anne_person', 'upcoming_bob_person']
        elif root == 'wrans':
            return ['upcoming_wrans_1', 'upcoming_wrans_2']
        elif root == 'debates': 
            return ['upcoming_debate_1', 'upcoming_debate_2']
        else:
            return ['internal stuff', 'more internal stuff']            

def newsletter_date():
    return date(2009, 1, 1)

class MockGoogle:

    def blogs(self, site_name, site_url, period=None, date=None):
        if date == newsletter_date():
            return {'url'         : 'http://test.host', 
                    'resultcount' : 78,
                    'results'     : [GoogleResult(title='blog one', link='http://one.example.com', content='Blog one content'),
                                     GoogleResult(title='blog two', link='http://two.example.com', content='Blog two content')]}
        else:
            return {'url'     : 'http://test.host', 
                    'resultcount' : 89}

    def news(self, site_name, site_url, period=None, date=None):
        if date == newsletter_date():
            return {'url'     : 'http://test.host', 
                    'resultcount' : 98,
                    'results'     : [GoogleResult(title='news one', link='http://one.example.com', content='News one content'),
                                     GoogleResult(title='news two', link='http://two.example.com', content='News two content')]}
        else:
            return {'url'     : 'http://test.host', 
                    'resultcount' : 87}      
                      
class NewsletterTests(unittest.TestCase):

    def setUp(self):
        self.sources = {'piwik'  : MockPiwik(), 'google' : MockGoogle()}
        self.newsletter = Newsletter()

    def testShouldRaiseErrorIfSiteNotFound(self):
        self.sources['piwik'].sites = self.sources['piwik'].empty_sites
        self.newsletter.site_name = 'test'
        self.assertRaises(NewsletterException, self.newsletter.set_site_id, self.sources)
        
    def testTrafficDataRetrievedForUniqueVisitors(self):
        data = self.newsletter.get_traffic_data('unique_visitors', self.sources, '%')
        expected_data = [{'current_value' : 22,
                          'unit' : '%'}, 
                         {'percent_change' : '-60%', 'previous_value' : 55}, 
                         {'current_value' : 98,
                          'unit' : '%'},
                         {'percent_change' : '+27%', 'previous_value' : 77}] 
        self.assertEqual(expected_data, data, 'get_data produces correct results for unique_visitors example')
