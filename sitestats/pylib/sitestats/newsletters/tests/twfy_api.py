from sitestats.newsletters.sources import twfy_api
import unittest
from datetime import date
import sitestats.newsletters.tests

class TWFYAPITests(unittest.TestCase):  
    
    def setUp(self):
        self.twfy_api = twfy_api.TWFYApi()
        self.fake_api_response = sitestats.newsletters.tests.fake_api_response
    
    def fake_subscriptions(self):
        return """{"alerts":[ {"criteria":"speaker:14137","count":"4"},
                              {"criteria":"spoken by Delyth Morgan","count":"1"},
                              {"criteria":"sri lanka","count":"3"},
                              {"criteria":"Stuart speaker:10229","count":"2"},
                              {"criteria":"dementia","count":"1"}]}"""
                             
    def testRaisesErrorWhenErrorReturned(self):
        self.fake_api_response(twfy_api, "{'error': 'Unknown person ID'}")
        self.assertRaises(Exception, self.twfy_api.person_name, 1)
      
    def testEmailSubscribersCount(self):
        self.fake_api_response(twfy_api, self.fake_subscriptions())
        start_date = date(2009, 6, 15)
        end_date = date(2009, 6, 22)
        subscribers = self.twfy_api.email_subscribers_count(start_date, end_date)
        expected_subscribers = 11
        self.assertEqual(expected_subscribers, subscribers, 'email_subscribers_count returns expected results for example data')

    def testTopEmailSubscriptions(self):
        self.fake_api_response(twfy_api, self.fake_subscriptions())
        start_date = date(2009, 6, 15)
        end_date = date(2009, 6, 22)
        top_subscriptions = self.twfy_api.top_email_subscriptions(start_date, end_date, limit=3)
        expected_subscriptions = ["speaker:14137", "sri lanka", "Stuart speaker:10229"]
        self.assertEqual(expected_subscriptions, top_subscriptions, "top_email_subscriptions returns expected results for example data")
        
    def testPersonName(self):
        self.fake_api_response(twfy_api, """[{"member_id":"1430",
                                              "house":"1",
                                              "first_name":"Dennis",
                                              "last_name":"Skinner",
                                              "constituency":"Bolsover",
                                              "lastupdate":"2008-02-26 22:25:20",
                                              "full_name":"Dennis Skinner",
                                              "image":"/images/mps/10544.jpg"}]""")
        name = self.twfy_api.person_name(33)
        self.assertEqual('Dennis Skinner', name, "person_name returns the expected result for example data")
    