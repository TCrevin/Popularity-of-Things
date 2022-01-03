import unittest
import shutil, tempfile
import os, yaml, json
from pytrends.request import TrendReq
from gpytrends import Fetch
from gsearch import readDB, saveResults, getName, getPageItems  # , customSearch

test_yaml = """
tools:
  - tool:
      nick: "0trace"
      name: "0trace"
      include: False
  - tool:
      nick: "wireshark"
      name: "Wireshark"
  - tool:
      nick: "3proxy"
      name: "3proxy"
"""


class TestFetch(unittest.TestCase):

    # This test will give ResourceWarning(s) regarding pytrends/request.py, ignore it.
    def test_getTrends(self):
        fetch = Fetch("trends", TrendReq(), 0)
        res = fetch.getTrends()
        self.assertTrue(
            res, "Expected fetch to return a numerical result between 0-100"
        )


class TestSearch(unittest.TestCase):
    # test_dir = None

    @classmethod
    def setUpClass(self):
        self.test_dir = tempfile.mkdtemp()
        with open(os.path.join(self.test_dir, "unittestDB.yml"), "w") as f:
            f.write(test_yaml)

    @classmethod
    def tearDownClass(self):
        shutil.rmtree(self.test_dir)

    def test_search(self):
        tools = readDB(os.path.join(self.test_dir, "unittestDB.yml"))
        self.assertEqual(tools, yaml.load(test_yaml, Loader=yaml.Loader), "Database is read correctly")
        name = getName(tools["tools"][0])
        self.assertIsNone(name, "The item's include: False")
        nick = tools["tools"][1]['tool']["nick"]
        name = getName(tools["tools"][1])
        self.assertEqual(name, "Wireshark", "Correct name returned")
        # Not testing query to the API due to key being disabled
        # res = getPageItems(name, 0)
        dummy_res = [
            "7810000",
            "https://www.wireshark.org/",
            "https://en.wikipedia.org/wiki/Wireshark",
            "https://www.wireshark.org/download.html",
            "https://wiki.wireshark.org/",
            "https://www.wireshark.org/docs/wsug_html_chunked/",
            "https://wiki.wireshark.org/SampleCaptures",
            "https://www.varonis.com/blog/how-to-use-wireshark/",
            "https://wiki.wireshark.org/CaptureSetup/USB",
            "https://sourceforge.net/projects/wireshark/",
            "https://wiki.wireshark.org/HTTP2",
        ]
        saveResults(nick, dummy_res, res_path=self.test_dir)
        with open(os.path.join(self.test_dir, nick + ".json"), "r") as f:
            file_res = json.load(f)
        self.assertEqual(file_res, dummy_res, "Results saved correctly")


if __name__ == "__main__":
    unittest.main()
