import http.client
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor
from datetime import date
import gsearch
import OpenSSL
from tqdm import tqdm
import time
from urllib import request, error
from bs4 import BeautifulSoup, SoupStrainer
import re
from collections import OrderedDict
import requests
import math
import traceback
from itertools import repeat
import json
import os

# TODO: Cross-reference count. Get.
# TODO: Make script to build directories to docker output folder Do by 8.12 -Sami
# TODO: Assemble all together on 9.12
# TODO: S is very large for generally defined terms like meat, juicy-potato. Final pN absurdly high due to this
yaml_path = "~"  # TODO: Replace with Docker filesystem
docker_path = "/var/lib/output/"
work_dir = "/home/toni/scripts/Popularity_of_Things/"


def getWorkDir(): # TODO: Docker
    #return "/home/toni/scripts/Popularity_of_Things/"
    return "/var/lib/output/"

def createDirs():
    os.mkdir(os.path.join(getWorkDir(), "Popularity-of-Things"))
    os.mkdir(os.path.join(getWorkDir(), "Popularity-of-Things/Reference_Count_Engine"))
    os.mkdir(os.path.join(getWorkDir(), "Popularity-of-Things/Reference_Count_Engine/pages"))
    os.mkdir(os.path.join(getWorkDir(), "Popularity-of-Things/Reference_Count_Engine/google_search_results"))
    os.mkdir(os.path.join(getWorkDir(), "Popularity-of-Things/Reference_Count_Engine/results"))



def getNames():  # Read files from tools.yaml that was converted to .json # TODO: DOCKER
    with open("tools.json", "r") as f:
        tool_dict = {}
        data = json.load(f)
        tools = data["tools"]
        path = os.path.join(getWorkDir(), "Popularity-of-Things/Reference_Count_Engine")
        #print("PATH: ", path)
        for tool in tools:
            try:
                tool_dict[tool["tool"]["nick"]] = tool["tool"]["urls"]
                os.mkdir(os.path.join(path, 'pages/{}'.format(
                        tool["tool"]["nick"])))
            except KeyError:
                #print("No home URLs for {}. Skipping..".format(tool))
                pass
            except FileExistsError:
                tool_dict[tool["tool"]["nick"]] = tool["tool"]["urls"]

        return tool_dict

def getTools():
    with open("tools.json", "r") as f:
        tool_list = []
        data = json.load(f)
        tools = data["tools"]
        for tool in tools:
            try:
                tool_list.append(tool["tool"]["nick"])
            except KeyError:
                #print("No home URLs for {}. Skipping..".format(tool))
                pass
    return tool_list


def getTool(tool):
    try:
        with open("tools.json", "r") as f:
            tool_dict = {}
            data = json.load(f)
            tools = data["tools"]
            aa = tools[tool]["nick"] = tools[tool]["urls"]

            tool_dict.update(aa)
            f.close()
        return tool_dict
    except KeyError:
        print("Home URLs not found.. Skipping {}".format(tool_dict))
        pass
    except Exception as e:
        print("Unknown error occured when getting {}: {}".format(tool, e))
        pass

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
    temp_path = os.path.join(work_dir, "Popularity-of-Things/Reference_Count_Engine/google_search_results/")
    tooljson = tool + ".json"
    try:
        with open(os.path.join(temp_path, tooljson)) as f:
            count = json.load(f)
            f.close()
            return count[0]
    except FileNotFoundError:
        #print("{} does not exist. Skipping..".format(tooljson))
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
            return True


def linkInLink(links,
               search_name):  # Get count of mentions of name in links # TODO : Use links from tools.yaml as search_name
    mentions = 0
    exclude = (".exe", ".tar.xz", ".zip", ".pdf", ".epub", ".dmg")
    try:
        if "https://" or "http://" in links and not links.endswith(exclude):  # TODO: Check for illegal links
            req = requests.get(links, 'html.parser', timeout=5)
            beep = req.text
            h = "".join(beep.splitlines())

            if search(h, search_name):  # TODO: Curl link
                mentions += 1

    except error.HTTPError:
        print("Forbidden 403 at :", links)
        pass



