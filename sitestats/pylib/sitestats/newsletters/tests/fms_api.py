from sitestats.newsletters.sources import fms_api
import unittest
from datetime import date
import sitestats.newsletters.tests

class FMSAPITests(unittest.TestCase):
    
    def setUp(self):
        self.fms_api = fms_api.FMSApi()
        self.fake_api_response = sitestats.newsletters.tests.fake_api_response
        
    def fakeProblems(self):
        return """[{"name":"",
                    "anonymous":"1",
                    "service":"Web interface",
                    "council":"Southwark Borough Council",
                    "detail":"Reporting a test problem. Please ignore",
                    "confirmed":"2009-07-01 09:15:47.561939",
                    "northing":"179765.049530099",
                    "category":"Trees",
                    "title":"Test problem",
                    "whensent":"2009-07-01 09:55:02.205413",
                    "easting":"532589.53517907"},
                    {"name":"",
                     "anonymous":"1",
                     "service":"iPhone",
                     "council":"Lambeth Borough Council and Southwark Borough Council",
                     "detail":"Reporting another test problem",
                     "confirmed":"2009-07-01 09:15:47.561939",
                     "northing":"179765.049530099",
                     "category":"Other",
                     "title":"Another test problem",
                     "whensent":"2009-07-01 09:55:02.205413",
                     "easting":"532589.53517907"}]"""
    
    
    def testNumReports(self):
        self.fake_api_response(fms_api, self.fakeProblems())
        num_reports = self.fms_api.num_reports(date(2009, 6, 3), date(2009, 6, 10))
        self.assertEqual(2, num_reports, 'num_reports returns the expected result with example data')

    def testNumFixes(self):
        self.fake_api_response(fms_api, self.fakeProblems())
        num_fixes = self.fms_api.num_fixes(date(2009, 6, 3), date(2009, 6, 10))
        self.assertEqual(2, num_fixes, 'num_fixes returns the expected result with example data')        

    def testServiceCounts(self):
        self.fake_api_response(fms_api, self.fakeProblems())
        service_counts = self.fms_api.service_counts(date(2009, 6, 3), date(2009, 6, 10))
        expected_counts = {'Web interface' : 1, 'iPhone' : 1}
        self.assertEqual(expected_counts, service_counts, 'service_counts returns the expected result with example data')
        
    def testCategoryCounts(self):
        self.fake_api_response(fms_api, self.fakeProblems())
        category_counts = self.fms_api.category_counts(date(2009, 6, 3), date(2009, 6, 10))
        expected_counts = {'Trees' : 1, 'Other' : 1}
        self.assertEqual(expected_counts, category_counts, 'category_counts returns the expected result with example data')
    
    def testTopCategories(self):
        self.fake_api_response(fms_api, self.fakeProblems())
        categories = self.fms_api.top_categories(date(2009, 6, 3), date(2009, 6, 10), limit=10)
        expected_categories = [('Trees', 1), ('Other', 1)]
        self.assertEqual(expected_categories, categories, 'top_categories returns the expected result with example data')
  
    def testCouncilCounts(self):
        self.fake_api_response(fms_api, self.fakeProblems())
        council_counts = self.fms_api.council_counts(date(2009, 6, 3), date(2009, 6, 10))
        expected_counts = {'Lambeth Borough Council' : 1, 'Southwark Borough Council' : 2}
        self.assertEqual(expected_counts, council_counts, 'council_counts returns the expected result with example data')

    def testCouncilCountsWithEmptyCouncils(self):
        problems = """[{"name":"",
                    "anonymous":"1",
                    "service":"Web interface",
                    "council":null,
                    "detail":"Reporting a test problem. Please ignore",
                    "confirmed":"2009-07-01 09:15:47.561939",
                    "northing":"179765.049530099",
                    "category":"Trees",
                    "title":"Test problem",
                    "whensent":"2009-07-01 09:55:02.205413",
                    "easting":"532589.53517907"}]"""
        self.fake_api_response(fms_api, problems)
        council_counts = self.fms_api.council_counts(date(2009, 6, 3), date(2009, 6, 10))
        expected_counts = {}
        self.assertEqual(expected_counts, council_counts, 'council_counts returns the expected result when problems are missing councils')
        
    def testTopCouncils(self):
        self.fake_api_response(fms_api, self.fakeProblems())
        categories = self.fms_api.top_councils(date(2009, 6, 3), date(2009, 6, 10), limit=10)
        expected_categories = [('Southwark Borough Council', 2), ('Lambeth Borough Council', 1)]
        self.assertEqual(expected_categories, categories, 'top_councils returns the expected result with example data')
       