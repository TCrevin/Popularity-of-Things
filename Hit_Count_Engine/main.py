import os
import json
from pathlib import Path

from reddit.reddit_api import reddit_process

import matplotlib.pyplot as plt
import pandas as pd

import datetime

processes = [reddit_process]



def JSONinputToPython(filename):
    """
    Parameters
    ----------
    filename : string
        A file to convert to python.

    Returns two python lists
     - queries
     - qualifying terms
    -------
    queries : list of string
    qualifying_terms : list of string
    """
    # Opening JSON file
    with open(filename) as json_file:
        data = json.load(json_file)
        queries = data['queries']
        qualifying_terms = data['qualifying_terms']

    # queries = ['que1', 'que2']
    # qualifying_terms = ['qt1', 'qt2']
    return queries, qualifying_terms

def processAPIprograms(queries, qualifying_terms):
    """
        Parameters
        ----------
        param1 : string
            A file to convert to python.

        Returns two python lists
         - queries
         - qualifying terms
        -------
        queries : list of string
        qualifying_terms : list of string
        """
    resultDicts = {}

    for process in  processes:
        name="API name undefined"
        if "reddit" in str(process):
            name = "reddit"
        if "twitter" in str(process):
            name = "twitter"
        if "google" in str(process):
            name = "google"
        if "facebook" in str(process):
            name = "facebook"
        if "instagram" in str(process):
            name = "instagram"

        resultDicts[name]=(process(queries, qualifying_terms))

    return resultDicts



def main():

    print("-----------This is the main script processing-----------")

    # --------------input extraction & conversion----------------
    input = JSONinputToPython('in_out_results/user_config.JSON')
    queries = input[0]
    qualifying_terms = input[1]
    print('User queries: ', queries)
    print('User qualifying terms: ', qualifying_terms)
    print('\n')



    # current date
    current_date = datetime.date.today()

    # directories
    Hit_Count_Engine = os.getcwd()
    in_out_results = Hit_Count_Engine + "\in_out_results"
    graphs = in_out_results + "\graphs"
    hists = graphs + "\hists"
    json_outputs = in_out_results + "\json_outputs"

    Path(hists + '\\' + str(current_date)).mkdir(parents=True, exist_ok=True)

    hists_date_dir = hists + '\\' + str(current_date)



    # ----------------------python results---------------------
    #TODO results = processAPIprograms(queries, qualifying_terms)
    results = {'reddit': {'java': 1, 'python': 5}, 'twitter': {'java': 2, 'python': 3}}
    print("The popularity results of" + str(current_date) + " are: ")
    print(results)
    print("\n")

    #-------------------------histograms----------------------
    # browsing APIs (reddit, twitter, ...)
    for API, API_res in results.items():
        # plotting a histogram (popularity in function of queries) for a particular API
        fig, ax = plt.subplots()

        ax.bar(list(API_res.keys()), API_res.values())

        ax.set_ylabel('Popularity Count')
        ax.set_title('Popularity Count by Query')

        plt.savefig(os.path.join(hists_date_dir + '\\' + API + '.png'))


    # plotting a grouped histogram (popularity in function of queries) for every used API
    fig = pd.DataFrame(results).plot(kind='bar'
                                    , title="Results"
                                    , legend=True)
    plt.ylabel('Popularity Count')
    plt.title('Popularity Count by Query, grouped by used API')
    plt.savefig(os.path.join(hists_date_dir + '\\all.png'))


    # Converting dict to JSON
    json_object = json.dumps(results, indent = 4)
    #Saving the JSON file
    with open(json_outputs + '\\'  + str(current_date) + '.json', 'w') as f:
        f.write(json_object)

if __name__ == "__main__":
    main()