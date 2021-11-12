# -*- coding: utf-8 -*-
import requests
import json
import ast
import subprocess
import os

import pandas as pd
import matplotlib.pyplot as plt

import praw
from praw.models import MoreComments


subreddits = ["programming", "ProgrammerHumor", ]
times = ["all", "year", "month", "week", "day", "hour"]
sorts = ["relevance", "hot", "top", "new", "comments"]

languages = ["c", "c++", "c#", "java", "javascript", "php", "python", "golang", "fortran"]

reddit = praw.Reddit(client_id="9aC2iDzQQi04w-q1cPmjUw",
                                  client_secret="O29M5Puueuew1y_rDYVuvUZLdKuF_w",
                                  user_agent="NLP_Project_API/0.0.1",
                                  check_for_async=False
                                )

globalTags = {"program":3, "code":3, "comput":3, "develop":3, "dev":3, 
            "tech":2, "software":2, "language":2, "framework":2, "engineer":2,
            #"python":2, "java":2, "c++":2, "cplusplus":2, "c#":2, "csharp":2, "php":2, "fortran":2, "javascript":2, "golang":2,
            "gam":1, "web":1, "work":1, 
            "meme":-2, 
            "d.c":-3, "b.c":-3, "dank":-3, "celsius":-3, "fahrenheit":-3, "°":-3,
            "nfl":-4, "basket":-4, "ball":-4, "football":-4, "tv":-4,
            "usb":-5}

def translateQuery(query):
    """

    Parameters
    ----------
    query : string
        A string query to translate.

    Returns a translated query if the base query has unwanted characters
    -------
    query : string
        A translated query.

    """
    """Translate some character which are unreadable by reddit API"""
    tr = {'+':"p", '#':"sharp"}
    for key in tr:
        if key in query:
            query = query.replace(key,tr[key])
    return query
    
    
def hasTag(subObject, tagDict=globalTags):
    """

    Parameters
    ----------
    subObject : string
        A string got from submission (sub title, selftext, comments).
    tagDict : dict, optional
        A dictionary of tags to check if the submission is corresponding to what we are looking for. 
        Examples: {"robot":3, "animal":-3}, the user whish to look for a query related to robot but not to animal
        The default is globalTags.

    Returns a integer representation of the relativness of a submission object (title, selftext, comment).
    -------
    tagScore : int
        A integer representation of the relativness of a submission object (title, selftext, comment).

    """
    
    tagScore=0
    if subObject is not None:
        for key in tagDict:
            if key.lower() in subObject.lower():
                tagScore+=tagDict[key]
    return tagScore
    

class Fetch:
    
    def __init__(self, query, subReddit='all', timestamp='week', tags=globalTags, sortP="relevance"):
        """

        Parameters
        ----------
        query : string
            A search query.
        subReddit : string, optional
            A subreddit to look the query in. The default is 'all'.
        timestamp : string, optional
            A timestamp to look the query results occured during this timestamp. The default is 'week'.
        tags : dict, optional
            A dictionary of tags to check if the submission is corresponding to what we are looking for. The default is globalTags.

        Returns an instance of a fetch class
        -------
        None.

        """
        
        self.query = query
        self.translatedQuery = translateQuery(query)
        self.subReddit = subReddit
        self.submissions = reddit.subreddit(subReddit).search(query, time_filter=timestamp, sort=sortP)
        self.tags=tags
        
        self.resultsDir = os.getcwd()
        
    def getResultsDir(self):
        directory = self.resultsDir + "/results"
        return directory
    
    def listResultsDir(self):
        """List contents of directory where .json files are located"""
        process = subprocess.Popen(['ls', self.getResultsDir()], stdout=subprocess.PIPE)
        return process.communicate()[0].decode('utf-8')

        
    def getPopularityScore(self, limit=10):
        """

        Parameters
        ----------
        limit : int, optional
            A limit of how much submissions we want to process. The default is 10.

        Returns a popularity score based on submission's and its comment's upvotes and query occcurences
        -------
        totalScore : int
            A popularity socre of a query.

        """
        totalScore=0
        titles = {}
        titlesScore = {}
        
        i=0
        for submission in self.submissions:
            ts = totalScore
            
            #if a minmimum amount of tag in sub title or text
            #print(self.tags())
            if (hasTag(submission.title.lower(), self.tags)>=3
                or hasTag(submission.selftext.lower(), self.tags) >=3 
                #or hasTag(submission.subreddit.display_name)>=4
                #or hasTag(submission.subreddit.description)>=4:
                ):
                    
                #submission upvotes count
                subPopularity = submission.score
                
                #submission comments count
                subComCount = len(submission.comments)
                
                #query counting in TITLE
                subTitleCount=0
                if self.query in submission.title.lower():
                    subTitleCount = submission.title.lower().count(self.query)
                elif self.translatedQuery in submission.title.lower():
                    subTitleCount = submission.title.lower().count(self.translatedQuery)
                
                #query counting in SUB TEXT
                subTextCount=0
                if self.query in submission.selftext.lower():
                    subTextCount = submission.selftext.lower().count(self.query)
                elif self.translatedQuery in submission.selftext.lower():
                    subTextCount = submission.selftext.lower().count(self.translatedQuery)
                
                totalScore += (subTitleCount+subTextCount)*subPopularity#*subComCount
                
                #query counting in SUB COMMENTS
                for comment in submission.comments:
                    if not(isinstance(comment, MoreComments)):
                        if self.query in comment.body.lower():
                            totalScore += comment.body.lower().count(self.query)#*comment.score
                        elif self.translatedQuery in comment.body.lower():
                            totalScore += comment.body.lower().count(self.translatedQuery)#*comment.score
                        
                #to know the max value of hasTag fct between sub title and selftext
                titles[submission.title]=max(hasTag(submission.title, self.tags),hasTag(submission.selftext, self.tags))
                
                #score of the submission
                titlesScore[submission.title] = totalScore-ts
                
                print("Searching for corresponding posts, please wait...")
                
                #limit of i submissions
                if i>=10:
                    break
                i+=1
                 
        print("\nPopularity of " + self.query + " : " + str(totalScore))
        print(titles)
        print("\n")
        print(titlesScore)
        return totalScore
    
    
    
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
        sort_dict = sorted(input_dict.items(), key=lambda x: int(x[1]), reverse=False)
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