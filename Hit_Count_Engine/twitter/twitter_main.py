import requests
import json
import ast
import subprocess
import time
import collections.abc
import copy
from functools import reduce
"""
Twitter API calls.
Maximum amount of Tweets to retrieve is limited to 100 per query.
Queries limited to 900 per 15 minutes.

Queries limited to 500,000 per month.

Count query limited to tweets over the past 7 days, can be narrowed down with
start_time, end_time parameters.

https://developer.twitter.com/en/docs/twitter-api/early-access

Keep track of remaining API calls as to not run out of them!
"""


# TODO: Add tracker for remaining amount of calls


class Fetch:
    def __init__(self, query):
        """
        :param query: defined search term for tweets tagged with #query
        """
        self.query = query
        self.bearer_token = "F8vjwbTQLdew9DilAjVVKiO5QoRcCLhu"
        self.payload = {}
        self.pwd_call = subprocess.Popen(["pwd"], stdout=subprocess.PIPE)
        self.resultsDir = self.pwd_call.stdout.readline().decode('utf-8').replace('\n', '')
        self.headers = {  # TODO: Replace to load bearer token from file in Docker instance.
            'Authorization': 'Bearer AAAAAAAAAAAAAAAAAAAAAOt8UAEAAAAAEN0BvdqkKaVE9slkjxdut6MPSXk'
                             '%3DI4q1yypw35bZx0KGloF8vjwbTQLdew9DilAjVVKiO5QoRcCLhu '

        }

    def getResultsDir(self):
        directory = self.resultsDir + "/results"
        return directory

    def listResultsDir(self):
        """List contents of directory where .json files are located"""
        process = subprocess.Popen(['ls', self.getResultsDir()], stdout=subprocess.PIPE)
        return process.communicate()[0].decode('utf-8')

    def getTweets(self):
        """
        Get recent tweets related to query (API limitation, limited to 100 of the most recent tweets)
        """
        url = "https://api.twitter.com/2/tweets/search/recent?query=%23{}&max_results=100".format(self.query)
        tweets_response = requests.request("GET", url, headers=self.headers, data=self.payload)
        tweets_response_text = json.loads(tweets_response.text)
        for tweet in tweets_response_text['data']:
            print(tweet['text'], "\n\n\n")

    def getCount(self):
        """
        Get count of query
        """
        url = "https://api.twitter.com/2/tweets/counts/recent?query=%23{}".format(self.query)
        count_response = requests.request("GET", url, headers=self.headers, data=self.payload)
        count_response_text = json.loads(count_response.text)
        return self.query, count_response_text['meta']['total_tweet_count']  # Return count [0] and related query [1]

    def __checkTimestamp(self, input_dict, query):
        print("DEBUG: Calling checkTimestamp()")
        #outdict = collections.defaultdict(lambda: collections.defaultdict(input_dict))
        val = input_dict.get(query, {}).get("timestamp", {})
        print("DEBUG Val: ", val)
        old_timestamp = int(val)
        new_timestamp = int(time.time())
        if old_timestamp - new_timestamp > 604800:
            return True
        else:
            return False

    def __exists(self, input_dict, query):
        print("DEBUG: ", query)
        get_query = input_dict.get("queries").get(query, "")
        print("DEBUG: __exists", get_query)
        if get_query:
            print("Query in dict")
        else:
            print("Query not in dict")

    def sortDict(self, input_dict): # FIXME: Broken. Sorting does not work. Old lambda function broken.
        print("DEBUG: Calling sortDict(): ", input_dict)
        largest_count = 0
        selected_item = ""
        test_dict = copy.deepcopy(input_dict)
        outfile = test_dict['queries']
        table = {}

        print("Type of outfile", type(outfile))
        item_count = len(outfile)
        output_dict = {"queries": {"":
                                       [{"count": "",
                                         "timestamp": str(int(time.time()))}]}}
        loop_counter = 0
        print("Item count: ", item_count)
        #print("AA: ", int(input_dict["queries"][query][0]["count"]))
        #while item_count > 0:
            #print("item_count: ", item_count)
        for item in outfile: # Get hashtable
            print("Item: ", item)
            print("Count", test_dict["queries"][item][0]["count"])
            d = {item: test_dict["queries"][item][0]["count"]}
            print("This is d: ", d)
            table.update(d)
            #outfile.pop(item)


        print("Hash table (unsorted): ", table)
        h = sorted(table.items(), key=lambda t: int(t[1]), reverse=True)
        print("Sorted table : ", h)
        for item in h: # Remove old items
            print("What's popping: ", item[0])
            outfile.pop(item[0])

        for x, item in enumerate(h): # Build new dictionary
            print("DEBUG: ", item)
            a = item[0]
            b = item[1]
            print("A: ", a)
            print("B: ", b)
            output_dict = {"queries": {a:
                                           [{"count": b,
                                             "timestamp": str(int(time.time()))}]}}
            self.deepUpdate(input_dict=test_dict, output_dict=output_dict)

        print("Contents of outfile: ", test_dict) # TODO: Return outfile
        return test_dict

    def getValues(self, input_dict, query):
        return input_dict["queries"][query][0]['timestamp'], input_dict["queries"][query][0]['count']

    def deepUpdate(self, input_dict, output_dict):
        for key, val in output_dict.items():
            if isinstance(val, collections.Mapping):
                tmp = self.deepUpdate(input_dict.get(key, []), val)
                input_dict[key] = tmp
            elif isinstance(val, list):
                input_dict[key] = (input_dict.get(key, []) + val)
            else:
                input_dict[key] = output_dict[key]
        return input_dict

    def __updateQuery(self, input_dict, query, value): # TODO: See below
        print("DEBUG Type of input_dict", type(input_dict))
        print("DEBUG: Calling addQuery")
        #query = str(self.getCount()[0])
        #value = str(self.getCount()[1])
        print("QUERY: ", type(query))
        timestamp = time.time()
        #outdict = collections.defaultdict(dict, input_dict)
        print("DEBUG: input_dict: ", input_dict)
        input_dict["queries"][query][0]["count"] = value
        input_dict["queries"][query][0]["timestamp"] = str(int(time.time()))
        print("DEBUG: DLC2: ", value)
        dlc = input_dict.get("queries").get(query, "")
        query_list = dict(dlc[0])["count"]
        print("DEBUG updated outdict: ", input_dict)
        #outdict[0][1]["count"] = value # TODO: Assignment not working correctly
        #outdict[0][1]["timestamp"] = timestamp
        return input_dict

    #def __addQuery(self, input_dict, query, value):


    def build(self, input_dict):
        print("DEBUG Type of input_dict", type(input_dict))
        print("Calling build")
        query = str(self.getCount()[0])
        value = str(self.getCount()[1])
        if self.__exists(input_dict, query) and self.__checkTimestamp(input_dict, query):
            print(1)
            input_dict = self.__updateQuery(input_dict, query, value)
            #input_dict = self.__sortDict(input_dict, query)
            return input_dict
        elif self.__exists(input_dict, query) and self.__checkTimestamp(input_dict, query):
            print(2)
            print("Query exists but it's not 7 days old yet.") # TODO: Return remaining time and print.
        elif not self.__exists(input_dict, query):
            print(3)
            #self.__sortDict(input_dict, query)
            input_dict = self.__updateQuery(input_dict, query, value)
            return input_dict


    def appendCount(self, input_dict): # TODO: This method does too many things. Refactor and remove. -Toni
        """
        Append the input dictionary of queries with results. Returned dictionary of query results is reverse
        sorted (high-to-low)
        Built-in sorted() absolutely the fastest way https://medium.com/@tuvo1106/how-fast-can-you-sort-9f75d27cf9c1
        """
        print("This is input dict: ", input_dict)
        output_dict = dict()
        nu_stamp = time.time()
        query = str(self.getCount()[0])
        value = str(self.getCount()[1])
        if query in input_dict.keys():
            print("DEBUG: Found query in queries!")
            old_stamp = int(input_dict[query]["timestamp"])
            if nu_stamp-old_stamp>604800: # older than a week, update
                input_dict.update({query: {"count":str(value), "timestamp":str(nu_stamp)}})
                sort_dict = sorted(input_dict.items(), key=lambda x: int(x["count"]), reverse=True)
                for v, k in sort_dict:
                    output_dict[v] = k
                return output_dict
        else:
            print("Query not in queries, resuming with updating table....")
            input_dict.update({query: {"count": str(value), "timestamp": str(int(nu_stamp))}})
            sort_dict = sorted(input_dict.items(), key=lambda x: int(x["count"]), reverse=True)
            for v, k in sort_dict:
                output_dict[v] = k
                return output_dict

    def readResults(self, filename):
        """Open and read file. File must be closed separately if writeResults() is not called"""
        try:
            file = open(filename)
            print("Type of file: ", type(file))
            data = json.load(file)
            #ding = data.replace("queries: ", '')
            return data
        except FileNotFoundError:
            self.readResults(filename) # User rechecks input


    def clearResults(self, file):
        """
        Clear file contents. Input file must be opened before calling method.
        """
        try:
            file.truncate(0)
        except FileNotFoundError:
            print("File not found, please recheck input.\n\n")
            self.clearResults(file)
        except:
            print("An unknown error occurred")

    def writeResults(self, file, output_dict):
        print("Calling write.")
        file.write(json.dumps(output_dict, indent=4, separators=(",",": ")))
        file.close()


