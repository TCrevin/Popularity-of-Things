from pytrends.request import TrendReq
from datetime import datetime, timedelta
import time
import json

# import matplotlib.pyplot as plt
"""
Google Trends does filter out some types of searches, such as:
- Searches made by very few people: Trends only shows data for popular terms, so search terms with low volume appear as "0"
- Duplicate searches: Trends eliminates repeated searches from the same person over a short period of time.
- Special characters: Trends filters out queries with apostrophes and other special characters.
"""


"""
    31      Programming: 
    314     Computer Security
    705     Security Products & Services
    730     Development Tools: 
    731     C & C++: 
    732     Java: 
    733     Scripting Languages: 
    734     Windows & .NET: 
    802     Developer Jobs: 
    1227    Computer Science: 
"""


now = datetime.today()
today = now.strftime("%Y-%m-%d")
old = now - timedelta(days=7)
week_ago = old.strftime("%Y-%m-%d")


class Fetch:
    def __init__(self, query, trend, category):
        """
        :param query: defined search term for tweets tagged with #query
        """
        self.query = query
        self.trend = trend
        self.category = category

    def getTrends(self):
        self.trend.build_payload(kw_list=[self.query], cat=self.category, timeframe="now 7-d")
        # build_payload(kw_list=["apple", "windows", "linux"], cat="303", timeframe="today 3-m")
        # pytrend_normal.outputbuild_payload(kw_list=["volatility"], cat="314", timeframe="today 12-m")

        int_over_time = self.trend.interest_over_time()
        try:
            return int_over_time.sum(numeric_only=True) / len(int_over_time)
        except AttributeError:
            return -1


def google_process(queries, category):
    res_dict = {}
    # gt = gtab.GTAB(dir_path="gtab_cmd")
    trend = TrendReq()
    #    pytrends_config = ({"cat": category, "geo": "", "timeframe": f"{week_ago} {today}"},)

    for query in queries:
        pytrends_obj = Fetch(query, trend, category)
        res_dict[query] = pytrends_obj.getTrends()
    return res_dict


def main():
    tools = ["wireshark", "nmap", "volatility"]
    cat = "314"  # Computer Security
    print(google_process(tools, cat))
    # cat = 1227  # Computer Science
    # print(google_process(tools, cat))
    # cat = None
    # print(google_process(tools, cat))


if __name__ == "__main__":
    main()
