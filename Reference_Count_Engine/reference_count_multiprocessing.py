from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor
from tqdm import tqdm
import time
from urllib import request, error
import re
import requests
from itertools import repeat
import json
import os

yaml_path = "~"  # TODO: Replace with Docker filesystem


def getNames():  # Read files from tools.yaml that was converted to .json
    with open("tools.json", "r") as f:
        #print("Getting links and corresponding names")
        tool_dict = {}
        data = json.load(f)
        tools = data["tools"]
        for tool in tools:
            try:
                # print("Key: ", tool["tool"]["nick"], "URL: ", tool["tool"]["urls"])
                tool_dict[tool["tool"]["nick"]] = tool["tool"]["urls"]
                os.mkdir(
                    '/home/toni/scripts/Popularity_of_Things/Popularity-of-Things/Reference_Count_Engine/pages/{}'.format(
                        tool["tool"]["nick"]))
            except KeyError:
                # print(tool)
                #print("KeyError raised at {}.\nSkipping....".format(tool))
                # print("Keyerror")
                pass
            except FileExistsError:
                tool_dict[tool["tool"]["nick"]] = tool["tool"]["urls"]

        return tool_dict


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


def getZarr(string, z):
    # print("Getting Zarr")
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
            # print("Gottem badabing.")
            return True


def linkInLink(links,
               search_name):  # Get count of mentions of name in links # TODO : Use links from tools.yaml as search_name
    mentions = 0
    exclude = (".exe", ".tar.xz", ".zip", ".pdf", ".epub", ".dmg")
    # print("Link from function!: ", links)
    try:
        if "https://" or "http://" in links and not links.endswith(exclude):  # TODO: Check for illegal links
            req = requests.get(links, 'html.parser', timeout=5)
            # print("{} is processing {}".format(os.getpid(), links))
            beep = req.text
            h = "".join(beep.splitlines())
            # print("H? : ", h)
            # print("Looking for: ", search_name)

            if search(h, search_name):  # TODO: Curl link
                # print("Time it took to use zalgo: ", time.time()-t1)
                mentions += 1

    except error.HTTPError:
        print("Forbidden 403 at :", links)


# TODO: Something wrong here. FIXME FIXME FIXME FIXME FIXME FIXME
def linkInFile(name,
               search_urls):  # Input the source file (link-name) name and list of links associated with name
    mentioned = False
    path = "/home/toni/scripts/Popularity_of_Things/Popularity-of-Things/Reference_Count_Engine/pages/{}/".format(name)
    for file in os.listdir(path):
        print(file)
        try:
            with open("/home/toni/scripts/Popularity_of_Things/Popularity-of-Things/Reference_Count_Engine/pages/{}/".format(name)+file) as req:  # Open source file (filename is link.txt)
                #print("Checking: ", "/home/toni/scripts/Popularity_of_Things/Popularity-of-Things/Reference_Count_Engine/pages/{}/".format(name)+file)
                source = req.readlines()
                h = ",".join(source)
                for link in search_urls:  # If the link is found, break. No need to check for any more links
                    if search(h, link):
                        mentioned = True
        except Exception as e:
            print("Error {} occurred".format(e))
        return mentioned  # Return


# TODO: Gather up

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
        # if "https://" in link and "text/html" in link.headers["content-type"]:
        if "https://" or "http://" in link and not link.endswith(exclude):
            list_of_links.append(link)
            print(link)
        else:
            pass


def getSources(tool_name, link):  # TODO: Reformat into Docker format
    # print("Getting links for  {}...".format(tool_name))

    formatted = tool_name.replace(".json", "")
    # print("Tool name: ", formatted)
    link_strip = link.replace("/", "\\")  # Swap / to \
    # print("Formatted: ", formatted)
    path = "/home/toni/scripts/Popularity_of_Things/Popularity-of-Things/Reference_Count_Engine/pages/{}/{}".format(
        formatted, link_strip)
    try:
        #print("This is path: ", path)
        if os.path.isdir(
                "/home/toni/scripts/Popularity_of_Things/Popularity-of-Things/Reference_Count_Engine/pages/{}".format(
                        formatted)):
            if os.path.isfile(path):  # TODO: Timestamp/duplicate checking here
                print("{} exists.. Skipping".format(formatted))  #
            elif not os.path.isfile(path):
                with open(path, 'w') as f:
                    html = requests.get(link, 'html.parser',
                                        timeout=5)  # Decreasing timeout will decrease execution # Need to preprocess links to exclude .pdf, .exe etc.
                    # print("Wrote {} to {}".format(link_strip, path))
                    f.write(html.text)
            else:
                raise FileNotFoundError
        else:
            print("DEBUG Tool has no URLs to compare it to, skipping")
            pass
    except FileNotFoundError as e:
        print("An unknown FileNotFoundError triggered: ", e)
        pass
    except requests.exceptions.ReadTimeout:
        print("Timeout at {}".format(link))
        pass
    except Exception as e:
        print("An error occurred at {}".format(link))
        print(e)
        pass


