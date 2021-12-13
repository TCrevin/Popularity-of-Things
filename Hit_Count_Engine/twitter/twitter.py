import requests
import json
import time

def twitter_process(a_list, qualifying):
	res_dict = {}
	null = ''
## GENERAL PROCESS #############################################################
	a = 1
	for original_query in a_list:
		a = a + 1
		print(a)
		if a>=10:
			print("The program is pausing to avoid twitter restrictions of 300 items/15min")
			print("Wait 15 minutes")
			time.sleep(5)
			a=1
	## CLEAN SPECIAL CHARACTERS  ##
		temp_query = ''.join(char for char in original_query if char.isalnum())
		if temp_query == (null) or temp_query == ' ':
			temp_query = '_'
		
	## PROCESS TO ADD RULES INTO QUERY##########################################	
		if len(qualifying) != 0:
			if len(qualifying) == 1:
				temp_query = temp_query + ' ' + qualifying[0]
			if len(qualifying) > 10:
				qualifying = qualifying[:9]
				print(qualifying)
			if len(qualifying) < 10:		
				temp_query = temp_query + ' (' + qualifying[0]
				for i in range(2,len(qualifying)):
					temp_query = temp_query + ' OR ' + qualifying[i]
				temp_query = temp_query + ')'
	
	## API CALLING #############################################################
		print(temp_query)
		fetch = Fetch(temp_query)
		new_count = fetch.getCount()
		res_dict.update({original_query: new_count})
	return res_dict
		
## MAIN #######################
	
def main():
	print("hello1")
#	twitter_process()
	
if __name__ == "__main__":
    main()
    
    
    
    
    
		
## API BODY  ###################################################################
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
            print(tweet['text'],"\n\n\n")

    def getCount(self):
        url = "https://api.twitter.com/2/tweets/counts/recent?query=%23{}".format(self.query)
        count_response = requests.request("GET", url, headers=self.headers, data=self.payload)
        count_response_text = json.loads(count_response.text)
        return	count_response_text['meta']['total_tweet_count']
        print("How many tweets with #{} as the query: {}\n\n\n".format(
            self.query,
            count_response_text['meta']['total_tweet_count'])) 
	