import requests, json


class Fetch:
    """
    A class used to represent one search with items from one or more pages.
    """

    def __init__(self, query):
        """Initializes object attributes for search.
        :param query: search term for custom search
        """
        self.query = query
        self.key = "AIzaSyBDCfGzExKZN_hLv1XYCuB4K_iZWdvpfR0"
        self.cx = "a400502691c2c4c3c"
        self.items = {}

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


def main():
    print("Google Custom Search\n")
    print("Give a search term, or 'exit' to stop the program.")

    while True:
        query = input("Query > ")
        if query == "":
            continue
        elif query == "exit":
            break
        print("Give the number of pages between 1 and 10 you want to search")
        while True:
            try:
                pages = int(input("Pages > ") or "1")
            except ValueError:
                print("Not a number")
                continue
            if pages <= 10 and pages > 0:
                break
        custom = Fetch(query)
        try:
            # custom.getItems(pages)
            custom.getItems(1)  # To avoid too reaching daily limit
        except Exception as err:
            print("Error occured:")
            print(err)
            continue
        links = set()
        # print(custom.items)
        for page in custom.items:
            links.update([item["displayLink"] for item in custom.items[page]])
        print("\nUnique links:\n" + "------------------------")
        print(links)
        print("\n\nGive a search term or 'exit' to stop the program.")
    print("Bye.")


if __name__ == "__main__":
    # import os
    # KEY = os.environ.get('GOOGLE_API_KEY')
    # CX = os.environ.get('SEARCH_ENGINE_ID')
    import yaml

    config = yaml.safe_load(open("config.yaml", "r"))
    try:
        main()
    except KeyboardInterrupt as ctrlc:
        print("\nBye.")
