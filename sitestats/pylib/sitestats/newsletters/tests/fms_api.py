from sitestats.newsletters.sources import fms_api
import unittest
from datetime import date
import sitestats.newsletters.tests

class FMSAPITests(unittest.TestCase):
    
    def setUp(self):
        self.fms_api = fms_api.FMSApi()
        self.fake_api_response = sitestats.newsletters.tests.fake_api_response
        
    def testNumReports(self):
        self.fake_api_response(fms_api, """[{"name":"","anonymous":"1","service":"","council":"Southwark Borough Council","detail":"Reporting a test problem. Please ignore","confirmed":"2009-07-01 09:15:47.561939","northing":"179765.049530099","category":"Trees","title":"Test problem","whensent":"2009-07-01 09:55:02.205413","easting":"532589.53517907"}]""")
        num_reports = self.fms_api.num_reports(date(2009, 6, 3), date(2009, 6, 10))
        self.assertEqual(1, num_reports, 'num_reports produces the expected result with example data')