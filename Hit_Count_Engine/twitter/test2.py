import requests
import json
import ast
import subprocess

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

    def appendCount(self, input_dict):
        """
        Append the input dictionary of queries with results. Returned dictionary of query results is reverse
        sorted (high-to-low)
        Built in sorted() absolutely the fastest way https://medium.com/@tuvo1106/how-fast-can-you-sort-9f75d27cf9c1
        """
        output_dict = dict()
        query = str(self.getCount()[0])
        value = str(self.getCount()[1])
        input_dict.update({query: value})
        sort_dict = sorted(input_dict.items(), key=lambda x: int(x[1]), reverse=True)
        for v, k in sort_dict:
            output_dict[v] = k
        return output_dict

    def readResults(self, filename):
        """Open and read file. File must be closed separately if writeResults() is not called"""
        try:
            file = open(filename)
            data = json.load(file)
            ding = data.replace("queries: ", '')
            return ding
        except FileNotFoundError:
            self.readResults(filename)

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
                iofile = fetch.readResults("results/results.json")
                input_file = ast.literal_eval(iofile)
                file = open("results/results.json", "r+")
                output_dict = fetch.appendCount(input_file)
                output_json = json.dumps("queries: " + str(output_dict))
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
