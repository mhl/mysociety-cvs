import os
import unittest
from sitestats.newsletters.sources import google
from datetime import date
from tests import example_dir

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
        mock_search_url = SearchUrl(example_dir() + 'blog_results.xml')
        google.urllib.urlopen = lambda url: mock_search_url

    def fake_news_search_response(self):
        mock_search_url = SearchUrl(example_dir() + 'news_results.xml')
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
                            'num'     : 1000,
                            'as_drrb' : 'b',
                            'output'  : 'atom', 
                            'scoring' : 'r'}
        self.assertEqual(expected_params, date_params, 'date_params produces correct params for a week period')

    def testNewsQueryForSiteWithNoCustomQuery(self):
        default_query = self.google._query('TheyWorkForYou')
        self.assertEqual('theyworkforyou', default_query, '_news_query returns a default site query correctly')
    
    def testNewsQueryForSiteWithCustomQuery(self):
        custom_query = self.google._query('FixMyStreet')
        self.assertEqual('NeighbourhoodFixIt OR FixMyStreet', custom_query, '_news_query returns a custom site query correctly')

    def testBlogsReturnsCorrectCount(self):
        self.fake_blog_search_response()
        result_attributes = self.google.blogs('test', 'www.example.com', date = date(2009, 5, 31))
        self.assertEqual(33, result_attributes['resultcount'], 'blogs returns correct result count for example')

    def testBlogsReturnsEntries(self):
        self.fake_blog_search_response()
        result_attributes = self.google.blogs('test', 'www.example.com', date = date(2009, 5, 31))
        self.assertEqual(33, len(result_attributes['results']), 'blogs returns correct number of results for example')

    def testBlogsReturnsCorrectFirstResult(self):
        self.fake_blog_search_response()
        result_attributes = self.google.blogs('test', 'www.example.com', date = date(2009, 5, 31))
        expected_first_result = google.GoogleResult(title=u"'I will publish a blog post on Tuesday 24th March about a woman in <b>...</b>", 
                                                    content=u'<b>PledgeBank</b> United States I\'ll do it, but only if you\'ll help. Search for pledges: Pledge \u201cAdaLovelaceDay\u201d. "I will publish a blog post on Tuesday <b>.....</b> Town: Translate <b>PledgeBank</b> into your language. Built by mySociety. Powered by Easynet.',
                                                    link=u'http://www.pledgebank.com/AdaLovelaceDay')
        first_result = result_attributes['results'][0]    
        self.assertEqual(expected_first_result.title, first_result.title, 'blogs returns correct first result for example')

    def testBlogsReturnsCorrectQuerystring(self):
        self.fake_blog_search_response()
        result_attributes = self.google.blogs('test', 'www.example.com', date = date(2009, 5, 31))
        expected_querystring = 'http://blogsearch.google.com/blogsearch_feeds?scoring=r&as_miny=2009&as_maxy=2009&as_maxd=31&num=1000&as_minm=5&as_q=test+-site%3Awww.example.com&output=atom&as_maxm=5&as_mind=25&as_drrb=b'
        self.assertEqual(expected_querystring, result_attributes['url'], 'blogs returns correct query string for example')

    def testNewsReturnsCorrectCount(self):
        self.fake_news_search_response()
        result_attributes = self.google.news('test', 'www.example.com', date = date(2009, 5, 31))
        self.assertEqual(6, result_attributes['resultcount'], 'news returns correct result count for example')

    def testNewsReturnsCorrectQuerystring(self):
        self.fake_news_search_response()
        result_attributes = self.google.news('test', 'www.example.com', date = date(2009, 5, 31))
        expected_querystring = 'http://news.google.com/news?scoring=r&as_miny=2009&as_maxy=2009&q=test+-site%3Awww.example.com&as_maxd=31&num=1000&as_minm=5&output=atom&as_maxm=5&as_mind=25&as_drrb=b'
        self.assertEqual(expected_querystring, result_attributes['url'], 'news returns correct querystring for example')
