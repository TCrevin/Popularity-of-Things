from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor
from tqdm import tqdm
import time
from urllib import request, error
import re
import requests
import traceback
from itertools import repeat
import json
import os
# TODO: Get results into individual .json files in /results/
# TODO: Add methods to filter out results
# TODO: Get all tools into a single .json in Reference_Count_Engine root
# TODO: Make script to build directories to docker output folder Do by 8.12 -Sami
# TODO: Assemble all together on 9.12
yaml_path = "~"  # TODO: Replace with Docker filesystem
docker_path = "/var/lib/output/"
work_dir = "/home/toni/scripts/Popularity_of_Things/"


def getWorkDir():
    return "/home/toni/scripts/Popularity_of_Things/"
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

def getTool(tool):
    try:
        with open("tools.json", "r") as f:
            tool_dict = {}
            data = json.load(f)
            tools = data["tools"]
            aa = tools[tool]["nick"] = tools[tool]["urls"]
            print("AA : ", aa)
            print("TOOL_DICT: ", tool_dict)
            tool_dict.update(aa)
            f.close()
        return tool_dict
    except KeyError:
        print("Home URLs not found.. Skipping {}".format(tool_dict))
        pass
    #except Exception as e:
        #print("Unknown error occured when getting {}: {}".format(tool, e))

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


def getGoogleHits(tool, work_dir):
    #print("Work_dir: ", work_dir)
    temp_path = os.path.join(work_dir, "Popularity-of-Things/Reference_Count_Engine/google_search_results/")
    #print("Temp path: ", temp_path)
    tooljson = tool + ".json"
    try:
        with open(os.path.join(temp_path, tooljson)) as f:
            count = json.load(f)
            #print("Opened: ", tool)
            f.close()
            return count[0]
    except FileNotFoundError:
        #print("{} does not exist".format(tooljson))
        pass



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
            beep = req.text
            h = "".join(beep.splitlines())

            if search(h, search_name):  # TODO: Curl link
                # print("Time it took to use zalgo: ", time.time()-t1)
                mentions += 1

    except error.HTTPError:
        print("Forbidden 403 at :", links)



def linkInFile(name, # TODO: Do filtering HERE
               search_url):  # Input the source file (link-name) name and list of links associated with name
    #print("Calling linkInFile")
    work_dir = getWorkDir()
    path = os.path.join(work_dir, "Popularity-of-Things/Reference_Count_Engine/pages/{}/".format(name))
    allhomeurls = getAllHomeUrls()
    #print("ALL HOME URLS: ", allhomeurls)
    references_to_current_name = 0              # St
    references_to_any_name = 0                  # Sr
    total_search_hit_count = getS(getNames(), getWorkDir()) #  Sd # FIXME Currently not working
    #a=False # Deleted return a
    template_dict = {name: {"St":"",
                            "Sr":"",
                            "Sd": str(total_search_hit_count.get(name)),
                            "S": sum(os.path.isfile(os.path.join(path, f)) for f in os.listdir(path))}}
    #print("TEMPLATE DICT: ", template_dict)
    template_json = json.dumps(template_dict)
    no = 0
    count_of_pages = sum(os.path.isfile(os.path.join(path, f)) for f in os.listdir(path))
    #print("Search urls: ", search_url)
    #print("Files in {}: {} ".format(name, os.listdir(path)))
    for numerator, file in enumerate(os.listdir(path)):
        #print("{}: Checking for {} from {}".format(numerator, search_url, file))

        try:
            with open("/home/toni/scripts/Popularity_of_Things/Popularity-of-Things/Reference_Count_Engine/pages/{}/{}".format(name, file)) as req:  # Open source file (filename is link.txt)
                #print("Opened: ", file)
                #print("Checking: ", "/home/toni/scripts/Popularity_of_Things/Popularity-of-Things/Reference_Count_Engine/pages/{}/".format(name)+file)
                source = req.readlines()
                h = ",".join(source)
                #print("Checking if {} in h.".format(search_url))
                if search(h, search_url): # TODO: Run search on every tool on page to get Sr
                    references_to_current_name += 1
                    #a=True
                    #req.close()
                else:
                    #print("No mention")
                    no+=1
                #for home_url in allhomeurls: # Are there mentions of any of the links from the
                ##    #print("HOME_URL: ", home_url)
                #    if search(h, home_url):
                #        print("Got hit")
                #        references_to_any_name += 1
                #        break
                #    else:
                #        pass

        except Exception as e:
            print("Error {} occurred".format(e))
            print(traceback.format_exc())

    temp_path = "/home/toni/scripts/Popularity_of_Things/Popularity-of-Things/Reference_Count_Engine/results/{}".format(name+"_results.txt")
    print("Neco_ARc")
    if os.path.isfile(temp_path):
        with open(temp_path, "r+") as f: # TODO: Write Sd, Sr, St and S as a .json
            print("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA")
            data = json.load(f)
            read_count = data['St']
            f.seek(0) # seek file
            f.truncate() # clear
            updated_count = read_count + references_to_current_name
            data['St'] = updated_count
            data['Sr'] = references_to_any_name
            print("THIS IS DATA: ", data)
            json.dump(data, f)
            f.close()
    else:
        with open(temp_path, "w") as f:
            print("BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB")
            template_json['St'] = references_to_current_name
            template_json['Sr'] = references_to_any_name
            print("THIS IS TEMPLATE_JSON: ", template_json)
            print("Wrote: ", temp_path)
            json.dump(template_json, f)
            f.close()
    #return a  # Return


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

