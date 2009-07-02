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
    
    def fake_comments(self):
        return """{"comments":[{"comment_id":"23935",
                                "user_id":"17136",
                                "epobject_id":"19970603",
                                "body":"comment one",
                                "posted":"2009-06-28 20:54:38",
                                "major":"1",
                                "gid":"uk.org.publicwhip/debate/2009-06-23a.655.6",
                                "url":"/debate/?id=2009-06-23a.655.6#c23935"},
                                {"comment_id":"23934",
                                "user_id":"6529",
                                "epobject_id":"14580056",
                                "body":"comment two",
                                "posted":"2009-06-28 11:40:49",
                                "major":"1",
                                "gid":"uk.org.publicwhip/debate/2009-01-12a.35.2",
                                "url":"/debate/?id=2009-01-12a.35.2#c23934"},
                                {"comment_id":"23933",
                                "user_id":"14541",
                                "epobject_id":"14580056",
                                "body":"comment three",
                                "posted":"2009-06-28 00:34:11",
                                "major":"1",
                                "gid":"uk.org.publicwhip/debate/2009-01-12a.35.2",
                                "url":"/debate/?id=2009-01-12a.35.2#c23933"}]}"""
                                 
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
        expected_subscriptions = [('speaker:14137', 4), ('sri lanka', 3), ('Stuart speaker:10229', 2)]
        self.assertEqual(expected_subscriptions, top_subscriptions, "top_email_subscriptions returns expected results for example data")
        
    def testTopCommentPages(self):
        self.fake_api_response(twfy_api, self.fake_comments())
        start_date = date(2009, 6, 15)
        end_date = date(2009, 6, 22)
        top_comment_pages = self.twfy_api.top_comment_pages(start_date, end_date, limit=3)
        expected_pages = ["/debate/?id=2009-01-12a.35.2", "/debate/?id=2009-06-23a.655.6"]
        self.assertEqual(expected_pages, top_comment_pages, "top_comment_pages returns expected results for example data")
        
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
    
    def testPageTitle(self):
        self.fake_api_response(twfy_api, """[{"gid" : "2009-06-24b.800.0",
                                              "body" : "Opposition Day &#8212; [14th allotted day]"
                                             },
                                             {
                                              "gid" : "2009-06-24b.800.1",      
                                              "body" : "Iraq Inquiry"}]""")
        title = self.twfy_api.page_title(gid="2009-06-24b.800.1", page_type='debates', sub_type='commons')
        self.assertEqual('Iraq Inquiry', title, 'page_title returns expected results for example data')
        
    def testPageTitleWrans(self):
        self.fake_api_response(twfy_api, """[{"epobject_id":"19985215",
                                              "gid" : "2009-06-24b.800.1", 
                                              "body":"Business, Innovation and Skills"},
                                             {"epobject_id":"19985231",
                                              "gid":"2009-06-24b.279662.h",
                                              "body":"Building Colleges for the Future Programme"}]""")
        title = self.twfy_api.page_title(gid="2009-06-24a.279662.h", page_type='wrans', sub_type='')
        self.assertEqual('Building Colleges for the Future Programme', title, 'page_title returns expected results for example data')
      
    def testNextVersionGid(self):
        next_gid = self.twfy_api.next_version_gid("2009-06-24a.279662.h")
        self.assertEqual("2009-06-24b.279662.h", next_gid, "next_version_gid increments gid to next version")
        next_gid = self.twfy_api.next_version_gid("2009-06-24.279662.h")
        self.assertEqual("2009-06-24.279662.h", next_gid, "next_version_gid increments gid to next version")
    