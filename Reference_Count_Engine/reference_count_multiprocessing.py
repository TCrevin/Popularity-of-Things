from concurrent.futures import ProcessPoolExecutor
from bs4 import BeautifulSoup
import time
from urllib import request, error
from psutil import cpu_count
import re
import requests

# TODO: Implement ProcessPoolExecutor to spawn child processes DONE
# TODO: Get names of tools from tools.yaml and iterate through assigning 'master_link'
master_link = "Nmap" # Reference what we're using


def linkInLink(link):
    html = request.urlopen(link)
    text = html.read()
    plaintext = text.decode('utf8')
    #links = re.findall("href=[\"\'](.*?)[\"\']", plaintext) # find links in plaintext
    req = requests.get(link, 'html.parser')
    print("Processing {}".format(link))
    print(type(req.text))
    try:

        if master_link in req.text: # get hit
            print("=============!!! GOT HIT !!!=============")
            print("=============!!! GOT HIT !!!=============")
            print("=============!!! GOT HIT !!!=============")
            return 1
        else:
            print("No hit.")
            return 0
    except error.HTTPError:
        print("403 Access Forbidden: ", link)
        pass


cpu_count = cpu_count()
print("CPU count: ", cpu_count)
count = 0
html = request.urlopen("https://wireshark.org")
text = html.read()
list_of_links = []
plaintext = text.decode('utf8')
links = re.findall("href=[\"\'](.*?)[\"\']", plaintext) # TODO: Biggest problem is Unicode Decode Error from .exe,
                                                        # TODO: tar.xz etc other file formats. Find a way to eliminate
                                                        # TODO: these from ever being executed

exclude = (".exe", ".tar.xz", ".zip", ".pdf", ".epub", ".dmg")


"""
Exclude items. Unicode Errors take an awful long time to process.
"""
for link in links:
    if "https://" in link and not link.endswith(exclude):
        list_of_links.append(link)
        print(link)

#for item in list_of_links:
#    print(item)

list_of_results = []

print("Count of links: ", len(list_of_links))

#for link in list_of_links:
def multinilkki_teloittaja(link): # TODO: Check if page is readable before
    try:
        #list_of_results.append(linkInLink(link))
        if linkInLink(link):
            return 1
        else:
            return 0
    except error.HTTPError:
        print("403 Access Forbidden at {}".format(link))
        #exit()
        return 0
        #continue
    except UnicodeDecodeError:
        print("Unicode Decode Error at {}".format(link))
        #xit()e
        return 0
        #continue
    except KeyboardInterrupt:
        print("Exiting program..")
        exit()
    except:
        print("An unknown error occurred at {}".format(link))
        #continue
results = 0
t1 = time.time()
with ProcessPoolExecutor() as executor:
    for link, result in zip(list_of_links, executor.map(multinilkki_teloittaja, list_of_links)):
        print("Result: ", result)
        list_of_results.append(result)



print("Reference count: ", results)
print("List of results: ", list_of_results)

for result in list_of_results: # sum
    results += result

print(results)
print("Execution time: ", time.time() - t1)


