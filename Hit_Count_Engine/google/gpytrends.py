from pytrends.request import TrendReq

from pytrends.exceptions import ResponseError
from requests.exceptions import HTTPError

# from datetime import datetime, timedelta
from random import randint
from time import sleep

# import json

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
    734     Windowns & .NET: 
    802     Developer Jobs: 
    1227    Computer Science: 
"""


# now = datetime.today()
# today = now.strftime("%Y-%m-%d")
# old = now - timedelta(days=7)
# week_ago = old.strftime("%Y-%m-%d")


class Fetch:
    def __init__(self, query, trend, category):
        """
        :param query: defined search term for tweets tagged with #query
        """
        self.query = query
        self.trend = trend
        self.category = category

    def getTrends(self):
        # build_payload(kw_list=["apple", "windows", "linux"], cat="303", timeframe="today 3-m")
        # pytrend_normal.outputbuild_payload(kw_list=["volatility"], cat="314", timeframe="today 12-m")

        current_delay = 1
        max_delay = 32
        while True:
            try:
                self.trend.build_payload(kw_list=[self.query], cat=self.category, timeframe="now 7-d")
                int_over_time = self.trend.interest_over_time()
                res = round(int_over_time.mean(numeric_only=True)[0])
                print(res)
                return res
            except AttributeError:
                return -1
            except (HTTPError, ResponseError) as err:
                # print(f"HTTP error occurred:\n  {err}")
                if current_delay > max_delay:
                    print("\tToo many retry attempts. Returning...\n")
                    break
                print("\tWaiting about", current_delay, "seconds before retrying.")
                delay = current_delay + randint(0, 1000) / 1000.0
                # time.sleep(current_delay + round(random(), 3))
                sleep(delay)
                current_delay *= 2
                continue
            except IndexError:
                print(0)
                break
            except Exception as err:
                print(f"Other error occurred: {err}\n\n")
                raise
        return 0


def google_process(queries, category):
    res_dict = {}
    # gt = gtab.GTAB(dir_path="gtab_cmd")
    trend = TrendReq()
    #    pytrends_config = ({"cat": category, "geo": "", "timeframe": f"{week_ago} {today}"},)

    for query in queries:
        print(f"{query}", end=" ")
        pytrends_obj = Fetch(query, trend, category)
        res_dict[query] = pytrends_obj.getTrends()
        # print("OK...")
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
