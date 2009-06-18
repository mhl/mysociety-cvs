import unittest
from sitestats.newsletters.models.pb import PBNewsletter
from tests import example_dir
from newsletter import MockPiwik
            
class PBNewsletterTests(unittest.TestCase):

    def setUp(self):
        self.sources = {'piwik'  : MockPiwik()}
        self.pb = PBNewsletter()
        self.pb.set_site_id = lambda sources: None
        
    def testRenderedToHTMLTemplateCorrectly(self):
        html = self.pb.render('html', self.sources).strip()
        expected_html = open(example_dir() + 'pb.html').read().strip()
        self.assertEqual(expected_html, html, 'render produces correct output in HTML for example data')
        
    def testRenderedToTextTemplateCorrectly(self):
        text = self.pb.render('text', self.sources).strip()
        expected_text = open(example_dir() + 'pb.txt').read().strip()
        self.assertEqual(expected_text, text, 'render produces correct output in text for example data')