# -*- coding: utf-8 -*-

import praw
from praw.models import MoreComments

reddit = praw.Reddit(client_id="9aC2iDzQQi04w-q1cPmjUw",
                                  client_secret="O29M5Puueuew1y_rDYVuvUZLdKuF_w",
                                  user_agent="NLP_Project_API/0.0.1",
                                )
class Fetch:
    def __init__(self, query, subReddit='all'):
        """
        :param query: defined search term for tweets tagged with #query
        """
        self.query = query
        self.submissions = reddit.subreddit(subReddit).search(query)
            
    def getCount(self, subReddit='all'):
        cptTotal=0
        cptSub=0
        
        for submission in self.submissions:
            #query counting in TITLE
            cptTotal +=  submission.title.count(self.query)
            #query counting in SUB TEXT
            cptTotal += submission.selftext.count(self.query)
            #query counting in SUB COMMENTS
            for comment in submission.comments:
                cptTotal += comment.body.count(self.query)
            
            if self.query in submission.title:
                cptSub+=1
            
            
        print("How many submissions in the subreddit {} with #{} as the query: {}\n\n\n".format(
            subReddit,
            self.query,
            cptSub))

        print("How times the query #{} has been find in total: {}\n\n\n".format(
            self.query,
            cptTotal))

def main():
    print("Welcome.\n\n")
    while(True):
        query = input("Enter a query, 'stop' if you want to stop : ")
        if query=='stop':
            break
        
        subReddit = input("What subreddit do you want to browse (type nothing for browsing every subreddit): ")
        fetch = Fetch(query)
        print(fetch.getCount(subReddit))


if __name__ == "__main__":
    main()