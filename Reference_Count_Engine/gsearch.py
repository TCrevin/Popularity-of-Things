"""Google Custom Search JSON API requester.

This script allows the user to get google search results using REST to invoke the API.
API gives maximum of 100 items per search term but 10 items per query (page). 
API gives 100 free queries per day and after those every 1000 query costs $5, 
maximum of 10k queries per day.

This tool reads through the user provided yaml DB. The structure of DB and mandatory fields are:

> tools:
>  - tool:
>      nick: "nick"
>      name: "name"
>      include: False    # if does not exist, include tool.
>  - tool:
> ...

This script requires 'requests' package to be installed within the Python environment.
The API key and Search engine ID are to be acquired separately and keep them private.
"""

import os
import requests, json
from requests.models import HTTPError
import yaml
from random import randint
from time import sleep, time
from datetime import datetime

# Google API key and Search engine ID
key = "AIzaSyBDCfGzExKZN_hLv1XYCuB4K_iZWdvpfR0"
cx = "a400502691c2c4c3c"
# Yaml DB path
db_loc = "tools.yaml"
results_path = "Popularity-of-Things/Reference_Count_Engine/google_search_results/"
global response
exclude = (".exe", ".tar.xz", ".zip", ".pdf", ".epub", ".dmg")

now = datetime.now()
date = now.strftime("%d-%m-%Y")

# Test Yaml DB, to be removed
# test_yaml = """
# tools:
#   - tool:
#       nick: "0trace"
#       name: "0trace"
#       include: False
#   - tool:
#       nick: "wireshark"
#       name: "Wireshark"
#   - tool:
#       nick: "3proxy"
#       name: "3proxy"
# """
def getWorkDir(): # TODO: Docker
    return "/home/toni/scripts/Popularity_of_Things/"
    #return "/var/lib/output/"

def readDB(path):
    """Reads the DB and returns it as dict

    :param path: the location of Yaml DB provided by the user
    :return: yaml DB as python dictionary
    """
    with open(path, "r") as stream:
        yamldb = yaml.load(stream, Loader=yaml.Loader)
    # yamldb = yaml.load(test_yaml, Loader=yaml.Loader)
    return yamldb


def saveResults(nick, result):
    # TODO: save to specific directory
    # save_path = "search_results/" + date + "/" + nick + ".json"
    save_path = os.path.join(getWorkDir(), results_path, nick+".json")
    print("SAVE PATH: ", save_path)
    #os.makedirs(os.path.dirname(save_path), exist_ok=True)
    with open(save_path, "w") as outfile:
        json.dump(result, outfile, sort_keys=True, indent=4)


def getName(item):
    """Gets the name of the item

    But at first, the function checks if the item is valid.

    :param item: item of dictionary to be validated
    :return: Returns item name if valid, otherwise None
    """
    name = None
    try:
        name = item["tool"]["name"]
        include = item["tool"]["include"]
    except KeyError:
        return name
    if include:
        return name
    # print(f"{name} include: False")
    return None


def getPageItems(query, page):
    """Gets and returns the items in page

    Function sends REST request to the API and checks the items.
    If response and it's fields are valid, returns the list of urls.
    Otherwise, it returns 'None' time module pro

    :param query: Search term used with the API
    :param page: The current page of items
    :return: Returns the list of URLs or 'None'
    """

    start = 10 * page + 1
    url = f"https://www.googleapis.com/customsearch/v1?key={key}&cx={cx}&start={start}&q={query}"
    results = []

    current_delay = 1
    max_delay = 32

    while True:
        try:
            response = requests.request("GET", url, timeout=5)
            response.raise_for_status()
        except HTTPError as http_err:
            print(f"HTTP error occurred: {http_err}")
            if current_delay > max_delay:
                print("Too many retry attempts. Returning...")
                return None
            print("Waiting about", current_delay, "seconds before retrying.")
            delay = current_delay + randint(0, 1000) / 1000.0
            # sleep(current_delay + round(random(), 3))
            sleep(delay)
            current_delay *= 2
            continue

        except requests.exceptions.Timeout:
            print("Timeout occurred")
        except Exception as err:
            print(f"HTTP error occurred: {err}")
            if current_delay > max_delay:
                print("Too many retry attempts. Returning...")
                return None
            print("Waiting about", current_delay, "seconds before retrying.")
            delay = current_delay + randint(0, 1000) / 1000.0
            # sleep(current_delay + round(random(), 3))
            sleep(delay)
            current_delay *= 2
            continue
        res_text = json.loads(response.text)
        break
    try:
        if page == 0:
            totRes = res_text["searchInformation"]["totalResults"]
            results.append(totRes)
            print(f"Total Results: {totRes}")
        results.extend([item["link"] for item in res_text["items"]])
        # TODO: check if nextpage exists
    except KeyError:
        return None
    return results


def customSearch():
    """The function

    This starts the search and calls function accordingly.
    The function prints the progress in terminal.
    """
    #starting_point = False
    starting_point = "bro"

    print("Starting the custom search from", end=" ")
    if starting_point:
        print(f"{starting_point}...\n")
    else:
        print(f"the beginning...\n")
    tools = readDB(db_loc)
    for tool in tools["tools"]:
        # Gets nick for saving purposes
        nick = tool["tool"]["nick"]
        # Skip finished queries
        if starting_point:
            if starting_point != nick:
                continue
            else:
                # Caught the place where last stopped
                starting_point = False
        print(f"{nick} -", end=" ")
        name = getName(tool)
        if not name:
            print("Invalid item, skipping...")
            continue

        # Initializing the urls list
        urls = []

        # Iterating throught pages max of 10 pages per tool
        for page in range(10):
            # print(f"{nick}'s", end=" ")
            res = getPageItems(name, page)
            print(f"    #{page+1}", end=" ")
            if not res:
                print("No results...")
                break
            urls.extend(res)
            print("Success...")  # , end=" ")
            sleep(0.2)

        # Save results to json file
        saveResults(nick, urls)
        print("- Saved!\n")
    print("\n------------------------\n", "Search Completed!", sep="")


def main():
    # TODO: Print time elapsed
    try:
        customSearch()
    except KeyboardInterrupt:
        print("Run interrupted.")


if __name__ == "__main__":
    main()
