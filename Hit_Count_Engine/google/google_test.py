import requests, json


class Search:
    def __init__(self, query):
        self.query = query
        self.key = config['google_api']['key']
        self.cx = config['google_api']['cx']
        self.items = {}

    def getItems(self, pages=1):
        if pages < 1 or pages > 10:
            print("Incorrect pages count!")
            return
        for page in range(pages):
            start = 10 * (page-1) + 1 # Actual starting index / First item in page
            url = f"https://www.googleapis.com/customsearch/v1?key={self.key}&cx={self.cx}&start={start}&q={self.query}"
            response = json.loads(requests.request("GET", url).text)
            if 'items' in response:
                # FIXME: works when executed in ipython, here KeyError: 'items'
                self.items[str(page)] = response['items']
            else:
                print('oh no :(')


def main():
    query = input("Search query >")
    custom = Search(query)
    custom.getItems(1)
    pages = [page for page in custom.items]
    # TODO: testing
    for page in pages:
        links = [item['displayLink'] for item in page]
    print(links)



if __name__=="__main__":
    # import os
    # KEY = os.environ.get('GOOGLE_API_KEY')
    # CX = os.environ.get('SEARCH_ENGINE_ID')
    import yaml
    config = yaml.safe_load(open('config.yaml','r'))            
    main()