import unittest
from sitestats.newsletters.models.hfymp import HFYMPNewsletter
from tests import example_dir
from newsletter import MockPiwik, MockGoogle, newsletter_date
            
class HFYMPNewsletterTests(unittest.TestCase):

    def setUp(self):
        self.sources = {'piwik'  : MockPiwik(), 'google' : MockGoogle()}
        self.hfymp = HFYMPNewsletter()
        self.hfymp.set_site_id = lambda sources: None
        self.hfymp.base_url = 'http://www.hearfromyourmp.com'
        
    def testRenderedToHTMLTemplateCorrectly(self):
        html = self.hfymp.render('html', self.sources, date=newsletter_date()).strip()
        expected_html = open(example_dir() + 'hfymp.html').read().strip()
        self.assertEqual(expected_html, html, 'render produces correct output in HTML for example data')
        
    def testRenderedToTextTemplateCorrectly(self):
        text = self.hfymp.render('text', self.sources, date=newsletter_date()).strip()
        expected_text = open(example_dir() + 'hfymp.txt').read().strip()
        self.assertEqual(expected_text, text, 'render produces correct output in text for example data')