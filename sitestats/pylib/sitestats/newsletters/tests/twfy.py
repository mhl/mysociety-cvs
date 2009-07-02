import unittest
from sitestats.newsletters.models.twfy import TWFYNewsletter
from tests import example_dir
from newsletter import MockPiwik, MockGoogle
from datetime import date


class MockTWFYAPI:
    
    def email_subscribers_count(self, start_date, end_date):
        return 10
        
    def top_email_subscriptions(self, start_date, end_date, limit=10):
        return [("a", 20), ("b", 10), ("c", 4)]
    
    def top_comment_pages(self, start_date, end_date, limit=10):
        return ['page one', 'page two']
    
    def person_name(self, id):
        return "Bob Person"
        
    def page_title(self, gid, page_type, sub_type):
        return "Title"
        
class TWFYNewsletterTests(unittest.TestCase):

    def setUp(self):
        self.sources = {'piwik'    : MockPiwik(), 
                        'twfy_api' : MockTWFYAPI(), 
                        'google'   : MockGoogle()}
        self.twfy = TWFYNewsletter()
        self.twfy.set_site_id = lambda sources: None
        self.twfy.base_url = 'http://www.theyworkforyou.com'
        
    def testRenderedToHTMLTemplateCorrectly(self):
        html = self.twfy.render('html', self.sources, date=date(2009, 1, 1)).strip()
        expected_html = open(example_dir() + 'twfy.html').read().strip()
        self.assertEqual(expected_html, html, 'render produces correct output in HTML for example data')
        
    def testRenderedToTextTemplateCorrectly(self):
        text = self.twfy.render('text', self.sources, date=date(2009, 1, 1)).strip()
        expected_text = open(example_dir() + 'twfy.txt').read().strip()
        self.assertEqual(expected_text, text, 'render produces correct output in text for example data')
        
    def testExtractGidTypeFromWrans(self):
        page_type = self.twfy.extract_gid_type_from_path("/wrans/?id=2009-06-24b.281735.h")
        self.assertEqual('wrans', page_type, 'extract_gid_type_from_path returns correct type for a written answer')
        
    def testExtractIdTypeFromDebate(self):
        page_type = self.twfy.extract_gid_type_from_path("/debate/?id=2009-06-25b.956.3")
        self.assertEqual('debate', page_type, 'extract_gid_type_from_path returns correct type for a debate')
     
    def testFormatInternalSearchKeywords(self):
        keywords = [('/?s=expenses&pop=1', 34), 
                    ('/?s=speaker%3A10544&pop=1', 27),
                    ('/?s=iran', 22)]
        expected_keywords = [({ 'current_value' : 'expenses', 
                               'link' : 'http://www.theyworkforyou.com/search/?s=expenses&pop=1' }, 34),
                             ({ 'current_value' : 'speaker:Bob Person', 
                               'link' : 'http://www.theyworkforyou.com/search/?s=speaker%3A10544&pop=1'}, 27),
                             ({ 'current_value' : 'iran', 
                               'link' : 'http://www.theyworkforyou.com/search/?s=iran&pop=1'}, 22) ]
        formatted_keywords = self.twfy.format_internal_search_keywords(keywords, self.sources)
        self.assertEqual(expected_keywords, formatted_keywords, 'format_internal_search_keywords produces correct output for example data')    