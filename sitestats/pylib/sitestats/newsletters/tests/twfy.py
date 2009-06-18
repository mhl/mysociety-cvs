import unittest
from sitestats.newsletters.models.twfy import TWFYNewsletter
from tests import example_dir
from newsletter import MockPiwik
            
class TWFYNewsletterTests(unittest.TestCase):

    def setUp(self):
        self.sources = {'piwik'  : MockPiwik()}
        self.twfy = TWFYNewsletter()
        self.twfy.set_site_id = lambda sources: None
        
    def testRenderedToHTMLTemplateCorrectly(self):
        html = self.twfy.render('html', self.sources).strip()
        expected_html = open(example_dir() + 'twfy.html').read().strip()
        self.assertEqual(expected_html, html, 'render produces correct output in HTML for example data')
        
    def testRenderedToTextTemplateCorrectly(self):
        text = self.twfy.render('text', self.sources).strip()
        expected_text = open(example_dir() + 'twfy.txt').read().strip()
        self.assertEqual(expected_text, text, 'render produces correct output in text for example data')
        