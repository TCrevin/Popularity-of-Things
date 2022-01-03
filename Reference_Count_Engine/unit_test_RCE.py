from reference_count_multiprocessing import search, linksFromFile, getTools
import os
import unittest
import logging
import sys

class TestRCE(unittest.TestCase):
    loremipsum = "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum"
    unit_test_dir = "home/toni/scripts/Popularity_of_Things/Reference_Count_Engine"
    links = getTools()
    #def __init__(self):
    #    super().__init__()
    #    self.loremipsum = "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum"
    #    self.unit_test_dir = "home/toni/scripts/Popularity_of_Things/Reference_Count_Engine"
    #    self.links = linksFromFile()

    def test_search(self):
        self.assertEqual(search(self.loremipsum, "dolor"), True, "Should be True")
        self.assertEqual(search(self.loremipsum, "dastardly"), None, "Should be None")
        self.assertEqual(search(self.loremipsum, "orem"), True, "Should be True")

    def test_search_links(self):
        self.assertEqual(self.links[2], "7zip", "Should be 7zip.org")
        self.assertEqual(self.links[15], "amap", "Should be amap")



    #def test_source(self):

    #   self.assertEqual()

if __name__ == '__main__':
    print("Starting...")
    #print(search("AAAA", "A"))
    #print(getTools())
    logging.basicConfig(stream=sys.stderr)
    logging.getLogger("TestRCE.test_search")
    logging.getLogger("TestRCE.test_search_links")
    unittest.main()

