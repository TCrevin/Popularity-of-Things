from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor
from bs4 import BeautifulSoup
import time
from urllib import request, error
from psutil import cpu_count
import re
import requests
import subprocess
import os

# TODO: Implement ProcessPoolExecutor to spawn child processes DONE
# TODO: Get names of tools from tools.yaml and iterate through assigning 'master_link'
master_link = "Nmap" # Reference what we're using
# Fills Z array for given string str[]
def getZarr(string, z):
    n = len(string)

    # [L,R] make a window which matches
    # with prefix of s
    l, r, k = 0, 0, 0
    for i in range(1, n):

        # if i>R nothing matches so we will calculate.
        # Z[i] using naive way.
        if i > r:
            l, r = i, i

            # R-L = 0 in starting, so it will start
            # checking from 0'th index. For example,
            # for "ababab" and i = 1, the value of R
            # remains 0 and Z[i] becomes 0. For string
            # "aaaaaa" and i = 1, Z[i] and R become 5
            while r < n and string[r - l] == string[r]:
                r += 1
            z[i] = r - l
            r -= 1
        else:

            # k = i-L so k corresponds to number which
            # matches in [L,R] interval.
            k = i - l

            # if Z[k] is less than remaining interval
            # then Z[i] will be equal to Z[k].
            # For example, str = "ababab", i = 3, R = 5
            # and L = 2
            if z[k] < r - i + 1:
                z[i] = z[k]

            # For example str = "aaaaaa" and i = 2,
            # R is 5, L is 0
            else:

                # else start from R and check manually
                l = i
                while r < n and string[r - l] == string[r]:
                    r += 1
                z[i] = r - l
                r -= 1

# prints all occurrences of pattern
# in text using Z algo
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
def linkInLink(link): #TODO:  Terrible, terrible, terrible. Replace with Z algorithm in C
    req = requests.get(link, 'html.parser')
    print("{} is processing {}".format(os.getpid(), link))
    beep = req.text
    h = "".join(beep.splitlines())
    #try    #if master_link in req.text: # get hit
        #    print("=============!!! GOT HIT !!!=============")
        #    print("=============!!! GOT HIT !!!=============")
        #    print("=============!!! GOT HIT !!!=============")
        #    print("Time it took to check the document: ", time.time() - t1)
        #    return 1
        #else:
        #    print("No hit.")
        #    print("Time it took to check the document: ", time.time() - t1)
        #    return 0
    #except error.HTTPError:
        #print("403 Access Forbidden: ", link)
        #pass
    #print("Time it took to check the document: ", time.time() - t1)
    #t2 = time.time()
    try:
        #a = "1"
        #t = subprocess.Popen(['./zalgo', master_link, str(h)], stdout=subprocess.PIPE)
        #stdout = t.communicate()[0]
        #print("STDOUT: ", stdout.decode('utf-8'))
        #if stdout.decode('utf-8') == '1':
        t1 = time.time()
        if search(h, master_link):
            print("Time it took to use zalgo: ", time.time()-t1)
            return 1
        else:
            #print("No hit.")
            return 0
    except error.HTTPError:
        print("Forbidden 403 at :", link)
        return 0
cpu_count = cpu_count()
#print("CPU count: ", cpu_count)
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
def multinilkki_teloittaja(link): # TODO: Check if page is readable before using requests and get the header
    try:
        #list_of_results.append(linkInLink(link))
        if linkInLink(link):
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
results = 0
t1 = time.time()
#with ThreadPoolExecutor as executor:
    #for link, result in zip(list_of_links, executor.map(multinilkki_teloittaja, list_of_links)):
    #r = {executor.submit(multinilkki_teloittaja, list_of_links): for item in list_of_links}
    #for i in concurrent.futures.as_completed(r):
    #    data = i.result()
    #for link, result in
    #print("Result: ", result)
    #list_of_results.append(data)
for item in list_of_links:
    list_of_results.append(linkInLink(item))


print("Reference count: ", results)
print("List of results: ", list_of_results)

for result in list_of_results: # sum
    results += result

print(results)
print("Execution time: ", time.time() - t1)
#TODO : iterate through google results (100 links) and check if rt/rn > 0.5
#TODO : if so, add to valid terms and save to text file, check for cross reference
#TODO : from score

