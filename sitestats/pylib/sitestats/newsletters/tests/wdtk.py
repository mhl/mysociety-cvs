import unittest
from sitestats.newsletters.models.wdtk import WDTKNewsletter
from tests import example_dir
from newsletter import MockPiwik
            
class WDTKNewsletterTests(unittest.TestCase):

    def setUp(self):
        self.sources = {'piwik'  : MockPiwik()}
        self.wdtk = WDTKNewsletter()
        self.wdtk.set_site_id = lambda sources: None
        
    def testRenderedToHTMLTemplateCorrectly(self):
        html = self.wdtk.render('html', self.sources).strip()
        expected_html = open(example_dir() + 'wdtk.html').read().strip()
        self.assertEqual(expected_html, html, 'render produces correct output in HTML for example data')
        
    def testRenderedToTextTemplateCorrectly(self):
        text = self.wdtk.render('text', self.sources).strip()
        expected_text = open(example_dir() + 'wdtk.txt').read().strip()
        self.assertEqual(expected_text, text, 'render produces correct output in text for example data')