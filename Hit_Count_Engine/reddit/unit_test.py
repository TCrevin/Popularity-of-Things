import unittest

import praw
from praw.models import MoreComments

import random


# reddit_api global functions
from reddit_api import translateQuery
from reddit_api import hasTag

from reddit_api import Fetch

# reddit_api globam variables
from reddit_api import reddit
from reddit_api import globalTags
from reddit_api import languages
from reddit_api import times
from reddit_api import sorts

# translateQuery
class testClassTranslateQuery(unittest.TestCase):

    def setUp(self):
        print("translateQuery function test beginning :")

    def tearDown(self):
        print("translateQuery function test finished !")

    def testTranslateQuery1(self):
        self.assertEqual(translateQuery("c++"), "cplusplus")
    def testTranslateQuery2(self):
        self.assertNotEqual(translateQuery("c++"), "c++")
        
    def testTranslateQuery3(self):
        self.assertEqual(translateQuery("c#"), "csharp")
    def testTranslateQuery4(self):
        self.assertNotEqual(translateQuery("c#"), "c#")
        
    def testTranslateQuery5(self):
        self.assertEqual(translateQuery("java"), "java")
       
# hasTag
class testClassHasTag(unittest.TestCase):

    def setUp(self):
        print("hasTag function test beginning :")

    def tearDown(self):
        print("hasTag function test finished !")

    def testHasTag1(self):
        title = "I wouldn’t want someone who knows Java either"
        subreddit = "ProgrammerHumor"
        subredditDescription = "Memes and jokes about everything programming and CS"
        selftext = None
        
        self.assertTrue(hasTag(title) or hasTag(selftext) or hasTag(subreddit) or hasTag(subredditDescription))
        
class testClassFetchParam(unittest.TestCase):
    
    def setUp(self):
        print("hasTag function test beginning :")

    def tearDown(self):
        print("hasTag function test finished !")

    def testFetchParam1(self): 
        query = languages[random.randint(0, len(languages)-1)]
        time = times[random.randint(0, len(times)-1)]
        sort = sorts[random.randint(0, len(sorts)-1)]
        
        fetch = Fetch(query, timestamp=time, sortP=sort)

if __name__ == '__main__':
    unittest.main()
    
print(__name__)