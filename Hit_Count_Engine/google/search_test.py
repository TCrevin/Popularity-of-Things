import requests, json, time
import gtab
from bs4 import BeautifulSoup
from hiddenprints import HiddenPrints
import regex as re

# Regex for finding URLs. Source: https://gist.github.com/winzig/8894715
# group1: optional URL scheme
# group2: rest of the URL
URL_PATTERN = r"(?i)\b(https?:\/{1,3})?((?:(?:[\w.\-]+\.(?:[a-z]{2,13})|(?<=http:\/\/|https:\/\/)[\w.\-]+)\/)(?:[^\s()<>{}\[\]]+|\([^\s()]*?\([^\s()]+\)[^\s()]*?\)|\([^\s]+?\))+(?:\([^\s()]*?\([^\s()]+\)[^\s()]*?\)|\([^\s]+?\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’])|(?:(?<!@)(?:\w+(?:[.\-]+\w+)*\.(?:[a-z]{2,13})|(?:(?:[0-9](?!\d)|[1-9][0-9](?!\d)|1[0-9]{2}(?!\d)|2[0-4][0-9](?!\d)|25[0-5](?!\d))[.]?){4})\b\/?(?!@)(?:[^\s()<>{}\[\]]+|\([^\s()]*?\([^\s()]+\)[^\s()]*?\)|\([^\s]+?\))*(?:\([^\s()]*?\([^\s()]+\)[^\s()]*?\)|\([^\s]+?\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’])?))"


class Fetch(object):
    """
    A class used to represent one search with items from one or more pages.
    """

    def __init__(self, cat="31"):
        """Initializes object attributes for search.
        :param query: search term for custom search
        """
        self._query = None
        self.cat = cat  # Programming
        self.key = "AIzaSyBDCfGzExKZN_hLv1XYCuB4K_iZWdvpfR0"
        self.cx = "a400502691c2c4c3c"
        self.items = {}
        self.popularity = self.__build_results()
        self.trends = gtab.GTAB()
        self.trends.set_options(
            pytrends_config={
                "cat": self.cat,
                "geo": "",
                "timeframe": "now 7-d",
            }
        )

    def __build_results(self):
        # TODO: check if existing results in file
        return {"queries": {}}

    @property
    def query(self):
        return self._query

    @query.setter
    def query(self, query):
        self._query = query

    def getItems(self, pages=1):
        """Sends API requests from 1 to 10 times each returning a page (10 items
        per page) and appends results into items object attribute.

        :param pages: Number between 1 and 10 requested for search, defaults to 1
        :type pages: int
        """
        if pages < 1 or pages > 10:
            print("Incorrect pages count!")
            return

        for page in range(1, pages + 1):
            start = 10 * (page - 1) + 1  # Actual starting index / First item in page
            url = (
                f"https://www.googleapis.com/customsearch/v1?key={self.key}&cx={self.cx}&start={start}&q={self.query}"
            )
            response = json.loads(requests.request("GET", url).text)
            if "items" in response:
                self.items[str(page)] = response["items"]
                # print(page)
            else:
                print("oh no :(")

    def getTrends(self):
        """
        Get recent search trends using Google Trends Anchor Bank
        """
        # if self.trends is None:
        #     with HiddenPrints():
        #         self.__init_gtab()
        query = self.trends.new_query(self.query)
        results = {
            "count": str(query.max_ratio.mean()),
            "timestamp": str(time.time()),
        }
        self.popularity["queries"][self.query.lower()] = results
        print(self.popularity["queries"][self.query.lower()])

    def getPopularities(self):
        res = dict(sorted(self.popularity["queries"].items(), key=lambda x: float(x[1]["count"]), reverse=True))
        # sorted(self.popularity.items(), key=lambda x: x[1]['queries']["count"], reverse=True)
        print({"queries": res})
        # TODO: save into a file

    def getReferences(self, links):
        refs = dict()
        for link in links:
            refs[link] = list()
            # Could use faster 3rd-party Python parser: lxml
            html_text = requests.get(link).text
            soup = BeautifulSoup(html_text, "html.parser")
            # for shref in soup.find_all("a", attrs=attrs, string=re.compile(link_pattern)):
            aa = soup.find_all("a", {"href": re.compile(URL_PATTERN)})
            for a in aa:
                # print(a["href"])
                refs[link].append(a["href"])


def main():
    # engine = input("> ")
    # print("Google Custom Search\n")
    # Initialize the object
    with HiddenPrints():
        search = Fetch()

    print("Google Custom Search(1) or Trends(2)")
    while True:
        print("Choose an engine, or 'exit' to stop the program.")
        engine = input("Engine > ")
        if engine == "":
            continue
        elif engine == "exit":
            break
        else:
            try:
                engine = int(engine)
            except ValueError:
                print("Not a number")
                continue
            if engine not in [1, 2, 3]:
                continue

        if engine == 3:
            languages = ["Python", "Java", "C++", "golang", "javascript", "C#", "C", "Rust", "PHP", "FORTRAN"]
            for language in languages:
                search.query = language
                search.getTrends()
            break

        print("Give a search term, or 'exit' to stop the program.")
        search.query = input("Query > ")
        if search.query == "":
            continue
        elif search.query == "exit":
            break

        if engine == 2:
            search.getTrends()
            continue
        # if engine is "1":
        print("Give the number of pages between 1 and 10 you want to search")
        while True:
            try:
                pages = int(input("Pages > ") or "1")
            except ValueError:
                print("Not a number")
                continue
            if pages <= 10 and pages > 0:
                break
        try:
            # custom.getItems(pages)
            search.getItems(pages)  # To avoid too reaching daily limit
        except Exception as err:
            print("Error occured:")
            print(err)
            continue
        links = set()
        # print(custom.items)
        for page in search.items:
            links.update([item["link"] for item in search.items[page]])
        print("\nUnique links:\n" + "------------------------")
        print(links)
        print("\n\nGive a search term or 'exit' to stop the program.")
    search.getPopularities()
    print("Bye.")


if __name__ == "__main__":
    # import os
    # KEY = os.environ.get('GOOGLE_API_KEY')
    # CX = os.environ.get('SEARCH_ENGINE_ID')
    # import yaml

    # config = yaml.safe_load(open("config.yaml", "r"))
    try:
        main()
    except KeyboardInterrupt as ctrlc:
        print("\nBye.")