class Error(Exception):
    """Base class"""
    pass


class ItemNotInListError(Error):
    """Raised when item not in list"""
    pass


def errorMsg():
    print("Invalid selection!\n Please try again.\n\n\n")


def main():
    global input_file, file
    mode_list = ['1', '2', 'X', 'x']
    print("Welcome.\n\n")
    while True:
        try:
            print("To exit the program, please press 'X' and 'Enter'.\n\n")
            query = input("Please input query: #")
            if query == 'X':
                print("Exiting program")
                quit()
            fetch = Fetch(query)
            mode = input("1 : Get tweets related to {0} from last 7 days\n\n"
                         "2 : Get the count of tweets related to {0}\n\n"
                         "[1/2?]: ".format(query))

            if mode == '1':
                fetch.getTweets()
            if mode == '2':  # TODO: Clear, write updated dict
                try:
                    print("Results files: \n\n", fetch.listResultsDir()) # list files in results dir # DO NOT DELETE COMMENT
                    infile = fetch.readResults("results/results2.json")
                    input_file = ast.literal_eval(str(infile))
                    file = open("results/results2.json", "r+")
                    fetch.getValues(input_file, query)
                    #print("Beep", beep)
                    fetch.clearResults(file)
                    input_file = fetch.sortDict(input_file,)
                    #output_dict = fetch.build(input_file)
                    #output_json = json.dumps(output_dict)
                    fetch.writeResults(file, fetch.build(input_file))

                    print("Completed fetch")
                except KeyError: # FIXME:
                    output_dict = {"queries": {query:
                                                   [{"count": fetch.getCount()[1],
                                                     "timestamp":str(int(time.time()))}]}}
                    inject = fetch.deepUpdate(input_dict=input_file, output_dict=output_dict)
                    fetch.writeResults(file, inject)
                    print("Test dict: ", inject)
                    infile = fetch.readResults("results/results2.json")
                    input_file = ast.literal_eval(str(infile))
                    fetch.sortDict(file)
                    fetch.writeResults(file, fetch.build(input_file))
                #except:
                #    print("FUCK")
            if mode == 'X' or 'x':
                print("Exiting program")
                quit()
            if mode not in mode_list:
                raise ItemNotInListError

        except ItemNotInListError:
            errorMsg()


if __name__ == "__main__":
    main()
