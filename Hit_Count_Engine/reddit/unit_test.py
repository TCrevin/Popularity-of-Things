import unittest

import praw
from praw.models import MoreComments

reddit = praw.Reddit(client_id="9aC2iDzQQi04w-q1cPmjUw",
                                  client_secret="O29M5Puueuew1y_rDYVuvUZLdKuF_w",
                                  user_agent="NLP_Project_API/0.0.1")

from reddit_api import translateQuery
from reddit_api import hasTag



class testClassTranslateQuery(unittest.TestCase):

    def setUp(self):
        print("translateQuery function test beginning :")

    def tearDown(self):
        print("translateQuery function test finished !")

    def test1(self):
        self.assertEqual(translateQuery("c++"), "cplusplus")
    def test2(self):
        self.assertNotEqual(translateQuery("c++"), "c++")
        
    def test3(self):
        self.assertEqual(translateQuery("c#"), "csharp")
    def test4(self):
        self.assertNotEqual(translateQuery("c#"), "c#")
        
    def test5(self):
        self.assertEqual(translateQuery("java"), "java")
    
        
        
"""class testClassHasTag(unittest.TestCase):

    def setUp(self):
        print("hasTag function test beginning :")

    def tearDown(self):
        print("hasTag function test finished !")

    def test_simple(self):
        submission = reddit.subreddit('all').search('java', time_filter='all')[0]
        
        submissions = reddit.subreddit('all').search('java', time_filter='all')
        for submission in submissions:
            self.assertTrue(hasTag(submission.title) or hasTag(submission.selftext) or hasTag(submission.subreddit.display_name) or hasTag(submission.subreddit.description))
"""

if __name__ == '__main__':
    unittest.main()