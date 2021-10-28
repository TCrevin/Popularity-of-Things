import requests
import json
import ast
import subprocess
import time
import collections

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

    def __checkTimestamp(self, input_dict):
        print("DEBUG: Calling checkTimestamp()")
        outdict = collections.defaultdict(lambda: collections.defaultdict(input_dict))
        old_timestamp = int(outdict[0][1]["timestamp"])
        new_timestamp = int(time.time())
        if old_timestamp - new_timestamp > 604800:
            return True
        else:
            return False

    def __exists(self, input_dict, *keys):
        print("DEBUG: Calling __exists()")
        if not isinstance(input_dict, dict):
            raise AttributeError("Expected dict as first argument")
        if len(keys) == 0:
            raise AttributeError("Expected at least two arguments")
        _input_dict= input_dict
        for key in keys:
            try:
                _input_dict = _input_dict[key]
            except KeyError:
                print("Query not in input_dict")
                return False
        print("Query in input_dict")
        return True

    def __sortDict(self, input_dict):
        print("DEBUG: Calling sortDict(): ", input_dict)
        outfile = sorted(input_dict.items(), key=lambda key_value: key_value[1]['count']) # sort
        return outfile

    def __addQuery(self, input_dict, query, value): # TODO: See below
        print("DEBUG Type of input_dict", type(input_dict))
        print("DEBUG: Calling addQuery")
        #query = str(self.getCount()[0])
        #value = str(self.getCount()[1])
        timestamp = time.time()
        outdict = collections.defaultdict(dict, input_dict)
        print("DEBUG: Outdict: ", outdict)
        outdict[0][1] = str(query)
        outdict[0][1]["count"] = value # TODO: Assignment not working correctly
        outdict[0][1]["timestamp"] = timestamp
        return dict(outdict)

    def build(self, input_dict):
        print("DEBUG Type of input_dict", type(input_dict))
        print("Calling build")
        query = str(self.getCount()[0])
        value = str(self.getCount()[1])
        if self.__exists(input_dict, query) and self.__checkTimestamp(input_dict):
            input_dict = self.__addQuery(input_dict, query, value)
            input_dict = self.__sortDict(input_dict)
            return input_dict
        elif self.__exists(input_dict, query) and not self.__checkTimestamp(input_dict):
            print("Query exists but it's not 7 days old yet.") # TODO: Return remaining time and print.
        elif not self.__exists(input_dict, query):
            input_dict = self.__addQuery(input_dict, query, value)
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
                input_dict.update({query: {"count":value, "timestamp":nu_stamp}})
                sort_dict = sorted(input_dict.items(), key=lambda x: int(x['count']), reverse=True)
                for v, k in sort_dict:
                    output_dict[v] = k
                return output_dict
        else:
            print("Query not in queries, resuming with updating table....")
            input_dict.update({query: {"count": value, "timestamp": nu_stamp}})
            sort_dict = sorted(input_dict.items(), key=lambda x: int(x['count']), reverse=True)
            for v, k in sort_dict:
                output_dict[v] = k
                return output_dict

    def readResults(self, filename):
        """Open and read file. File must be closed separately if writeResults() is not called"""
        try:
            file = open(filename)
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
        file.write(str(output_dict))
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
            if mode == '2':  # TODO: Implement timestamp so if timestampAge > 7 days: clear entry -Toni 18.10
                # print("Results files: \n\n", fetch.listResultsDir()) # list files in results dir # DO NOT DELETE COMMENT
                infile = fetch.readResults("results/results2.json")
                input_file = ast.literal_eval(str(infile))
                file = open("results/results2.json", "r+")
                output_dict = fetch.build(input_file)
                output_json = json.dumps(output_dict)
                fetch.writeResults(file, output_json)
                print("Completed fetch")
            if mode == 'X' or 'x':
                print("Exiting program")
                quit()
            if mode not in mode_list:
                raise ItemNotInListError

        except ItemNotInListError:
            errorMsg()


if __name__ == "__main__":
    main()
