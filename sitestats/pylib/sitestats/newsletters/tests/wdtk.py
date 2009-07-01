import unittest
from sitestats.newsletters.models.wdtk import WDTKNewsletter
from tests import example_dir
from newsletter import MockPiwik, MockGoogle, newsletter_date
            
class WDTKNewsletterTests(unittest.TestCase):

    def setUp(self):
        self.sources = {'piwik'  : MockPiwik(), 'google' : MockGoogle()}
        self.wdtk = WDTKNewsletter()
        self.wdtk.set_site_id = lambda sources: None
        self.wdtk.base_url = 'http://www.whatdotheyknow.com'
        
    def testRenderedToHTMLTemplateCorrectly(self):
        html = self.wdtk.render('html', self.sources, date=newsletter_date()).strip()
        expected_html = open(example_dir() + 'wdtk.html').read().strip()
        self.assertEqual(expected_html, html, 'render produces correct output in HTML for example data')
        
    def testRenderedToTextTemplateCorrectly(self):
        text = self.wdtk.render('text', self.sources, date=newsletter_date()).strip()
        expected_text = open(example_dir() + 'wdtk.txt').read().strip()
        self.assertEqual(expected_text, text, 'render produces correct output in text for example data')