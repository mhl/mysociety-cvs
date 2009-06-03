import sys
import os
import unittest
sys.path.append("../../../pylib")
from datetime import date, timedelta

from sitestats.newsletters import formatting
from sitestats.newsletters.models import CommonBaseMeasuresNewsletter
from sitestats.newsletters import common
from sitestats.newsletters.sources import piwik
from sitestats.newsletters.sources import google

def example_dir():
    return os.path.dirname(__file__) + "/examples/"

class FormattingTests(unittest.TestCase):
    
    def testFormatHTMLCellValueWithLink(self):
        info = {'link'           : 'http://test.host', 
                'current_value'  : '34',
                'percent_change' : '+12%', 
                'unit'           : 's'}
        formatted = formatting.format_cell_value('html', info)
        expected_formatted  = "<a href='http://test.host'>34s</a> (+12%)"
        self.assertEqual(expected_formatted, formatted, 'format_cell_value formats html example with units and link correctly')
      
     
    def testFormatHTMLCellValueWithoutLink(self):
        info = {'current_value'  : '34', 
                'percent_change' : '-3%', 
                'unit'           : '%'}
        formatted = formatting.format_cell_value('html', info)
        expected_formatted = "34% (-3%)"
        self.assertEqual(expected_formatted, formatted, 'format_cell_value formats html example without link correctly')  

    def testFormatTextCellValue(self):
        info = {'link'           : 'http://test.host', 
                'current_value'  : '34',
                'percent_change' : '+12%', 
                'unit'           : 's'}
        formatted = formatting.format_cell_value('text', info)
        expected_formatted  = "34s (+12%)"    
        self.assertEqual(expected_formatted, formatted, 'format_cell_value formats text example without link correctly')  

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

class CommonBaseMeasuresNewsletterTests(unittest.TestCase):

    def setUp(self):
        self.sources = {'piwik'  : MockPiwik(),
                        'google' : MockGoogle()}
        self.base_measures = CommonBaseMeasuresNewsletter()
    
    def testDataRetrieved(self):
        
        base_measures = self.base_measures.get_data(self.sources['piwik'].sites()[1], self.sources, {})
        expected_base_measures = [{'current_value': 22, 'percent_change': '-60%', 'unit': ''}, 
                                  {'current_value': 33, 'percent_change': '-25%', 'unit': ''}, 
                                  {'current_value': 77, 'percent_change': '-13%', 'unit': '%'}, 
                                  {'current_value': 34, 'percent_change': '-24%', 'unit': '%'}, 
                                  {'current_value': 56, 'percent_change': '-16%', 'unit': '%'}, 
                                  {'current_value': 11, 'percent_change': '-83%', 'unit': ''}, 
                                  {'current_value': 12, 'percent_change': '-48%', 'unit': 's'}, 
                                  {'current_value': 98, 'link': 'http://test.host', 'percent_change': '+13%', 'unit': ''}, 
                                  {'current_value': 78, 'link': 'http://test.host', 'percent_change': '-12%', 'unit': ''}] 
        self.assertEqual(expected_base_measures, base_measures, 'get_data produces correct results for example')

    def testRenderedToHTMLTemplateCorrectly(self):
        html = self.base_measures.render('html', self.sources).strip()
        expected_html = open(example_dir() + 'base_measures.html').read().strip()
        self.assertEqual(expected_html, html, 'render produces correct output in HTML for example data')

    def testRenderedToTextTemplateCorrectly(self):
        text = self.base_measures.render('text', self.sources).strip()
        expected_text = open(example_dir() + 'base_measures.txt').read().strip()
        self.assertEqual(expected_text, text, 'render produces correct output in text for example data')

class SearchUrl:
    '''An object whose read method returns an example html page'''

    def __init__(self, file):
        self.file = file

    def read(self):
        return open(self.file).read()
#---