def linksFromGoogleFiles(filename):
    list_of_links = []
    exclude = (".exe", ".tar.xz", ".zip", ".pdf", ".epub", ".dmg")
    with open(os.path.join(
            "/home/toni/scripts/Popularity_of_Things/Popularity-of-Things/Hit_Count_Engine/google/search_results/30"
            "-11-2021", # TODO: Date based google searches outdated, reformat the source
            filename)) as f:
        for line in json.load(f):
            if line.startswith("https://") and not line.endswith(exclude) or line.startswith(
                    "http://") and not line.endswith(exclude):
                # print("DEBUG Line: ", line)
                list_of_links.append(line)
            else:
                print("ENDED with exclude: ", line)
                pass
    return list_of_links


def queryNames():  # TODO: Reformat into Docker format
    names = os.listdir(
        "/home/toni/scripts/Popularity_of_Things/Popularity-of-Things/Hit_Count_Engine/google/search_results/30-11-2021")
    files = []
    for name in names:
        # print("Debug name: ", name)
        name.replace(".json", "")
        files.append(name)
    # for file in files:
    # print("File: ", file)
    return files


def returner(link, name):
    try:
        # list_of_results.append(linkInLink(link))
        # print("Multinilkki link: {} and name {}".format(link, name))
        if linkInLink(link, name):  # TODO Bring name here.
            return 1
        else:
            return 0
    except error.HTTPError:
        print("403 Access Forbidden at {}".format(link))
        # exit()
        return 0
        # continue
    except UnicodeDecodeError:
        print("Unicode Decode Error at {}".format(link))
        # xit()e
        return 0
        # continue
    except KeyboardInterrupt:
        print("Exiting program..")
        exit()
    except Exception as e:
        print("An unknown error occurred at {}".format(link))
        print(e)
        pass


def returner2(filename, home_urls):  # Input one link and then the name and search_urls list from tools.json
    try:  # TODO: Get S, St, Sr and Sd here (see page 3, formula 1)
        if linkInFile(filename, home_urls):  # TODO: Rip
            return 1
        else:
            return 0
    except KeyboardInterrupt:
        print("Exiting program..")
        exit()
    except Exception as e:
        print("An unknown error occurred at {}".format(e))
        pass


def tempDict():
    aa = {}
    for filename in queryNames():  # TODO change to in range, so can take in arguments
        aa[filename] = linksFromGoogleFiles(filename)
    # for key, value in aa.items():
    # print(key, " : ", value)
    return aa


def execute(filename, home_urls): # TODO: Input links from tools.json and
    list_of_results = []
    results = 0
    with ThreadPoolExecutor() as executor:  # Task is I/O bound, not CPU bound, use threads.
        for link, result in zip(filename, executor.map(returner2, repeat(filename), home_urls)):
            list_of_results.append(result)

    for result in list_of_results:  # sum
        if result != None:
            results += result
        else:
            pass
    print("Count of mentions of {} in the links provided: {}".format(home_urls, results))

def execute2(input_link, filename):
    list_of_results = []
    results = 0
    with ThreadPoolExecutor() as executor:  # Task is I/O bound, not CPU bound, use threads.
        for link, result in zip(input_link, executor.map(returner2, input_link, repeat(filename))):
            list_of_results.append(result)

    for result in list_of_results:  # sum
        if result != None:
            results += result
        else:
            pass
    print("Count of mentions of {} in the links provided: {}".format(filename, results))


def getPages():
    aa = tempDict()
    # for number, i in enumerate(aa.items()):
    # print(number, ": ", i)
    for filename in queryNames():
        aa[filename] = linksFromGoogleFiles(filename)
    with ThreadPoolExecutor() as executor:
        for filename, links in aa.items():
            list(tqdm(executor.map(getSources, repeat(filename), links), total=len(links)))
    # print("Execution time: ", time.time() - t1)


t1 = time.time()
# links = linksFromFile()
# asd = linksFromGoogleFiles()
# master_links = getNames() # returns dict "tool": "url"
# with ThreadPoolExecutor() as executor:
# for name, link in master_links:
# beep = linksFromGoogleFiles()
#    search_term = filename.replace(".json", "")
#    print("SEARCH TERM: ", search_term)
# for link in linksFromGoogleFiles(filename):
# print("{}: ".format(filename), linksFromGoogleFiles(filename))
# print(filename, " :",linksFromGoogleFiles(filename))
#    execute(linksFromGoogleFiles(filename), search_term)
#    #execute(linksFromGoogleFiles(filename), search_term)
# print("AA: ", aa)
thing = getNames()
for tool, homeurls in thing.items():
    execute(tool, homeurls)
    #print(tool, ": ", homeurls)
# TODO: IMPLEMENT ProcessPoolExecutor by dividing contents of file count n with cpu_count
#getPages() # This downloads all the pages
#for tool, homeurls in thing.items():
#    execute(tool, homeurls)
# getNames()
print("Total execution time: ", time.time() - t1)
# for i in master_links:
