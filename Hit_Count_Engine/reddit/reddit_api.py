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
        self.subReddit = subReddit
        self.submissions = reddit.subreddit(subReddit).search(query)
            
    def getCount(self):
        cptTotal=0
        cptSub=0
        
        for submission in self.submissions:
            #query counting in TITLE
            cptTotal +=  submission.title.count(self.query)
            #query counting in SUB TEXT
            cptTotal += submission.selftext.count(self.query)
            #query counting in SUB COMMENTS
            for comment in submission.comments:
                if not(isinstance(comment, MoreComments)):
                    cptTotal += comment.body.count(self.query)
            
            if self.query in submission.title:
                cptSub+=1
            
            
        print("How many submissions in the subreddit {} with #{} as the query: {}\n\n\n".format(
            self.subReddit,
            self.query,
            cptSub))

        print("How times the query #{} has been find in total: {}\n\n\n".format(
            self.query,
            cptTotal))
        
    def getPopularityScore(self):
        totalScore=0
        
        for submission in self.submissions:
            #query upvotes count
            subPopularity = submission.score
            
            #query counting in TITLE
            subTitleCount = submission.title.count(self.query)
            
            #query counting in SUB TEXT
            subTextCount = submission.selftext.count(self.query)
            
            totalScore += (subTitleCount+subTextCount)*subPopularity
            
            #query counting in SUB COMMENTS
            for comment in submission.comments:
                if not(isinstance(comment, MoreComments)):
                    totalScore += comment.body.count(self.query)*comment.score
                    
        return totalScore
    
def comparePopularity(query1, query2, subreddit="all"):
    fetch1 = Fetch(query1, subreddit)
    fetch2 = Fetch(query2, subreddit)
    
    score1 = fetch1.getPopularityScore()
    score2 = fetch2.getPopularityScore()
    
    return score1 - score2

def main():
    print("Welcome.\n\n")
    while(True):
        query = input("Enter a query, 'stop' if you want to stop : ")
        if query=='stop':
            break
        
        subRBool = input("Do you want to look at a precise subreddit ? (y/n)")
        if subRBool=='y':
            subReddit = input("What subreddit do you want to browse : ")
            fetch = Fetch(query, subReddit)
        else:
            fetch = Fetch(query)
            
        score1=fetch.getPopularityScore()
        print("Total popularity score of " + str(query) + " : " + str(score1))
        
        comparBool = input("Do you want to compare the query " + str(query) + " to another one ? (y/n)")
        if comparBool=='y':
            query2 = input("What query ? ")
            fetch2 = Fetch(query2)
            score2 = fetch2.getPopularityScore()
            compare = score1 - score2
            if compare > 0:
                print(str(query) + " is more popular " + str(query2) + " by " + str(compare))
            elif compare < 0:
                 print(str(query2) + " is more popular " + str(query) + " by " + str(abs(compare)))
            else:
                print(str(query2) + " and " + str(query) + " are equally popular")


if __name__ == "__main__":
    main()