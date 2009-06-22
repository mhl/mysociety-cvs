import unittest
from sitestats.newsletters.models.hfymp import HFYMPNewsletter
from tests import example_dir
from newsletter import MockPiwik
            
class HFYMPNewsletterTests(unittest.TestCase):

    def setUp(self):
        self.sources = {'piwik'  : MockPiwik()}
        self.hfymp = HFYMPNewsletter()
        self.hfymp.set_site_id = lambda sources: None
        
    def testRenderedToHTMLTemplateCorrectly(self):
        html = self.hfymp.render('html', self.sources).strip()
        expected_html = open(example_dir() + 'hfymp.html').read().strip()
        self.assertEqual(expected_html, html, 'render produces correct output in HTML for example data')
        
    def testRenderedToTextTemplateCorrectly(self):
        text = self.hfymp.render('text', self.sources).strip()
        expected_text = open(example_dir() + 'hfymp.txt').read().strip()
        print text
        print "***"
        print expected_text
        self.assertEqual(expected_text, text, 'render produces correct output in text for example data')