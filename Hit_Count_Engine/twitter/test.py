import requests
import json

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
        self.headers = {  # TODO: Replace to load bearer token from file in Docker instance.
            'Authorization': 'Bearer AAAAAAAAAAAAAAAAAAAAAOt8UAEAAAAAEN0BvdqkKaVE9slkjxdut6MPSXk'
                             '%3DI4q1yypw35bZx0KGloF8vjwbTQLdew9DilAjVVKiO5QoRcCLhu '
        }

    def getTweets(self):
        print("'ello")
        url = "https://api.twitter.com/2/tweets/search/recent?query=%23{}&max_results=100".format(self.query)
        tweets_response = requests.request("GET", url, headers=self.headers, data=self.payload)
        tweets_response_text = json.loads(tweets_response.text)
        for tweet in tweets_response_text['data']:
            print(tweet['text'])  # TODO: Return as variable, append to file -Toni 6.10.2021

    def getCount(self):
        print("'ello2")
        url = "https://api.twitter.com/2/tweets/counts/recent?query=%23{}".format(self.query)
        count_response = requests.request("GET", url, headers=self.headers, data=self.payload)
        count_response_text = json.loads(count_response.text)
        print("How many tweets with #{} as the query: {}".format(
            self.query,
            count_response_text['meta']['total_tweet_count']))  # TODO: Append to file -Toni 6.10.2021


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
    print("Welcome.")
    while True:

        try:
            print("To exit the program, please press 'X' and 'Enter'.\n\n")
            query = input("Please input query: #")
            if query == 'X':
                print("Exiting program")
                quit()
            fetch = Fetch(query)
            mode = input("1 : Get tweets related to {0} from last 7 days\n"
                         "2 : Get the count of tweets related to {0}\n"
                         "[1/2?]: ".format(query))

            if mode == '1':
                fetch.getTweets()
            if mode == '2':
                fetch.getCount()
            if mode == 'X':
                print("Exiting program")
                quit()
            if mode not in mode_list:
                raise ItemNotInListError

        except ItemNotInListError:
            errorMsg()
        except ValueError:
            errorMsg()


if __name__ == "__main__":
    main()