def getAllHomeUrls():
    with open("tools.json", "r") as f:
        #print("Getting links and corresponding names")
        tool_list = []
        flat_tool_list = []
        data = json.load(f)
        #print("AAA", data)
        tools = data["tools"]
        for tool in tools:
            #print("TOOL: ", tool)
            try:
                #print(tool["tool"]["name"])
                tool_list.append(tool["tool"]["urls"])
            except KeyError:
                #print("Tool has no home URLs.. Skipping: ", tool)
                pass
            except Exception as e:
                print("Something went wrong in allHomeUrls(): {}".format(e))
                pass

        #print("This is tool_list: ", tool_list)
        for sublist in tool_list:
            for item in sublist:
                flat_tool_list.append(item)
        print("This is flat_tool_list: ", flat_tool_list)
        return flat_tool_list


def linksFromGoogleFiles(filename):
    list_of_links = []
    exclude = (".exe", ".tar.xz", ".zip", ".pdf", ".epub", ".dmg")
    with open(os.path.join( # TODO: Replace with work_dir for docker
            "/home/toni/scripts/Popularity_of_Things/Popularity-of-Things/Hit_Count_Engine/google/search_results/30"
            "-11-2021", # TODO: Date based google searches outdated, reformat the source in gsearch.py
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
        name.replace(".json", "")
        files.append(name)
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


def returner2(filename, home_urls):  # Input one link and then the name and search_urls list from tools.json
    print("Checking: ", filename)
    #work_dir = getWorkDir()
    print("WORK DIR: ", work_dir)
    try:  # TODO: Get S, St, Sr and Sd here (see page 3, formula 1)
        linkInFile(filename, home_urls)  # TODO: Rip
    except KeyboardInterrupt:
        print("Exiting program..")
        exit()
    #except Exception as e:
    ##    print("An unknown error occurred at {}: {}".format(filename, e))
     #   pass


def tempDict(): # Returns dictionary
    aa = {}
    for filename in queryNames():  # TODO change to in range, so can take in arguments
        aa[filename] = linksFromGoogleFiles(filename)
    return aa

def execute(filename, home_urls):
    print("Starting")
    with ProcessPoolExecutor(max_workers=80) as executor:  # Task is CPU bound not I/O bound, use processes.
        (executor.map(returner2, repeat(filename), home_urls))

def execute2(input_link, filename):
    list_of_results = []
    results = 0
    allhomeurls = getAllHomeUrls()
    print("ALLHOMEURLS: ", allhomeurls)
    with ThreadPoolExecutor() as executor:  # Task is I/O bound, not CPU bound, use threads.
        for link, result in zip(input_link, executor.map(returner2, input_link, repeat(filename), repeat(allhomeurls))):
            print("\n\n----------------")
            list_of_results.append(result) #

    for result in list_of_results:  # sum
        if result != None:
            results += result
        else:
            pass


def deleteResults():
    path = "/home/toni/scripts/Popularity_of_Things/Popularity-of-Things/Reference_Count_Engine/results/"
    for file in os.listdir(path):
        os.remove(os.path.join(path, file))


def getPages(): # Download pages to appropriate directories
    aa = tempDict() #TODO: Initial path as argument to function

    for filename in queryNames():
        aa[filename] = linksFromGoogleFiles(filename)
    with ThreadPoolExecutor() as executor:
        for filename, links in aa.items():
            list(tqdm(executor.map(getSources, repeat(filename), links), total=len(links)))

def getS(names, work_dir): # Argument getNames(), returns a dictionary with tool: count
    s_dict = {}
    for numerator, tool in enumerate(names):
        s_dict[format(tool)] = getGoogleHits(tool, work_dir)
    return s_dict

t1 = time.time()
def main():
    #deleteResults() # FIXME: FileNotFoundError
    for tool, homeurls in getNames().items():
        execute(tool, homeurls)
    s = getS(getNames(), getWorkDir()) # Get S here
    print("Total execution time: ", time.time() - t1)

main()
