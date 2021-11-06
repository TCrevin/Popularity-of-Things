import unittest

import praw
from praw.models import MoreComments

# reddit_api global functions
from reddit_api import translateQuery
from reddit_api import hasTag

# reddit_api globam variables
from reddit_api import reddit
from reddit_api import globalTags


# translateQuery
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
       
# hasTag
class testClassHasTag(unittest.TestCase):

    def setUp(self):
        print("hasTag function test beginning :")

    def tearDown(self):
        print("hasTag function test finished !")

    def test_simple(self):
        title = "I wouldn’t want someone who knows Java either"
        subreddit = "ProgrammerHumor"
        subredditDescription = "Memes and jokes about everything programming and CS"
        selftext = None
        
        self.assertTrue(hasTag(title) or hasTag(selftext) or hasTag(subreddit) or hasTag(subredditDescription))

if __name__ == '__main__':
    unittest.main()