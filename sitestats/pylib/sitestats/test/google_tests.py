import sys
import unittest
from datetime import date, timedelta
sys.path.append("../../../pylib")
from sitestats import google

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
        mock_search_url = SearchUrl('example_blog_results.html')
        google.urllib.urlopen = lambda url: mock_search_url
        
    def fake_news_search_response(self):
        mock_search_url = SearchUrl('example_news_results.html')
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
        
    def testBlogResultsParsing(self):
        result_attributes = self.google._parse_results(SearchUrl('example_blog_results.html').read()) 
        expected_attributes = {'results': '24'}
        self.assertEqual(expected_attributes, result_attributes, '_parse_results can extract the number of results from a blog search example')
    
    def testBlogsReturnsAttributes(self):
        self.fake_blog_search_response()
        result_attributes = self.google.blogs('test')
        expected_attributes = {'results': '24', 
                               'url'    : 'http://blogsearch.google.com/blogsearch?as_miny=2009&as_maxy=2009&as_maxd=31&as_minm=5&as_q=test&as_maxm=5&as_mind=25&as_drrb=b'}
        self.assertEqual(expected_attributes, result_attributes, 'blogs returns correct querystring and result count for example')
        
    def testNewsResultsParsing(self):
        result_attributes = self.google._parse_results(SearchUrl('example_news_results.html').read())
        expected_attributes = {'results' : '26'}
        self.assertEqual(expected_attributes, result_attributes, '_parse_results can extract the number of results from a news search example')
    
    def testNewsReturnsAttributes(self):
        self.fake_news_search_response()
        result_attributes = self.google.news('test')
        expected_attributes = {'results' : '26', 
                               'url' : 'http://news.google.com/news?as_miny=2009&as_maxy=2009&q=test&as_maxd=31&as_minm=5&as_maxm=5&as_mind=25&as_drrb=b'}
        self.assertEqual(expected_attributes, result_attributes, 'news returns correct querystring and results for example')
        
def main():
    unittest.main()

if __name__ == '__main__':
    main()