def linkInFile(name):  # Input the source file (link-name) name and list of links associated with name
    try:
        print("Checking ", name)
        #print("PROCESS ID: ", os.getpid())
        work_dir = getWorkDir()
        references_to_current_name = 0 # FIXME: Problem with count is here. Fix.
        references_to_any_name = 0
        path = os.path.join(work_dir, "Popularity-of-Things/Reference_Count_Engine/pages/{}/".format(name))
        Sd = sum(os.path.isfile(os.path.join(path, f)) for f in os.listdir(path))
        allhomeurls = getAllHomeUrls()
        for item in allhomeurls:
            for homeurl in getHomeUrls(name):
                if item == homeurl:
                    #print("Removing: ", item)
                    allhomeurls.remove(item)
        #print("ALL HOME URLS: ", allhomeurls)
        # Sr
        #allhomeurls.remove(getHomeUrls(name)[0])
        # TODO: Make method to rip out
        total_search_hit_count = getS(getNames(), getWorkDir())
        template_dict = {name: [str(references_to_current_name), # St
                            str(references_to_any_name), # Sr
                            str(total_search_hit_count.get(name)), # S
                            Sd]} # Sd
        template_json = json.dumps(template_dict)
        #print("NAME: ", name, ": ", os.getpid())
        no = 0
    #print("SEARCH URL: ", home_url)
        for numerator, file in enumerate(os.listdir(path)):
            with open("/home/toni/scripts/Popularity_of_Things/Popularity-of-Things/Reference_Count_Engine/pages/{}/{}".format(name, file)) as req:  # Open source file (filename is link.txt)
                #print("Opening file {}.".format(file))
                source = req.read()
                links = []
                #links = re.findall("href=[\"\'](.*?)[\"\']", source)
                soup = BeautifulSoup(source)
                for link in soup.find_all('a'): # Get all links from page source
                    #if str(link):
                    links.append(link.get('href'))
                #print("LINKS TO USE: ", links)
                for item in allhomeurls:
                    if item in links:
                        allhomeurls.remove(item)

                #S1 = set(getHomeUrls(name))
                #print("S1: ", S1)
                #S2 = set(links)
                #print("S2: ", S2)
                #references_to_current_name = S1.intersection(S2)

                #else:
                #    no+=1
                for item in getHomeUrls(name):
                    for i, element in enumerate(links):
                        if element == None:
                            pass
                        elif item in element:
                            references_to_current_name += 1
                            break
                        else:
                            no += 1
                    break
                for item in allhomeurls:
                    for i, element in enumerate(links):
                        if element == None:
                            pass
                        elif item in element:
                            references_to_any_name += 1
                            #break
                    #break

        temp_path = os.path.join(getWorkDir(), "Popularity-of-Things/Reference_Count_Engine/results/{}".format(name+"_results.txt")) # TODO: DOCKER
        print("TRUE COUNT FOR {}: {}".format(name, references_to_current_name))  # TODO: Redo using for in range.
        #print(references_to_current_name)
        print("TRUE ALL COUNT FOR {}: {}".format(name, references_to_any_name))
        print("TRUE FILES IN FOLDER COUNT FOR {}: {}".format(name, sum(
            os.path.isfile(os.path.join(path, f)) for f in os.listdir(path))))
        with open(temp_path, "w") as f:
            data = json.loads(template_json)
            data[name][0] = str(references_to_current_name)
            data[name][1] = str(references_to_any_name)
            json.dump(data, f)
            f.close()
    except KeyError:
        pass
    except FileNotFoundError:
        pass
    except Exception as e:
        print(e)
        print(traceback.format_exc())
        pass



