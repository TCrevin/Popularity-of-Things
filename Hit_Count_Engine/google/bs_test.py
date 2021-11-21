from bs4 import BeautifulSoup
import requests, json
from requests.exceptions import Timeout, TooManyRedirects, ConnectionError, ReadTimeout
import regex as re
from requests.models import ReadTimeoutError

# Regex for finding URLs. Source: https://gist.github.com/winzig/8894715
# group1: optional URL scheme
# group2: rest of the URL
URL_PATTERN = r"(?i)\b(https?:\/{1,3})?((?:(?:[\w.\-]+\.(?:[a-z]{2,13})|(?<=http:\/\/|https:\/\/)[\w.\-]+)\/)(?:[^\s()<>{}\[\]]+|\([^\s()]*?\([^\s()]+\)[^\s()]*?\)|\([^\s]+?\))+(?:\([^\s()]*?\([^\s()]+\)[^\s()]*?\)|\([^\s]+?\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’])|(?:(?<!@)(?:\w+(?:[.\-]+\w+)*\.(?:[a-z]{2,13})|(?:(?:[0-9](?!\d)|[1-9][0-9](?!\d)|1[0-9]{2}(?!\d)|2[0-4][0-9](?!\d)|25[0-5](?!\d))[.]?){4})\b\/?(?!@)(?:[^\s()<>{}\[\]]+|\([^\s()]*?\([^\s()]+\)[^\s()]*?\)|\([^\s]+?\))*(?:\([^\s()]*?\([^\s()]+\)[^\s()]*?\)|\([^\s]+?\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’])?))"


def main(filename):
    # attrs = {"href": re.compile(r"")}  # filter through hrefs with matching attributes
    refs = dict()
    for link in links:
        print(f"Searching {link}")
        if link.endswith(".pdf"):
            print("\tInvalid address...")
            continue
        refs[link] = list()
        # Could use faster 3rd-party Python parser: lxml
        try:
            html_text = requests.get(link, timeout=5).text
        except (Timeout, TooManyRedirects, ConnectionError, ReadTimeout):
            print(f"\tNo response from {link}")
            continue
        print("\tParsing...")
        soup = BeautifulSoup(html_text, "html.parser")
        # for shref in soup.find_all("a", attrs=attrs, string=re.compile(link_pattern)):
        aa = soup.find_all("a", {"href": re.compile(URL_PATTERN)})
        for a in aa:
            # print(a["href"])
            refs[link].append(a["href"])
        # for shref in soup.find_all("a"):  # , {"href": re.compile(URL_PATTERN)}):
        # print(shref)
        # href = re.matchshref.get("href")
        # print(href)
        # if "https://" in href:
        # refs[link].append(href)
    with open(f"soup_results/{filename}.json", "w") as fp:
        fp.write(json.dumps(refs))


if __name__ == "__main__":
    global links
    files = ["nmap", "volatility", "wireshark"]
    for filename in files:
        print(f"Beautiful Souping {filename}")
        print("Loading home URLs...")
        with open(f"search_results/{filename}.json") as json_file:
            links = json.load(json_file)
        print("Home URLs loaded...")
        main(filename)
        print(f"{filename} Done.")
