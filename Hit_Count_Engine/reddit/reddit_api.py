# -*- coding: utf-8 -*-
import requests
import json
import ast
import subprocess
import os

import praw
from praw.models import MoreComments

reddit = praw.Reddit(client_id="9aC2iDzQQi04w-q1cPmjUw",
                                  client_secret="O29M5Puueuew1y_rDYVuvUZLdKuF_w",
                                  user_agent="NLP_Project_API/0.0.1",
                                )

def translateQuery(query):
        """Translate some character which are unreadable by reddit API"""
        tr = {"+":"plus", "#":"sharp", "-":"minus"}
        for k,v in tr:
            if k in query:
                query = query.replace(k,v)
        return query
    
class Fetch:
    
    def __init__(self, query, subReddit='all', timestamp='all'):
        """
        :param query: defined search term for tweets tagged with #query
        """
        self.query = translateQuery(query)
        self.subReddit = subReddit
        self.submissions = reddit.subreddit(subReddit).search(query, time_filter=timestamp)
        
        self.resultsDir = os.getcwd()
        
    def getResultsDir(self):
        directory = self.resultsDir + "/results"
        return directory
    
    def listResultsDir(self):
        """List contents of directory where .json files are located"""
        process = subprocess.Popen(['ls', self.getResultsDir()], stdout=subprocess.PIPE)
        return process.communicate()[0].decode('utf-8')

        
    def getPopularityScore(self, limit=10):
        """Calculate popularity score of the query"""
        totalScore=0
        
        i=0
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
                    
            if i>=10:
                break
            i+=1
                 
        print("Popularity of " + self.query + " : " + str(totalScore))
        return totalScore 
        #totalScore = 
        #    sub_upvotes*(title_query_occurence + sub_text_query_occurence) 
        #  + sum(comment(i)_score*(comment_query_occurence))
    
    
    
    def appendCount(self, input_dict):
        """
        Append the input dictionary of queries with results. Returned dictionary of query results is reverse
        sorted (high-to-low)
        Built in sorted() absolutely the fastest way https://medium.com/@tuvo1106/how-fast-can-you-sort-9f75d27cf9c1
        """
        output_dict = dict()
        query = str(self.query)
        value = str(self.getPopularityScore())
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
    
            
    
    
    

def main():
    print("Welcome.\n\n")
    #Main loop
    while(True):
        try:
            #Getting the query
            query = input("Enter a query, 'stop' if you want to stop : ")
            
            #Stop the loop
            if query=='stop':
                print('Loop terminated')
                break
            
            #Getting a timestamp
            #timestamp = 'all'
            timestamp = input("Please choos a timestamp : 'hour', 'day', 'week', 'month', 'year', 'all' ")
            
            #Looking for a subreddit
            subRBool = input("Do you want to look at a precise subreddit ? (y/n)")
            if subRBool=='y':
                subReddit = input("What subreddit do you want to browse : ")
                fetch = Fetch(query, subReddit, timestamp)
            elif subRBool=='n':
                fetch = Fetch(query)
                
            #Getting the query score
            #score1=fetch.getPopularityScore()
            #print("Total popularity score of " + str(query) + " : " + str(score1))
            
            iofile = fetch.readResults("results/results.json")
            input_file = ast.literal_eval(iofile)
            file = open("results/results.json", "r+")
            output_dict = fetch.appendCount(input_file)
            output_json = json.dumps("queries: " + str(output_dict))
            fetch.writeResults(file, output_json)
            print("Completed fetch, query added to the JSON results file")
                    
                    
        except UnboundLocalError:
            print("Wrong input, please retry")
        except KeyboardInterrupt:
            print("Program interrupted")
            break
            
    print('Goodbye !')

if __name__ == "__main__":
    main()