def filterAndAssemble(): # FIXME: All results undefined for whatever reason
    work_dir = getWorkDir()
    #print("WORK DIR: ", work_dir)
    results_dir = 'Popularity-of-Things/Reference_Count_Engine/results'
    filepath = os.path.join(work_dir, results_dir)
    results_dict = {}
    for numerator, file in enumerate(os.listdir(filepath)):
        try:
            with open(os.path.join(filepath, file), "r") as f:
                data = json.load(f)
                tool = file.replace("_results.txt", "")
                St = data[tool][0]
                Sr = data[tool][1]
                S = data[tool][2]
                Sd  = data[tool][3]
                if ((float(St)/float(Sr))>=0.5) and ((float(Sr)/float(Sd))>=0.2): # TODO: Test with Sr/Sd >= 0.3 and 0.28
                    pn = str(math.log(math.log((int(St)/int(Sd))*int(S))))
                    results_dict.update({tool: pn})
                else:
                    pn = "Undefined"
                    results_dict.update({tool: pn})
        except ZeroDivisionError:
            pn = "Undefined"
            results_dict.update({tool: pn})
            pass
        except Exception as e:
            print("An unknown error occured at {}: {}".format(file, traceback.format_exc()))
            pass

    with open("name_search_results_{}.txt".format(date.today()), "w") as f:
        sorted_dict = {key:val for key, val in results_dict.items() if val != "Undefined"}

        sorted_results = OrderedDict(sorted(sorted_dict.items(), key=lambda x: x[1], reverse=True))
        json.dump(sorted_results, f, indent=4)
        f.close()
    return results_dict



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
        if "https://" or "http://" in link and not link.endswith(exclude):
            list_of_links.append(link)
            print(link)
        else:
            pass


def getSources(tool_name, link):  # TODO: Docker
    formatted = tool_name.replace(".json", "")
    link_strip = link.replace("/", "\\")  # Swap / to \
    path = os.path.join(getWorkDir(), "Popularity-of-Things/Reference_Count_Engine/pages/{}/{}".format(
        formatted, link_strip))
    #print("PATH: ", path)
    try:
        if os.path.isdir(os.path.join(getWorkDir(), "Popularity-of-Things/Reference_Count_Engine/pages/{}".format(formatted))):
            if os.path.isfile(path):  # TODO: Timestamp/duplicate checking here
                print("{} exists.. Skipping".format(formatted))  #
            elif not os.path.isfile(path):

                with open(path, 'w') as f:
                    html = requests.get(link, 'html.parser', # TODO Insert Pycurl here.
                                        timeout=5)  # Decreasing timeout will decrease execution # Need to preprocess links to exclude .pdf, .exe etc.
                    f.write(html.text)
            else:
                #print("DDD")
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
    except OpenSSL.SSL.Error:
        print(traceback.format_exc())
        pass
    except http.client.RemoteDisconnected:
        print(traceback.format_exc())
        pass
    except requests.exceptions.ConnectionError:
        print(traceback.format_exc())
        pass
    except Exception as e:
        #print(e)
        print(traceback.format_exc())
        pass

def getAllHomeUrls():
    with open("tools.json", "r") as f:
        tool_list = []
        flat_tool_list = []
        data = json.load(f)
        tools = data["tools"]
        for tool in tools:
            try:
                tool_list.append(tool["tool"]["urls"])
            except KeyError:
                pass
            except Exception as e:
                pass
        remove = ["https://", "http://", "https://www.", "http://www."]
        for sublist in tool_list:
            for item in sublist:
                for url in remove:
                    if url in item:
                        aa = item.replace(url, "")
                        flat_tool_list.append(aa)
        for item in flat_tool_list:
            if item.startswith("www."):
                flat_tool_list.remove(item)
                aa = item.replace("www.", "")
                flat_tool_list.append(aa)
        return flat_tool_list



def linksFromGoogleFiles(filename): # TODO: Docker
    list_of_links = []
    exclude = (".exe", ".tar.xz", ".zip", ".pdf", ".epub", ".dmg")
    with open(os.path.join(getWorkDir(),
            "Popularity-of-Things/Reference_Count_Engine/google_search_results/", # TODO: Date based google searches outdated, reformat the source in gsearch.py
            filename)) as f:
        for line in json.load(f):
            if line.startswith("https://") and not line.endswith(exclude) or line.startswith(
                    "http://") and not line.endswith(exclude):
                list_of_links.append(line)
            else:
                #print("ENDED with exclude: ", line)
                pass
    return list_of_links


def queryNames():  # TODO: Docker
    names = os.listdir(os.path.join(getWorkDir(),
            "Popularity-of-Things/Reference_Count_Engine/google_search_results/"))
    files = []
    for name in names:
        if name.endswith(".json"):
            name.replace(".json", "")
            files.append(name)
        else:
            pass
    return files


def returner(link, name):
    try:
        if linkInLink(link, name):  # TODO Bring name here.
            return 1
        else:
            return 0
    except error.HTTPError:
        print("403 Access Forbidden at {}".format(link))
        return 0
    except UnicodeDecodeError:
        print("Unicode Decode Error at {}".format(link))
        return 0
    except KeyboardInterrupt:
        print("Exiting program..")
        exit()


