import unittest
from sitestats.newsletters.models.wtt import WTTNewsletter
from tests import example_dir
from newsletter import MockPiwik
            
class WTTNewsletterTests(unittest.TestCase):

    def setUp(self):
        self.sources = {'piwik'  : MockPiwik()}
        self.wtt = WTTNewsletter()
        self.wtt.set_site_id = lambda sources: None
        
    def testRenderedToHTMLTemplateCorrectly(self):
        html = self.wtt.render('html', self.sources).strip()
        expected_html = open(example_dir() + 'wtt.html').read().strip()
        self.assertEqual(expected_html, html, 'render produces correct output in HTML for example data')
        
    def testRenderedToTextTemplateCorrectly(self):
        text = self.wtt.render('text', self.sources).strip()
        expected_text = open(example_dir() + 'wtt.txt').read().strip()
        self.assertEqual(expected_text, text, 'render produces correct output in text for example data')