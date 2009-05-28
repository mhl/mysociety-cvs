import sys
import unittest
sys.path.append("../../pylib")
import piwik

#---

class SimpleApiUrl:
    '''An object whose read method returns a json string containing the value the SimpleApiUrl was initialized with (jsonified if an int value)'''
    def __init__(self, value):
       self.value = value
       
    def read(self):
        if type(self.value) == int:
            return '{"value":%d}' % self.value
        else:
            return self.value
#---

class PiwikTests(unittest.TestCase):
    
    def setUp(self):
        self.piwik = piwik.Piwik()
        
    def fake_api_response(self, value):
        mock_api = SimpleApiUrl(value)
        piwik.urllib.urlopen = lambda url: mock_api
            
    def testUniqueVisitors(self):
        self.fake_api_response(4)
        visitors = self.piwik.unique_visitors(1)
        self.assertEqual(4, visitors, "unique_visitors returns the expected number of visitors")
        
    def testVisits(self):
        self.fake_api_response(5)
        visits = self.piwik.visits(1)
        self.assertEqual(5, visits, "visits returns the expected number of visitors") 
           
    def testBounces(self):
        self.fake_api_response(6)
        bounces = self.piwik.bounces(1)
        self.assertEqual(6, bounces, "bounces returns the expected number of bounces")
 
    def testActions(self):
       self.fake_api_response(7)
       actions = self.piwik.actions(1)
       self.assertEqual(7, actions, "actions returns the expected number of actions") 
         
    def testTotalTime(self):
        self.fake_api_response(8)
        bounces = self.piwik.total_time(1)
        self.assertEqual(8, bounces, "total_time returns the expected time")    
    
    def testTimePerVisit(self):
        self.piwik.total_time = lambda site_id, period, date: 25
        self.piwik.visits = lambda site_id, period, date: 100
        time_per_visit = self.piwik.time_per_visit(1)
        self.assertEqual(0.25, time_per_visit, "time_per_visit returns the expected time per visit")         
    
    def testPageviewsPerVisit(self):
        self.piwik.actions = lambda site_id, period, date: 25
        self.piwik.visits = lambda site_id, period, date: 100
        pageviews_per_visit = self.piwik.pageviews_per_visit(1)
        self.assertEqual(0.25, pageviews_per_visit, "pageviews_per_visit returns the expected pageviews per visit")
    
    def testBounceRate(self):
        self.piwik.bounces = lambda site_id, period, date: 25
        self.piwik.visits = lambda site_id, period, date: 100
        bounce_rate = self.piwik.bounce_rate(1)
        self.assertEqual(0.25, bounce_rate, "bounce_rate returns the expected time bounce rate")
        
    def testSiteIds(self):
        self.fake_api_response('[["1"],["2"],["3"]]')
        site_ids = self.piwik.site_ids()     
        self.assertEqual([1, 2, 3], site_ids, "sites returns the expected sites")
    
    def testSite(self):
        self.fake_api_response('[{"idsite":"1","name":"PledgeBank","main_url":"http:\/\/www.pledgebank.com","ts_created":"2008-06-10 18:29:58","feedburnerName":"Piwik"}]')
        site_info = self.piwik.site(1)
        expected_info = { 'id' : 1, 
                          'name' : 'PledgeBank', 
                          'main_url' : 'http://www.pledgebank.com',
                          'ts_created': "2008-06-10 18:29:58", 
                          'feedburnerName' : 'Piwik' }
        self.assertEqual(expected_info, site_info, 'site returns hash of site info')
    
    def testSites(self):
        self.fake_api_response('[["1"],["2"]]')
        self.piwik.site = lambda site_id: {'test': 'value'}
        sites = self.piwik.sites()
        self.assertEqual([{'test': 'value'}, {'test': 'value'}], sites, 'sites returns hashes of site info for all sites')
        
def main():
    unittest.main()

if __name__ == '__main__':
    main()
