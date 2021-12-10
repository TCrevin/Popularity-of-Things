from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor
from tqdm import tqdm
import time
from urllib import request, error
from bs4 import BeautifulSoup, SoupStrainer
import re
import requests
import math
import traceback
from itertools import repeat
import json
import os

# TODO: FIXME at filterAndAssemble (all results undefined)
# TODO: Check if directories exist, if not, create
# TODO: Make script to build directories to docker output folder Do by 8.12 -Sami
# TODO: Assemble all together on 9.12
yaml_path = "~"  # TODO: Replace with Docker filesystem
docker_path = "/var/lib/output/"
work_dir = "/home/toni/scripts/Popularity_of_Things/"


def getWorkDir():
    return "/home/toni/scripts/Popularity_of_Things/"


def getNames():  # Read files from tools.yaml that was converted to .json
    with open("tools.json", "r") as f:
        tool_dict = {}
        data = json.load(f)
        tools = data["tools"]
        for tool in tools:
            try:
                tool_dict[tool["tool"]["nick"]] = tool["tool"]["urls"]
                os.mkdir(
                    '/home/toni/scripts/Popularity_of_Things/Popularity-of-Things/Reference_Count_Engine/pages/{}'.format(
                        tool["tool"]["nick"]))
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
        allhomeurls = getAllHomeUrls()                  # Sr
        allhomeurls.remove(getHomeUrls(name)[0])
        # TODO: Make method to rip out
        total_search_hit_count = getS(getNames(), getWorkDir())
        template_dict = {name: [str(references_to_current_name), # St
                            str(references_to_any_name), # Sr
                            str(total_search_hit_count.get(name)), # S
                            sum(os.path.isfile(os.path.join(path, f)) for f in os.listdir(path))]} # Sd
        template_json = json.dumps(template_dict)
        #print("NAME: ", name, ": ", os.getpid())
        no = 0
        homeurls = getHomeUrls(name)
        anyhomeurls = getAllHomeUrls()
        for item in getHomeUrls(name):
            anyhomeurls.remove(item)
        for item in anyhomeurls:
            if item == any(homeurls):
                print("DUPLICATE")
    #print("SEARCH URL: ", home_url)
        for numerator, file in enumerate(os.listdir(path)):
            with open("/home/toni/scripts/Popularity_of_Things/Popularity-of-Things/Reference_Count_Engine/pages/{}/{}".format(name, file)) as req:  # Open source file (filename is link.txt)
                #print("Opening file {}.".format(file))
                source = req.read()
                links = []
                #links = re.findall("href=[\"\'](.*?)[\"\']", source)
                soup = BeautifulSoup(source)
                for link in soup.find_all('a'): # Get all links from page source
                    links.append(link.get('href'))
                #print("LINKS TO USE: ", links)
                # Get allhomeurls. Check if links from source contain any
                #for i in links:

                for home_url in getHomeUrls(name): # TODO: What the fuck
                    #print("Home url: ", home_url)
                    #print("Checking for {} from {}".format(name, links))
                    #h = ",".join(source)
                    if filter(lambda element: home_url in element, links): # If any home url concerning that tool in any links from source, add
                        references_to_current_name += 1
                        #print("References to current name:", references_to_current_name)
                        #print("Hit {}: {}".format)
                    else:
                        #print("No hit.")
                        no += 1
                #for _ in getAllHomeUrls():
                #for home_url in getAllHomeUrls():
                   # print("Home_url: ", home_url)
                if filter(lambda element: any(allhomeurls) in element, links):
                #if any(tool_home_url in allhomeurls for tool_home_url in links): # If any home_url in allhomeurls in links from source, add
                        #print("AA")
                        references_to_any_name += 1
                else:
                     pass

                    #print("References to any name:", references_to_any_name)

                #for home_url in allhomeurls:
                    #print("Checking for {} in {}".format(home_url, name))
                    # print("Checking home URL: ", home_url)
                    #links = re.findall("href=[\"\'](.*?)[\"\']", source)

                #    if home_url in links:
                    #    print("Gottem")
                #        references_to_any_name += 1
                #        print("References to any name:", references_to_any_name)
                #else:
                    #pass

        temp_path = "/home/toni/scripts/Popularity_of_Things/Popularity-of-Things/Reference_Count_Engine/results/{}".format(name+"_results.txt")
    #if any(home_url in h for home_url in allhomeurls):
    #    references_to_any_name += 1
    #print("ALL HOME URLS {}: {}".format(allhomeurls)
    #print("Done checking Home URLs.")
        print("TRUE COUNT FOR {}: {}".format(name, references_to_current_name)) # TODO: Redo using for in range.
        print("TRUE ALL COUNT FOR {}: {}".format(name, references_to_any_name))
        print("TRUE FILES IN FOLDER COUNT FOR {}: {}".format(name, sum(os.path.isfile(os.path.join(path, f)) for f in os.listdir(path))))
        #if os.path.isfile(temp_path):
        #    print("AAAAAAAAAAAAAAA")
        #    with open(temp_path, "r+") as f: # TODO: Write Sd, Sr, St and S as a .json
        ##        data = json.load(f)
         #       m = json.loads(data)
         #       read_count = int(m[name][0])
         #       f.seek(0) # seek file
         ##       f.truncate() # clear
          #      updated_count = read_count + references_to_current_name
          #      m[name][0] = str(updated_count)
          #      m[name][1] = str(references_to_any_name)
          #      json.dump(data, f)
          #      f.close()
        #else:
          #  print("BBBBBBBBBBBBBBBB")
        with open(temp_path, "w") as f:
            data = json.loads(template_json)
            data[name][0] = str(references_to_current_name)
            data[name][1] = str(references_to_any_name)
            json.dump(data, f)
            f.close()
    except KeyError:
        #print(traceback.format_exc())
        #print(name)
        pass
    except FileNotFoundError:
        #print("Could not find {}. Skipping..".format(name))
        pass
    except Exception as e:
        #print(e)
        #print(traceback.format_exc())
        pass



