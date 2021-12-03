import requests
import time
import json


class Fetch:
    def __init__(self, query):
        """
        :param query: defined search term for tweets tagged with #query
        """
        self.query = query
        self.bearer_token = "F8vjwbTQLdew9DilAjVVKiO5QoRcCLhu"
        self.payload = {}
        self.headers = {
            'Authorization': 'Bearer AAAAAAAAAAAAAAAAAAAAAOt8UAEAAAAAEN0BvdqkKaVE9slkjxdut6MPSXk'
                             '%3DI4q1yypw35bZx0KGloF8vjwbTQLdew9DilAjVVKiO5QoRcCLhu '
        }

    def getTweets(self):
        url = "https://api.twitter.com/2/tweets/search/recent?query=%23{}&max_results=100".format(self.query)
        tweets_response = requests.request("GET", url, headers=self.headers, data=self.payload)
        tweets_response_text = json.loads(tweets_response.text)
        for tweet in tweets_response_text['data']:
            print(tweet['text'], "\n\n\n")

    def getCount(self):
        url = "https://api.twitter.com/2/tweets/counts/recent?query=%23{}".format(self.query)
        count_response = requests.request("GET", url, headers=self.headers, data=self.payload)
        count_response_text = json.loads(count_response.text)
        return count_response_text['meta']['total_tweet_count']
        #print("How many tweets with #{} as the query: {}\n\n\n".format(self.query, count_response_text['meta']['total_tweet_count']))


def twitter_process(a_list, eliminating):
    res_dict = {}
    i = 1
    for query in a_list:
        if i%275==0:
            print("The program is pausing to avoid twitter restrictions of 300 items/15min")
            time.sleep(15*60)
        print(query)
        fetch = Fetch(query)
        new_count = fetch.getCount()
        res_dict.update({query: new_count})
        print("Popularity of " + query + " : " + str(new_count) +"\n")
        i+=1
    return res_dict


def main():
    print("hello1")
    twitter_process()


if __name__ == "__main__":
    main()