def returner2(filename):  # Input one link and then the name and search_urls list from tools.json
    try:  # TODO: Get S, St, Sr and Sd here (see page 3, formula 1)
        linkInFile(filename)  # TODO: Rip
    except KeyboardInterrupt:
        print("Exiting program..")
        exit()


def tempDict(): # Returns dictionary
    aa = {}
    for filename in queryNames():  # TODO change to in range, so can take in arguments
        #print("AA: ", filename)
        aa[filename] = linksFromGoogleFiles(filename)
    return aa

def getHomeUrls(tool):
    #aa = {}
    bb = []
    remove = ["https://", "http://", "https://www.", "http://www."]
    try:
        with open("tools.json", "r") as f:
            data = json.load(f)
        for numerator, i in enumerate(data["tools"]):
            try:
                if i["tool"]["nick"] == tool:
                    for tool in i["tool"]["urls"]:
                        for item in remove:
                            if item in tool:
                                dd = tool.replace(item, "")
                                bb.append(dd)

                else:
                    pass

            except KeyError:
                continue
        for item in bb:
            if item.startswith("www"):
                bb.remove(item)
        return bb
    except Exception as e:
        pass

def execute(tool):
    print("Starting")
    print("Amount of items: ", len(tool))
    time.sleep(3)
    with ProcessPoolExecutor(max_workers=10) as executor:  # Task is CPU bound not I/O bound, use processes.
    #with ProcessPoolExecutor(max_workers=(os.cpu_count()*5)) as executor: # WARNING: DO NOT SET MULTIPLIER OVER 20
        for item in tool:
            executor.submit(returner2, item)


def execute2(input_link, filename):
    list_of_results = []
    results = 0
    allhomeurls = getAllHomeUrls()
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
    path = "Popularity-of-Things/Reference_Count_Engine/results/"
    work_dir = getWorkDir()
    filepath = os.path.join(work_dir, path)
    for numerator, file in enumerate(os.listdir(filepath)):
        os.remove(os.path.join(filepath, file))

def getPages(): # Download pages to appropriate directories
    try:
        aa = tempDict() #TODO: Initial path as argument to function
        for filename in queryNames():
            aa[filename] = linksFromGoogleFiles(filename)
        with ThreadPoolExecutor() as executor:
            for filename, links in aa.items():
                list(tqdm(executor.map(getSources, repeat(filename), links), total=len(links)))
    except Exception:
        pass

def getS(names, work_dir): # Argument getNames(), returns a dictionary with tool: count
    s_dict = {}
    for numerator, tool in enumerate(names):
        s_dict[format(tool)] = getGoogleHits(tool, work_dir)
    return s_dict

def choose():
    user_input = input("Do you wish to download new pages? [y/N]: ")
    valid_choices = ['y', 'Y', 'n', 'N']
    if user_input in valid_choices:
        return user_input
    else:
        print("Please check your input.")
        choose()


def main():
    try:
        createDirs()
        if not os.path.isdir(os.path.join(getWorkDir(), "Popularity-of-Things/Reference_Count_Engine/pages/")):
            os.mkdir(os.path.join(getWorkDir(), "Popularity-of-Things/Reference_Count_Engine/pages"))
        t1 = time.time()
        dr = choose()
        gsearch.customSearch()
        getNames()
        getPages()
        execute(getTools())
        filterAndAssemble()
        print("Total execution time: ", time.time() - t1)  # TODO: Remove
    except OpenSSL.SSL.Error:
        print(traceback.format_exc())
        pass
    except http.client.RemoteDisconnected:
        print(traceback.format_exc())
        pass
    except requests.exceptions.ConnectionError:
        print(traceback.format_exc())
        pass
    except Exception as e:
        #print(e)
        print(traceback.format_exc())
        pass
    #deleteResults()
    #execute(getTools())
    #filterAndAssemble()
        #print("Total execution time: ", time.time() - t1) # TODO: Remove

main()
#print(getWorkDir())
#filterAndAssemble()
#getSources("beef.json", )
#linkInFile("beef")
#linkInFile("wireshark")
#linkInFile("nmap")
#gsearch.customSearch()