def filterAndAssemble(): # FIXME: All results undefined for whatever reason
    work_dir = getWorkDir()
    #print("WORK DIR: ", work_dir)
    results_dir = 'Popularity-of-Things/Reference_Count_Engine/results'
    filepath = os.path.join(work_dir, results_dir)
    #print("FILEPATH: ", filepath)
    results_dict = {}
    for numerator, file in enumerate(os.listdir(filepath)):
        try:
            with open(os.path.join(filepath, file), "r") as f:
                print("Loading tool ", file)
                data = json.load(f)
                tool = file.replace("_results.txt", "")
                print(tool, " : ", data)
                St = data[tool][0]
                print(type(St))
                Sr = data[tool][1]
                S = data[tool][2]
                Sd  = data[tool][3]
                if (float(St)/float(Sr)>=0.5) and (float(Sr)/float(Sd)>=0.2):
                    print("DING")
                    pn = str(math.log(math.log((int(St)/int(Sd))*int(S))))
                    results_dict.update({tool: pn})
                else:
                    print("DONG")
                    pn = "Undefined"
                    results_dict.update({tool: pn})
        except ZeroDivisionError:
            print("FUCK")
            #print("Setting {} as undefined..".format(file))
            pn = "Undefined"
            results_dict.update({tool: pn})
            pass
        except Exception as e:
            print("An unknown error occured at {}: {}".format(file, traceback.format_exc()))
            pass

    #print("Done filtering. Assembling..")
    with open("name_search_results.txt", "w") as f:
        print("RESULTS: ", results_dict)
        #results_json = json.dumps(results_dict)
        json.dump(results_dict, f, indent=4)
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


def getSources(tool_name, link):  # TODO: Reformat into Docker format
    formatted = tool_name.replace(".json", "")
    link_strip = link.replace("/", "\\")  # Swap / to \
    path = "/home/toni/scripts/Popularity_of_Things/Popularity-of-Things/Reference_Count_Engine/pages/{}/{}".format(
        formatted, link_strip)
    try:
        if os.path.isdir(
                "/home/toni/scripts/Popularity_of_Things/Popularity-of-Things/Reference_Count_Engine/pages/{}".format(
                        formatted)):
            if os.path.isfile(path):  # TODO: Timestamp/duplicate checking here
                print("{} exists.. Skipping".format(formatted))  #
            elif not os.path.isfile(path):
                with open(path, 'w') as f:
                    html = requests.get(link, 'html.parser', # TODO: Pycurl here.
                                        timeout=5)  # Decreasing timeout will decrease execution # Need to preprocess links to exclude .pdf, .exe etc.
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
                #print("Something went wrong in allHomeUrls(): {}".format(e))
                pass

        for sublist in tool_list:
            for item in sublist:
                flat_tool_list.append(item)
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
    #print("Checking: ", filename)
    try:  # TODO: Get S, St, Sr and Sd here (see page 3, formula 1)
        linkInFile(filename)  # TODO: Rip
    except KeyboardInterrupt:
        print("Exiting program..")
        exit()


def tempDict(): # Returns dictionary
    aa = {}
    for filename in queryNames():  # TODO change to in range, so can take in arguments
        aa[filename] = linksFromGoogleFiles(filename)
    return aa

def getHomeUrls(tool):
    #aa = {}
    bb = []
    try:
        with open("tools.json", "r") as f:
            tool_list = []
            flat_tool_list = []
            data = json.load(f)
        for numerator, i in enumerate(data["tools"]):
            try:
                if i["tool"]["nick"] == tool:
                    #aa.update({i["tool"]['nick']:i["tool"]["urls"]})
                    for tool in i["tool"]["urls"]:
                        bb.append(tool)
                else:
                    pass

            except KeyError:
                #print("Didn't find {}. Skipping..".format(i))
                continue
        #print("Tool: {}\t Links: {}".format(tool, bb))
        return bb
    except Exception as e:
        #print("Something went from getting {} home urls".format(tool))
        #print(e)
        pass

def execute(tool):
    print("Starting")
    print("Amount of items: ", len(tool))
    time.sleep(3)
    with ProcessPoolExecutor(max_workers=20) as executor:  # Task is CPU bound not I/O bound, use processes.
    #with ProcessPoolExecutor(max_workers=(os.cpu_count()*5)) as executor: # WARNING: DO NOT SET MULTIPLIER OVER 20
        for item in tool:
            executor.submit(returner2, item)


    #for item in tool:
    #    returner2(item)


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
        #print(file)


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


def main():
    t1 = time.time()
    deleteResults()
    #tools = getTools()
    #print(getNames().items())
#    for tool in tools:
#        print("{}".format(tool))
    execute(getTools())
    print("Total execution time: ", time.time() - t1)

#main()
linkInFile("wireshark")
#print(getHomeUrls("wireshark"))
#filterAndAssemble()
#for item in aa:
    #print(item)
