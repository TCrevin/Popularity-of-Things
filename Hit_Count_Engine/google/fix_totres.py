import os
import requests, json
from requests.models import HTTPError
import yaml
from time import sleep
from datetime import datetime

key = "AIzaSyBDCfGzExKZN_hLv1XYCuB4K_iZWdvpfR0"
cx = "a400502691c2c4c3c"
db_loc = "../../yaml_db/tools.yaml"

now = datetime.now()
date = now.strftime("%m-%d-%Y")
test_yaml = """
tools:
  - tool:
      nick: "0trace"
      name: "0trace"
  - tool:
      nick: "wireshark"
      name: "Wireshark"
  - tool:
      nick: "3proxy"
      name: "3proxy"
"""


def main():
    starting_point = False

    with open(db_loc, "r") as stream:
        tools = yaml.load(stream, Loader=yaml.Loader)
        # tools = yaml.load(test_yaml, Loader=yaml.Loader)
        # print(tools)
        # return
    for tool in tools["tools"]:
        nick = tool["tool"]["nick"]
        if starting_point:
            if starting_point != nick:
                continue
            else:
                starting_point = False

        try:
            query = tool["tool"]["name"]
        except KeyError:
            print(nick + ": No name, skipping...")
            continue
        urls = []

        # Loop
        for page in range(10):
            break  # Fix missing totalResults, skip loop
            print(f"{nick} #{page+1}...", end=" ")
            start = 10 * page + 1
            start = 1
            url = f"https://www.googleapis.com/customsearch/v1?key={key}&cx={cx}&start={start}&q={query}"
            try:
                response = requests.request("GET", url)
                response.raise_for_status()
            except HTTPError as http_err:
                print(f"HTTP error occurred: {http_err}")
            except Exception as err:
                print(f"Other error occurred: {err}")
            else:
                res_text = json.loads(response.text)
            try:
                # print(response["queries"]["request"][0]["totalResults"])
                if page == 0:
                    totRes = res_text["searchInformation"]["totalResults"]
                    urls.append(totRes)
                    print(f"Total Results: {totRes}", end=" ")
                urls.extend([item["link"] for item in res_text["items"]])
                # TODO: check if nextpage exists
            # if response["queries"]["nextPage"][0]["totalResults"] == "0":
            #     break
            except KeyError:
                print("No items left")
                break
            print("Success!")
            sleep(0.2)

        # Save results to json file
        save_path = "search_results/" + date + "/" + nick + ".json"
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        with open(save_path, "r") as stream:
            urls = json.load(stream)
        try:
            test_int = int(urls[0])
            print(f"{nick} OK")
            continue
        except ValueError:
            url = f"https://www.googleapis.com/customsearch/v1?key={key}&cx={cx}&q={query}"
            try:
                response = requests.request("GET", url)
                response.raise_for_status()
            except HTTPError as http_err:
                print(f"HTTP error occurred: {http_err}")
            except Exception as err:
                print(f"Other error occurred: {err}")
            else:
                pass
            res_text = json.loads(response.text)
            try:
                totRes = res_text["searchInformation"]["totalResults"]
            except KeyError:
                print(json.dumps(res_text))
                continue
            urls.insert(0, totRes)
            print(f"{nick}'s total results: {totRes}")
            sleep(0.2)

        with open(save_path, "w") as outfile:
            json.dump(urls, outfile, sort_keys=True, indent=4)


if __name__ == "__main__":
    main()
