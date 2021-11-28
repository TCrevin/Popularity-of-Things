from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor
from bs4 import BeautifulSoup
import time
from urllib import request, error
import re
import requests
import json
import os

yaml_path = "~" # TODO: Replace with Docker filesystem

# TODO: Implement ProcessPoolExecutor to spawn child processes DONE
# TODO: Get names of tools from tools.yaml and iterate through assigning 'search_name'
# TODO: Get files from dir, use filenames as input
def getNames(): # TODO: Read directly from YAML
    with open("tools.json", "r") as f:
        print("Getting links and corresponding names")
        tool_dict = {}
        data = json.load(f)
        tools = data["tools"]
        for tool in tools:
            try:
                #print("Key: ", tool["tool"]["nick"], "URL: ", tool["tool"]["urls"])
                tool_dict[tool["tool"]["nick"]] = tool["tool"]["urls"]
                os.mkdir('/home/toni/scripts/Popularity_of_Things/Popularity-of-Things/Reference_Count_Engine/pages/{}'.format(tool["tool"]["nick"]))
            except KeyError:
                #print(tool)
                #print("KeyError raised at {}.\nSkipping....".format(tool))
                #print("Keyerror")
                pass
            except FileExistsError:
                tool_dict[tool["tool"]["nick"]] = tool["tool"]["urls"]

        print(tool_dict)

def linksFromFile():
    with open("tools.json", "r") as f:
        links = []
        data = json.load(f)
        tools = data["tools"]
        for tool in tools:
            try:
                links.append(tool)
            except KeyError:
                pass
        return links

#search_name = "Nmap" # Reference what we're using # TODO ^ append items to a list
#master_link = "https://wireshark.org"
# TODO: Read YAML file with a function, return to list
def getZarr(string, z):
    n = len(string)
    l, r, k = 0, 0, 0
    for i in range(1, n):
        if i > r:
            l, r = i, i
            while r < n and string[r - l] == string[r]:
                r += 1
            z[i] = r - l
            r -= 1
        else:
            k = i - l
            if z[k] < r - i + 1:
                z[i] = z[k]

            else:
                l = i
                while r < n and string[r - l] == string[r]:
                    r += 1
                z[i] = r - l
                r -= 1

def search(text, pattern):
    # Create concatenated string "P$T"
    concat = pattern + "$" + text
    l = len(concat)

    # Construct Z array
    z = [0] * l
    getZarr(concat, z)

    # now looping through Z array for matching condition
    for i in range(l):

        # if Z[i] (matched region) is equal to pattern
        # length we got the pattern
        if z[i] == len(pattern):
            print("Gottem badabing.")
            return True

def linkInLink(links, search_name): # Get count of mentions of name in links
    mentions = 0
    for link in links:
        try:
            req = requests.get(link, 'html.parser')
            print("{} is processing {}".format(os.getpid(), link))
            beep = req.text
            h = "".join(beep.splitlines())

            if search(h, search_name): # TODO: Curl link
                print("Time it took to use zalgo: ", time.time()-t1)
                mentions+=1

        except error.HTTPError:
            print("Forbidden 403 at :", link)

    print("Number of mentions for {}".format(search_name))
    return mentions

def linkList(master_links):
    html = request.urlopen(master_links)
    text = html.read()
    list_of_links = []
    plaintext = text.decode('utf8')
    links = re.findall("href=[\"\'](.*?)[\"\']", plaintext)  # TODO: Biggest problem is Unicode Decode Error from
    # .exe, tar.xz etc other file formats. Find a way to eliminate these from ever being executed

    exclude = (".exe", ".tar.xz", ".zip", ".pdf", ".epub", ".dmg")

    """
    Exclude items. Unicode Errors take an awful long time to process.
    """
    for link in links:
        #if "https://" in link and "text/html" in link.headers["content-type"]:
        if "https://" or "http://" in link and not link.endswith(exclude):
            list_of_links.append(link)
            print(link)

    print("Count of links: ", len(list_of_links))
    print("Called.")
    return list_of_links

def getSources(tool_name, tool_links): # TODO: Reformat into Docker format
    path = os.path.join("/home/toni/scripts/Popularity_of_Things/Popularity-of-Things/Reference_Count_Engine", tool_name)
    for link in tool_links:
        html = requests.get(link, 'html.parser')
        try:
            filename = os.path.join(path, link+".txt")
            with open(filename, 'w') as f:
                f.write(html.text)
                f.close()
        except FileNotFoundError:
            filename = os.path.join(path, link + ".txt")
            with open(filename, 'x') as f:
                f.write(html.text)
                f.close()

def linksFromFile(filename):
    list_of_links = []
    with open(os.path.join("/home/toni/scripts/Popularity_of_Things/Popularity-of-Things/Reference_Count_Engine/google_queries", filename)) as f:
        for line in f:
            list_of_links.append(line)
    return list_of_links

def queryNames(): # TODO: Reformat into Docker format
    names = os.listdir("/home/toni/scripts/Popularity_of_Things/Popularity-of-Things/Reference_Count_Engine/google_queries")
    files = []
    for name in names:
        print("Debug name: ", name)
        name.replace(".json", "")
        files.append(name)
    for file in files:
        print("File: ", file)
    return files

def multinilkki_teloittaja(link, name):
    try:
        #list_of_results.append(linkInLink(link))
        if linkInLink(link, name):
            return 1
        else:
            return 0
    except error.HTTPError:
        #print("403 Access Forbidden at {}".format(link))
        #exit()
        return 0
        #continue
    except UnicodeDecodeError:
        #print("Unicode Decode Error at {}".format(link))
        #xit()e
        return 0
        #continue
    except KeyboardInterrupt:
        print("Exiting program..")
        exit()
    #except:
    #    print("An unknown error occurred at {}".format(link))
        #continue

def execute():
    list_of_results = []
    debug_list_links = linkList(master_link)
    results = 0
    #t1 = time.time()

    with ThreadPoolExecutor() as executor: # Task is I/O bound, not CPU bound, use threads.
        for link, result in zip(debug_list_links, executor.map(multinilkki_teloittaja, debug_list_links)):
            #print("Result: ", result)
            list_of_results.append(result)



    print("Reference count: ", results)
    print("List of results: ", list_of_results)

    for result in list_of_results: # sum
        results += result

    print(results)
    #print("Execution time: ", time.time() - t1)
    #TODO : iterate through google results (100 links) and check if rt/rn > 0.5
    #TODO : if so, add to valid terms and save to text file, check for cross reference
    #TODO : from score
t1 = time.time()
master_links = getNames() # returns dict "tool": "url"
for filename in queryNames(): # TODO: Filter link output lists from additional characters like '\n', ',' etc.
    print(linksFromFile(filename))
#links = linksFromFile()
#print(queryNames())
#for i in master_links:
