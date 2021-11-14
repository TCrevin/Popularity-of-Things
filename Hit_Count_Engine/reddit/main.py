import requests
import json
import ast
import subprocess
import time
import collections
from functools import reduce


from reddit_api import Fetch

# reddit_api globam variables
from reddit_api import globalTags

import matplotlib.pyplot as plt

def main():
    print("Welcome.\n\n")
    #Main loop
    while(True):
        try:
            #Getting the query
            query = input("Enter a query, 'stop' if you want to stop : ").lower()
            
            #Stop the loop
            if query=='stop':
                print('Loop terminated')
                break
            
            #Getting tags to check if the submission is corresponding to what we are looking for
            tagBool = input("Do you wish to add a specific tag ? (y/n): ")
            otherTagDict = {}
            otherTagDict.update(globalTags)
            while(tagBool == 'y'):
                otherTag = input("What tag do you wish to add : ")
                otherTagScore = int(input("Whith what score ? It can be negative if not wanted in the search: "))
                otherTagDict[otherTag]=otherTagScore
                
                tagBool = input("Do you wish to add a specific tag ? (y/n): ")

            #Getting a timestamp
            #timestamp = input("Please choos a timestamp : 'hour', 'day', 'week', 'month', 'year', 'all' ")
            
            #Looking for a subreddit
            subRBool = input("Do you want to look at a specific subreddit ? (y/n): ")
            if subRBool=='y':
                subReddit = input("What subreddit do you want to browse : ")
            elif subRBool=='n':
                subReddit = 'all'
                
            #Initializing the class
            fetch = Fetch(query, subReddit, timestamp="week", tags=otherTagDict)
                
            #Saving score in JSON file
            iofile = fetch.readResults("results/results.json")
            input_file = ast.literal_eval(iofile)
            file = open("results/results.json", "r+")
            output_dict = fetch.appendCount(input_file)
            print("THIS THE OUTPUT DICT")
            print(output_dict)
            output_json = json.dumps("queries: " + str(output_dict))
            fetch.writeResults(file, output_json)
            print("Completed fetch, query added to the JSON results file")
                    
            
        except UnboundLocalError:
            print("Wrong input, please retry")
        except KeyboardInterrupt:
            print("Program interrupted")
            break
            
    hist = input("Do you wish to see the results as an histogram ? (y/n): ")
    if hist=='y':
        plt.bar(list(output_dict.keys()), output_dict.values())
        plt.show()
    print('Goodbye !')

if __name__ == "__main__":
    main()