class GoogleTests(unittest.TestCase):

    def setUp(self):
        self.google = google.Google()

    def fake_blog_search_response(self):
        mock_search_url = SearchUrl(example_dir() + 'blog_results.html')
        google.urllib.urlopen = lambda url: mock_search_url

    def fake_news_search_response(self):
        mock_search_url = SearchUrl(example_dir() + 'news_results.html')
        google.urllib.urlopen = lambda url: mock_search_url

    def testDateParamsNotImplementedForMonth(self):
        end_date = date(2009, 6, 1)
        self.assertRaises(NotImplementedError, self.google._date_params, 'month', end_date)

    def testDateParamsCorrectForWeek(self):
        current_date = date(2009, 5, 31)
        date_params = self.google._date_params('week', current_date)
        expected_params = { 'as_mind' : 25,
                            'as_minm' : 5,
                            'as_miny' : 2009,
                            'as_maxd' : 31,
                            'as_maxm' : 5,
                            'as_maxy' : 2009, 
                            'as_drrb'  : 'b' }
        self.assertEqual(expected_params, date_params, 'date_params produces correct params for a week period')

    def testNewsQueryForSiteWithNoCustomQuery(self):
        default_query = self.google._query('TheyWorkForYou')
        self.assertEqual('theyworkforyou', default_query, '_news_query returns a default site query correctly')

    def testNewsQueryForSiteWithCustomQuery(self):
        custom_query = self.google._query('FixMyStreet')
        self.assertEqual('NeighbourhoodFixIt OR FixMyStreet', custom_query, '_news_query returns a custom site query correctly')

    def testBlogResultsParsing(self):
        result_attributes = self.google._parse_results(SearchUrl(example_dir() + 'blog_results.html').read()) 
        expected_attributes = {'results': 24}
        self.assertEqual(expected_attributes, result_attributes, '_parse_results can extract the number of results from a blog search example')

    def testNewsResultsParsingReturnsZeroForNoResults(self):
        result_attributes = self.google._parse_results(SearchUrl(example_dir() + 'news_no_results.html').read()) 
        expected_attributes = {'results': 0}
        self.assertEqual(expected_attributes, result_attributes, '_parse_results gets zero results from an example response with no results')

    def testBlogsReturnsAttributes(self):
        self.fake_blog_search_response()
        result_attributes = self.google.blogs('test', date = date(2009, 5, 31))
        expected_attributes = {'results': 24, 
                               'url'    : 'http://blogsearch.google.com/blogsearch?as_miny=2009&as_maxy=2009&as_maxd=31&as_minm=5&as_q=test&as_maxm=5&as_mind=25&as_drrb=b'}
        self.assertEqual(expected_attributes, result_attributes, 'blogs returns correct querystring and result count for example')

    def testNewsResultsParsing(self):
        result_attributes = self.google._parse_results(SearchUrl(example_dir() + 'news_results.html').read())
        expected_attributes = {'results' : 26}
        self.assertEqual(expected_attributes, result_attributes, '_parse_results can extract the number of results from a news search example')

    def testNewsReturnsAttributes(self):
        self.fake_news_search_response()
        result_attributes = self.google.news('test', date = date(2009, 5, 31))
        expected_attributes = {'results' : 26, 
                               'url' : 'http://news.google.com/news?as_miny=2009&as_maxy=2009&q=test&as_maxd=31&as_minm=5&as_maxm=5&as_mind=25&as_drrb=b'}
        self.assertEqual(expected_attributes, result_attributes, 'news returns correct querystring and results for example')


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
        self.fake_api_response('[{"label":"Search Engines","nb_uniq_visitors":350,"nb_visits":353,"nb_actions":506,"max_actions":23,"sum_visit_length":21751,"bounce_count":294,"nb_visits_converted":0},{"label":"Websites","nb_uniq_visitors":176,"nb_visits":184,"nb_actions":393,"max_actions":33,"sum_visit_length":42592,"bounce_count":129,"nb_visits_converted":0},{"label":"Direct Entry","nb_uniq_visitors":99,"nb_visits":138,"nb_actions":293,"max_actions":36,"sum_visit_length":22162,"bounce_count":107,"nb_visits_converted":0}]')
        visits_from_search = self.piwik.visits_from_search(1)
        self.assertEqual(353, visits_from_search, 'visits_from_search returns correct information from example')

    def testVisitsFromSites(self):
        self.fake_api_response('[{"label":"Search Engines","nb_uniq_visitors":350,"nb_visits":353,"nb_actions":506,"max_actions":23,"sum_visit_length":21751,"bounce_count":294,"nb_visits_converted":0},{"label":"Websites","nb_uniq_visitors":176,"nb_visits":184,"nb_actions":393,"max_actions":33,"sum_visit_length":42592,"bounce_count":129,"nb_visits_converted":0},{"label":"Direct Entry","nb_uniq_visitors":99,"nb_visits":138,"nb_actions":293,"max_actions":36,"sum_visit_length":22162,"bounce_count":107,"nb_visits_converted":0}]')
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

def main():
    unittest.main()

if __name__ == '__main__':
    main()