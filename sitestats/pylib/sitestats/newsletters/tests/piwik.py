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
        
    def testPriorDateSetsDateParam(self):
        params = {'date' : 'prior1'}
        self.piwik.prior_date(params)
        self.assertEqual('previous2', params['date'], 'filter_for_prior correctly alters date param')
        
    def testPriorDateReturnsTrueWhenPrior(self):
        params = {'date' : 'prior1'}
        is_prior = self.piwik.prior_date(params)
        self.assertEqual(True, is_prior, 'filter_for_prior returns true when date is in "prior" form')
        
    def testPriorDateSetsResultsToKeep(self):
        params = {'date' : 'prior1'}
        self.piwik.prior_date(params)
        self.assertEqual(1, self.piwik.results_to_keep, 'filter_for_prior correctly sets the number of results to keep')
        
    def testFilterForPrior(self):
        result = {"2009-04-20 to 2009-04-26":
                   {"bounce_count":5049,"max_actions":70,"nb_actions":10486,"nb_uniq_visitors":5777,"nb_visits":6345,"nb_visits_converted":0,"sum_visit_length":543675},
                 "2009-04-27 to 2009-05-03":
                   {"bounce_count":4885,"max_actions":71,"nb_actions":9669,"nb_uniq_visitors":5562,"nb_visits":6014,"nb_visits_converted":0,"sum_visit_length":458155},
                 "2009-05-04 to 2009-05-10":
                   {"bounce_count":4388,"max_actions":47,"nb_actions":8362,"nb_uniq_visitors":5011,"nb_visits":5393,"nb_visits_converted":0,"sum_visit_length":397179},
                 "2009-05-11 to 2009-05-17":
                   {"bounce_count":10219,"max_actions":87,"nb_actions":23448,"nb_uniq_visitors":12522,"nb_visits":13238,"nb_visits_converted":0,"sum_visit_length":1135300},
                 "2009-05-18 to 2009-05-24":
                   {"bounce_count":5319,"max_actions":88,"nb_actions":13368,"nb_uniq_visitors":6487,"nb_visits":7107,"nb_visits_converted":0,"sum_visit_length":758480},
                 "2009-05-25 to 2009-05-31":
                   {"bounce_count":4776,"max_actions":79,"nb_actions":11719,"nb_uniq_visitors":5893,"nb_visits":6429,"nb_visits_converted":0,"sum_visit_length":648816},
                 "2009-06-01 to 2009-06-07":
                   {"bounce_count":5900,"max_actions":86,"nb_actions":13268,"nb_uniq_visitors":6933,"nb_visits":7628,"nb_visits_converted":0,"sum_visit_length":784984},
                 "2009-06-08 to 2009-06-14":
                   {"bounce_count":4850,"max_actions":88,"nb_actions":10897,"nb_uniq_visitors":5735,"nb_visits":6267,"nb_visits_converted":0,"sum_visit_length":547939}
                  }
        self.piwik.results_to_keep = 4
        result = self.piwik.filter_for_prior(result)
        expected_result = {"2009-04-20 to 2009-04-26":
                   {"bounce_count":5049,"max_actions":70,"nb_actions":10486,"nb_uniq_visitors":5777,"nb_visits":6345,"nb_visits_converted":0,"sum_visit_length":543675},
                 "2009-04-27 to 2009-05-03":
                   {"bounce_count":4885,"max_actions":71,"nb_actions":9669,"nb_uniq_visitors":5562,"nb_visits":6014,"nb_visits_converted":0,"sum_visit_length":458155},
                 "2009-05-04 to 2009-05-10":
                   {"bounce_count":4388,"max_actions":47,"nb_actions":8362,"nb_uniq_visitors":5011,"nb_visits":5393,"nb_visits_converted":0,"sum_visit_length":397179},
                 "2009-05-11 to 2009-05-17":
                   {"bounce_count":10219,"max_actions":87,"nb_actions":23448,"nb_uniq_visitors":12522,"nb_visits":13238,"nb_visits_converted":0,"sum_visit_length":1135300}}
        self.assertEqual(expected_result, result, 'filter_for_prior retains the first n results where n is results_to_keep')
        
    def testUniqueVisitors(self):
        self.fake_api_response('{"max_actions":57,"nb_uniq_visitors":1796,"nb_visits":2011,"nb_actions":3755,"sum_visit_length":201371,"bounce_count":1511,"nb_visits_converted":0}')
        visitors = self.piwik.unique_visitors(1)
        self.assertEqual(1796, visitors, "unique_visitors returns the expected number of visitors")

    def testVisits(self):
        self.fake_api_response('{"max_actions":57,"nb_uniq_visitors":1796,"nb_visits":2011,"nb_actions":3755,"sum_visit_length":201371,"bounce_count":1511,"nb_visits_converted":0}')
        visits = self.piwik.visits(1)
        self.assertEqual(2011, visits, "visits returns the expected number of visitors") 

    def testActions(self):
        self.fake_api_response('{"max_actions":57,"nb_uniq_visitors":1796,"nb_visits":2011,"nb_actions":3755,"sum_visit_length":201371,"bounce_count":1511,"nb_visits_converted":0}')
        actions = self.piwik.actions(1)
        self.assertEqual(3755, actions, "actions returns the expected number of actions") 

    def testTotalTime(self):
        self.fake_api_response('{"max_actions":57,"nb_uniq_visitors":1796,"nb_visits":2011,"nb_actions":3755,"sum_visit_length":201371,"bounce_count":1511,"nb_visits_converted":0}')
        time = self.piwik.total_time(1)
        self.assertEqual(201371, time, "total_time returns the expected time")    

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

    def testVisitsFromSearch(self):
        self.fake_api_response('[{"label":"Search Engines","sum_daily_nb_uniq_visitors":350,"nb_visits":353,"nb_actions":506,"max_actions":23,"sum_visit_length":21751,"bounce_count":294,"nb_visits_converted":0},{"label":"Websites","sum_daily_nb_uniq_visitors":176,"nb_visits":184,"nb_actions":393,"max_actions":33,"sum_visit_length":42592,"bounce_count":129,"nb_visits_converted":0},{"label":"Direct Entry","sum_daily_nb_uniq_visitors":99,"nb_visits":138,"nb_actions":293,"max_actions":36,"sum_visit_length":22162,"bounce_count":107,"nb_visits_converted":0}]')
        visits_from_search = self.piwik.visits_from_search(1)
        self.assertEqual(353, visits_from_search, 'visits_from_search returns correct information from example')

    def testVisitsFromSearchShouldReturnZeroIfNoSearchKey(self):
        self.fake_api_response('[{"label":"Websites","sum_daily_nb_uniq_visitors":176,"nb_visits":184,"nb_actions":393,"max_actions":33,"sum_visit_length":42592,"bounce_count":129,"nb_visits_converted":0},{"label":"Direct Entry","sum_daily_nb_uniq_visitors":99,"nb_visits":138,"nb_actions":293,"max_actions":36,"sum_visit_length":22162,"bounce_count":107,"nb_visits_converted":0}]')
        visits_from_search = self.piwik.visits_from_search(1)
        self.assertEqual(0, visits_from_search, 'visits_from_search returns zero when key "Search Engines" is not present')        
        
    def testVisitsFromSites(self):
        self.fake_api_response('[{"label":"Search Engines","sum_daily_nb_uniq_visitors":350,"nb_visits":353,"nb_actions":506,"max_actions":23,"sum_visit_length":21751,"bounce_count":294,"nb_visits_converted":0},{"label":"Websites","sum_daily_nb_uniq_visitors":176,"nb_visits":184,"nb_actions":393,"max_actions":33,"sum_visit_length":42592,"bounce_count":129,"nb_visits_converted":0},{"label":"Direct Entry","sum_daily_nb_uniq_visitors":99,"nb_visits":138,"nb_actions":293,"max_actions":36,"sum_visit_length":22162,"bounce_count":107,"nb_visits_converted":0}]')
        visits_from_sites = self.piwik.visits_from_sites(1)
        self.assertEqual(184, visits_from_sites, 'visits_from_sites returns correct information from example')

    def testVisitsFromDirectAccess(self):
        self.fake_api_response('[{"label":"Search Engines","sum_daily_nb_uniq_visitors":350,"nb_visits":353,"nb_actions":506,"max_actions":23,"sum_visit_length":21751,"bounce_count":294,"nb_visits_converted":0},{"label":"Websites","sum_daily_nb_uniq_visitors":176,"nb_visits":184,"nb_actions":393,"max_actions":33,"sum_visit_length":42592,"bounce_count":129,"nb_visits_converted":0},{"label":"Direct Entry","sum_daily_nb_uniq_visitors":99,"nb_visits":138,"nb_actions":293,"max_actions":36,"sum_visit_length":22162,"bounce_count":107,"nb_visits_converted":0}]')
        visits_from_direct_access = self.piwik.visits_from_direct_access(1)
        self.assertEqual(138, visits_from_direct_access, 'visits_from_sites returns correct information from example')
            
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
 
    def testPercentVisitsFromDirectAccess(self):
        self.piwik.visits_from_direct_access = lambda site_id, period, date: 33
        self.piwik.visits = lambda site_id, period, date: 99
        percent_from_direct_access = self.piwik.percent_visits_from_direct_access(1)
        self.assertEqual(33, percent_from_direct_access, "percent_visits_from_direct_access returns the expected figure") 
          
    def testVisitorsFromParliament(self):
        self.fake_api_response('[{"label":"IP","nb_uniq_visitors":3091,"nb_visits":3808,"nb_actions":11271,"max_actions":171,"sum_visit_length":640475,"bounce_count":2424,"nb_visits_converted":0,"url":"http:\/\/piwik.org\/faq\/general\/#faq_52"},{"label":"Btcentralplus","nb_uniq_visitors":1513,"nb_visits":1669,"nb_actions":5320,"max_actions":154,"sum_visit_length":261469,"bounce_count":970,"nb_visits_converted":0,"url":"http:\/\/www.btcentralplus.com\/"},{"label":"Ntl","nb_uniq_visitors":638,"nb_visits":715,"nb_actions":2218,"max_actions":89,"sum_visit_length":113479,"bounce_count":413,"nb_visits_converted":0,"url":"http:\/\/www.ntl.com\/"},{"label":"Parliament","nb_uniq_visitors":156,"nb_visits":604,"nb_actions":2890,"max_actions":136,"sum_visit_length":153454,"bounce_count":313,"nb_visits_converted":0,"url":"http:\/\/www.parliament.uk\/"},{"label":"Gov","nb_uniq_visitors":197,"nb_visits":372,"nb_actions":1752,"max_actions":97,"sum_visit_length":118760,"bounce_count":193,"nb_visits_converted":0,"url":"http:\/\/www.gov.uk\/"}]')
        parliament_visitors = self.piwik.visitors_from_parliament(1, period='day')
        self.assertEqual(156, parliament_visitors, 'visitors_from_parliament returns the expected figure for example data')
        
    def testVisitsFromParliament(self):
        self.fake_api_response('[{"label":"IP","nb_uniq_visitors":3091,"nb_visits":3808,"nb_actions":11271,"max_actions":171,"sum_visit_length":640475,"bounce_count":2424,"nb_visits_converted":0,"url":"http:\/\/piwik.org\/faq\/general\/#faq_52"},{"label":"Btcentralplus","nb_uniq_visitors":1513,"nb_visits":1669,"nb_actions":5320,"max_actions":154,"sum_visit_length":261469,"bounce_count":970,"nb_visits_converted":0,"url":"http:\/\/www.btcentralplus.com\/"},{"label":"Ntl","nb_uniq_visitors":638,"nb_visits":715,"nb_actions":2218,"max_actions":89,"sum_visit_length":113479,"bounce_count":413,"nb_visits_converted":0,"url":"http:\/\/www.ntl.com\/"},{"label":"Parliament","nb_uniq_visitors":156,"nb_visits":604,"nb_actions":2890,"max_actions":136,"sum_visit_length":153454,"bounce_count":313,"nb_visits_converted":0,"url":"http:\/\/www.parliament.uk\/"},{"label":"Gov","nb_uniq_visitors":197,"nb_visits":372,"nb_actions":1752,"max_actions":97,"sum_visit_length":118760,"bounce_count":193,"nb_visits_converted":0,"url":"http:\/\/www.gov.uk\/"}]')
        parliament_visits = self.piwik.visits_from_parliament(1, period='day')
        self.assertEqual(604, parliament_visits, 'visits_from_parliament returns the expected figure for example data')
        
    def testVisitsFromParliamentSummed(self):
        self.fake_api_response("""{"2009-06-16":[{"label":"Parliament","nb_uniq_visitors":153,"nb_visits":440,"nb_actions":2589,"max_actions":151,"sum_visit_length":144615,"bounce_count":173,"nb_visits_converted":0,"url":"http:\/\/www.parliament.uk\/"},
                                                 {"label":"As9105","nb_uniq_visitors":368,"nb_visits":401,"nb_actions":1230,"max_actions":45,"sum_visit_length":93719,"bounce_count":227,"nb_visits_converted":0,"url":"http:\/\/www.as9105.com\/"},
                                                 {"label":"Sky","nb_uniq_visitors":373,"nb_visits":388,"nb_actions":1117,"max_actions":97,"sum_visit_length":50671,"bounce_count":227,"nb_visits_converted":0,"url":"http:\/\/www.sky.com\/"},
                                                 {"label":"Gov","nb_uniq_visitors":187,"nb_visits":308,"nb_actions":1754,"max_actions":144,"sum_visit_length":96181,"bounce_count":143,"nb_visits_converted":0,"url":"http:\/\/www.gov.uk\/"},
                                                 {"label":"Ac","nb_uniq_visitors":262,"nb_visits":281,"nb_actions":761,"max_actions":42,"sum_visit_length":41073,"bounce_count":178,"nb_visits_converted":0,"url":"http:\/\/www.ac.uk\/"}],
                                   "2009-06-17":[{"label":"Parliament","nb_uniq_visitors":156,"nb_visits":604,"nb_actions":2890,"max_actions":136,"sum_visit_length":153454,"bounce_count":313,"nb_visits_converted":0,"url":"http:\/\/www.parliament.uk\/"},
                                                 {"label":"Blueyonder","nb_uniq_visitors":522,"nb_visits":599,"nb_actions":2405,"max_actions":146,"sum_visit_length":106125,"bounce_count":371,"nb_visits_converted":0,"url":"http:\/\/www.blueyonder.co.uk\/"},
                                                 {"label":"As9105","nb_uniq_visitors":458,"nb_visits":557,"nb_actions":1561,"max_actions":55,"sum_visit_length":98770,"bounce_count":336,"nb_visits_converted":0,"url":"http:\/\/www.as9105.com\/"},
                                                 {"label":"Sky","nb_uniq_visitors":442,"nb_visits":456,"nb_actions":1186,"max_actions":39,"sum_visit_length":54846,"bounce_count":266,"nb_visits_converted":0,"url":"http:\/\/www.sky.com\/"}]}""")
        parliament_visits = self.piwik.visits_from_parliament(1, period='day')
        self.assertEqual(1044, parliament_visits, 'visits_from_parliament returns the expected figure for summed example data')
        
    def testBounces(self):
        self.fake_api_response('{"max_actions":57,"nb_uniq_visitors":1796,"nb_visits":2011,"nb_actions":3755,"sum_visit_length":201371,"bounce_count":1511,"nb_visits_converted":0}')
        bounce_count = self.piwik.bounces(1)
        self.assertEqual(1511, bounce_count, 'bounces returns the expected figure')
        
    def testBouncesFromCached(self):
        self.piwik.visit_summaries['1_week_yesterday'] = {"max_actions":57,"nb_uniq_visitors":1796,"nb_visits":2011,"nb_actions":3755,"sum_visit_length":201371,"bounce_count":1511,"nb_visits_converted":0}
        bounce_count = self.piwik.bounces(1)
        self.assertEqual(1511, bounce_count, 'bounces returns the expected figure')

    def testBounceRateSummedOverPeriod(self):
        self.fake_api_response('{"2009-05-25 to 2009-05-31":{"bounce_count":41456,"max_actions":663,"nb_actions":292298,"nb_uniq_visitors":71711,"nb_visits":78704,"nb_visits_converted":0,"sum_visit_length":16055700},"2009-06-01 to 2009-06-07":{"bounce_count":49718,"max_actions":831,"nb_actions":310627,"nb_uniq_visitors":79917,"nb_visits":89569,"nb_visits_converted":0,"sum_visit_length":16606500},"2009-06-08 to 2009-06-14":{"bounce_count":43675,"max_actions":601,"nb_actions":253324,"nb_uniq_visitors":64994,"nb_visits":74769,"nb_visits_converted":0,"sum_visit_length":14042000}}')
        bounce_count = self.piwik.bounces(1)
        self.assertEqual(134849, bounce_count, 'bounces returns the expected figure when summing over a period')