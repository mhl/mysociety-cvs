import unittest
from sitestats.newsletters.models.fms import FMSNewsletter
from tests import example_dir
from newsletter import MockPiwik
from datetime import date

class MockFMSAPI:
    
    def num_reports(self, start_date, end_date):
        return 10
        
class FMSNewsletterTests(unittest.TestCase):

    def setUp(self):
        self.sources = {'piwik'  : MockPiwik(), 'fms_api' : MockFMSAPI()}
        self.fms = FMSNewsletter()
        self.fms.set_site_id = lambda sources: None
        
    def testRenderedToHTMLTemplateCorrectly(self):
        html = self.fms.render('html', self.sources, date=date(2009, 1, 1)).strip()
        expected_html = open(example_dir() + 'fms.html').read().strip()
        self.assertEqual(expected_html, html, 'render produces correct output in HTML for example data')
        
    def testRenderedToTextTemplateCorrectly(self):
        text = self.fms.render('text', self.sources, date=date(2009, 1, 1)).strip()
        expected_text = open(example_dir() + 'fms.txt').read().strip()
        self.assertEqual(expected_text, text, 'render produces correct output in text for example data')