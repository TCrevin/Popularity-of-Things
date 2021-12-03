from os import get_terminal_size
import gtab
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
Programming: 31
    C & C++: 731
    Developer Jobs: 802
    Development Tools: 730
    Java: 732
    Scripting Languages: 733
    Windows & .NET: 734
"""


class Fetch:
    def __init__(self, query, gtab):
        """
        :param query: defined search term for tweets tagged with #query
        """
        self.query = query
        self.gtab = gtab

    def getTrends(self):
        trend = self.gtab.new_query(self.query)
        return round(trend.max_ratio.mean())


def google_process(queries, category):
    res_dict = {}
    gt = gtab.GTAB()
    gt.set_options(
        pytrends_config={"cat": category, "geo": "", "timeframe": "now 7-d"},
        gtab_config={"anchor_candidates_file": "550_cities_and_countries.txt", "num_anchors": 100},
    )

    try:
        gt.set_active_gtab(f"google_anchorbank_geo=_timeframe=now 7-d_cat={category}.tsv")
    except FileNotFoundError:
        gt.create_anchorbank()
        gt.set_active_gtab(f"google_anchorbank_geo=_timeframe=now 7-d_cat={category}.tsv")

    for query in queries:
        gtrend = Fetch(query, gt)
        res_dict[query] = gtrend.getTrends()
    return res_dict


def main():
    tools = ["wireshark", "nmap"]
    cat = 341  # Computer Security
    print(google_process(tools, cat))


if __name__ == "__main__":
    main()
