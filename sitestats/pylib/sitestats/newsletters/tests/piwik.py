from sitestats.newsletters.sources import piwik
import unittest

class SimpleApiUrl:
    '''An object whose read method returns a json string containing the value the SimpleApiUrl was initialized with (jsonified if an int value)'''
    def __init__(self, value):
       self.value = value

    def read(self):
        if type(self.value) == int:
            return '{"value":%d}' % self.value
        else:
            return self.value
            
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
        time = self.piwik.total_time(1)
        self.assertEqual(8, time, "total_time returns the expected time")    

    def testRaisesErrorWhenErrorReturned(self):
        self.fake_api_response("{'message': 'You are requesting a precise subTable but there is not such data in the Archive.', 'result': 'error'}")
        self.assertRaises(Exception, self.piwik.total_time, 1)

    def testTimePerVisit(self):
        self.piwik.total_time = lambda site_id, period, date: 100
        self.piwik.visits = lambda site_id, period, date: 33
        time_per_visit = self.piwik.time_per_visit(1)
        self.assertEqual(3, time_per_visit, "time_per_visit returns the expected time per visit")         

    def testPageviewsPerVisit(self):
        self.piwik.actions = lambda site_id, period, date: 33
        self.piwik.visits = lambda site_id, period, date: 99
        pageviews_per_visit = self.piwik.pageviews_per_visit(1)
        self.assertEqual(0.3, pageviews_per_visit, "pageviews_per_visit returns the expected pageviews per visit")

    def testBounceRate(self):
        self.piwik.bounces = lambda site_id, period, date: 33
        self.piwik.visits = lambda site_id, period, date: 99
        bounce_rate = self.piwik.bounce_rate(1)
        self.assertEqual(33, bounce_rate, "bounce_rate returns the expected time bounce rate")

    def testBounceRateWithZeroValues(self):
        self.piwik.bounces = lambda site_id, period, date: 0
        self.piwik.visits = lambda site_id, period, date: 0
        bounce_rate = self.piwik.bounce_rate(1)
        self.assertEqual(0, bounce_rate, "bounce_rate returns zero for zero values")
            
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
        self.piwik.site = lambda site_id: {  'name' : str(site_id) }
        sites = self.piwik.sites()
        self.assertEqual([{'name': '1'}, {'name': '2'}], sites, 'sites returns hashes of site info for all sites sorted by name')

    def testVisitorsFromSearch(self):
        self.fake_api_response('[{"label":"Search Engines","sum_daily_nb_uniq_visitors":350,"nb_visits":353,"nb_actions":506,"max_actions":23,"sum_visit_length":21751,"bounce_count":294,"nb_visits_converted":0},{"label":"Websites","sum_daily_nb_uniq_visitors":176,"nb_visits":184,"nb_actions":393,"max_actions":33,"sum_visit_length":42592,"bounce_count":129,"nb_visits_converted":0},{"label":"Direct Entry","sum_daily_nb_uniq_visitors":99,"nb_visits":138,"nb_actions":293,"max_actions":36,"sum_visit_length":22162,"bounce_count":107,"nb_visits_converted":0}]')
        visits_from_search = self.piwik.visits_from_search(1)
        self.assertEqual(353, visits_from_search, 'visits_from_search returns correct information from example')

    def testVisitorsFromSearchShouldReturnZeroIfNoSearchKey(self):
        self.fake_api_response('[{"label":"Websites","sum_daily_nb_uniq_visitors":176,"nb_visits":184,"nb_actions":393,"max_actions":33,"sum_visit_length":42592,"bounce_count":129,"nb_visits_converted":0},{"label":"Direct Entry","sum_daily_nb_uniq_visitors":99,"nb_visits":138,"nb_actions":293,"max_actions":36,"sum_visit_length":22162,"bounce_count":107,"nb_visits_converted":0}]')
        visits_from_search = self.piwik.visits_from_search(1)
        self.assertEqual(0, visits_from_search, 'visits_from_search returns zero when key "Search Engines" is not present')        
        
    def testVisitorsFromSites(self):
        self.fake_api_response('[{"label":"Search Engines","sum_daily_nb_uniq_visitors":350,"nb_visits":353,"nb_actions":506,"max_actions":23,"sum_visit_length":21751,"bounce_count":294,"nb_visits_converted":0},{"label":"Websites","sum_daily_nb_uniq_visitors":176,"nb_visits":184,"nb_actions":393,"max_actions":33,"sum_visit_length":42592,"bounce_count":129,"nb_visits_converted":0},{"label":"Direct Entry","sum_daily_nb_uniq_visitors":99,"nb_visits":138,"nb_actions":293,"max_actions":36,"sum_visit_length":22162,"bounce_count":107,"nb_visits_converted":0}]')
        visits_from_sites = self.piwik.visits_from_sites(1)
        self.assertEqual(184, visits_from_sites, 'visits_from_sites returns correct information from example')

    def testPercentVisitsFromSearch(self):
        self.piwik.visits_from_search = lambda site_id, period, date: 33
        self.piwik.visits = lambda site_id, period, date: 99
        percent_from_search = self.piwik.percent_visits_from_search(1)
        self.assertEqual(33, percent_from_search, "percent_visits_from_search returns the expected figure")

    def testPercentVisitsFromSites(self):
        self.piwik.visits_from_sites = lambda site_id, period, date: 33
        self.piwik.visits = lambda site_id, period, date: 99
        percent_from_sites = self.piwik.percent_visits_from_sites(1)
        self.assertEqual(33, percent_from_sites, "percent_visits_from_sites returns the expected figure")
