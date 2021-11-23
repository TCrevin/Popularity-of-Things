import os
import requests, json
import yaml
from datetime import datetime

key = "AIzaSyBDCfGzExKZN_hLv1XYCuB4K_iZWdvpfR0"
cx = "a400502691c2c4c3c"
db_loc = "../../yaml_db/tools.yaml"

now = datetime.now()
date = now.strftime("%m-%d-%Y")


def main():
    with open(db_loc, "r") as stream:
        tools = yaml.load(stream, Loader=yaml.Loader)
    i = 0
    for tool in tools["tools"]:
        # TODO: check if recent search
        i = i + 1
        if i >= 3:
            break
        try:
            nick = tool["tool"]["nick"]
            query = tool["tool"]["name"]
        except KeyError:
            print(nick + ": No name, skipping...")
            continue
        urls = []
        for page in range(10):
            start = 10 * page + 1
            url = f"https://www.googleapis.com/customsearch/v1?key={key}&cx={cx}&start={start}&q={query}"
            response = json.loads(requests.request("GET", url).text)
            try:
                # print(response["queries"]["request"][0]["totalResults"])
                urls.extend([item["link"] for item in response["items"]])
                # TODO: check if nextpage exists
            # if response["queries"]["nextPage"][0]["totalResults"] == "0":
            #     break
            except KeyError:
                print("No items left")
                break
        save_path = "search_results/" + nick + "/" + date + ".json"
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        with open(save_path, "w") as outfile:
            json.dump(urls, outfile, sort_keys=True, indent=4)


if __name__ == "__main__":
    main()
