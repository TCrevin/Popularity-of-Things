import os
import json
from pathlib import Path

import threading

from reddit.reddit_api import reddit_process
from twitter.twitter import twitter_process
from google.gpytrends import google_process

from operator import itemgetter

import matplotlib.pyplot as plt
import pandas as pd

import datetime
import time

processes = [twitter_process, google_process, reddit_process]


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
        queries = data["queries"]
        qualifying_terms = data["qualifying_terms"]

    # queries = ['que1', 'que2']
    # qualifying_terms = ['qt1', 'qt2']
    return queries, qualifying_terms


def normalize(results):
    """
     Parameters
    ----------
    results: An API dictionary of query/hitcount dictionaries

    Normalize data for each API dictionnary so it is easier to read the final results
    -------
    """
    for d in results.values():
        factor = 100.0 / sum(d.values())
        for k in d:
            d[k] = d[k] * factor


def getMergedResults(results, queries):
    """
    Parameters
    ----------
    results: An API dictionary of query/hitcount dictionaries
    queries : list of the queries string

    Returns a merged dictionary of query/hitcount values
    -------
    resultDicts : dict
    """
    merged_results = {key: 0 for key in queries}
    for counts in results.values():
        for k, v in counts.items():
            merged_results[k] += v
    return merged_results


def processAPIprograms(queries, qualifying_terms, norm=True):
    """
    Parameters
    ----------
    queries : list of string
    qualifying_terms : list of string
    norm : True by default, if True, normalize query/hitcount dictionaries values

    Returns an API dictionary of query/hitcount dictionaries
    -------
    resultDicts : dict
    """
    resultDicts = {}

    for process in processes:
        name = "API name undefined"
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

        # API processing functions should have two list of strings (queries and qualifying_terms)
        print("-----Processing queries through " + name + " API is starting:-----\n")

        """th = threading.main_thread(target=process, args="qualifying_terms")
        th.start()
        resultDicts[name]=th"""
        if name == "google":
            # Category 314: Computer Science
            category = "314"
            resultDicts[name] = process(queries, category)
        else:
            resultDicts[name] = process(queries, qualifying_terms)
        print("-----Processing queries through " + name + " API has ended:-----\n")

    if norm:
        normalize(resultDicts)

    return resultDicts


def getDirectories(current_date):
    """
    Parameters
    ----------
    current_date : current date time in datetime.date format

    Returns directories needed to save the final results
    """
    Hit_Count_Engine = os.getcwd()
    in_out_results = Hit_Count_Engine + "\in_out_results"
    graphs = in_out_results + "\graphs"
    hists = graphs + "\hists"
    json_outputs = in_out_results + "\json_outputs"

    Path(hists + "\\" + str(current_date)).mkdir(parents=True, exist_ok=True)

    hists_date_dir = hists + "\\" + str(current_date)

    return Hit_Count_Engine, in_out_results, graphs, hists, json_outputs, hists_date_dir


def main():
    start_time = time.time()

    print("-----------This is the main script processing-----------")

    # --------------input extraction & conversion----------------
    input = JSONinputToPython("in_out_results/user_config.JSON")
    queries = input[0]
    qualifying_terms = input[1]
    print("User queries: ", queries)
    print("User qualifying terms: ", qualifying_terms)
    print("\n")

    # Current date
    current_date = datetime.date.today()

    # Directories
    Hit_Count_Engine, in_out_results, graphs, hists, json_outputs, hists_date_dir = getDirectories(current_date)
    # ----------------------python results---------------------
    # TODO change queries to real queries from JSON

    # Test input, to comment
    #queries = ["python", "java", "golang", "javascript"]
    #qualifying_terms = ["computer", "program", "code", "develop"]

    # Threading ?
    # results = threading.Thread(target=processAPIprograms, args=(queries, qualifying_terms, True))
    # results.start()
    # results.join()
    # print(results)

    # Normalized Results by API
    results = processAPIprograms(queries, qualifying_terms, norm=True)

    # Merged Normalized Results of every used API
    merged_results = getMergedResults(results, queries)

    # Top N results to display on histograms
    N = 10

    merged_top_results = dict(sorted(merged_results.items(), key=itemgetter(1), reverse=True)[:N])
    top_results = {api: {} for api in results.keys()}
    for api in results.keys():
        for key in merged_top_results.keys():
            top_results[api][key] = results[api][key]

    # print(merged_top_results)
    # print(top_results)

    print("The popularity results of " + str(current_date) + " are: ")
    print("For each API: " + str(results))
    print("Merged results: " + str(merged_results))

    # -------------------------HISTOGRAMS-----------------------

    # HISTOGRAMS for each API
    # browsing APIs (reddit, twitter, ...)
    for API,  API_res in results.items():
        API_res = dict(sorted(API_res.items(), key=itemgetter(1), reverse=True)[:N])
        # plotting a histogram (popularity in function of queries) for a particular API
        fig, ax = plt.subplots()

        ax.bar(list(API_res.keys()), API_res.values())

        ax.set_ylabel("Popularity Count of " + str(API))
        ax.set_title("Popularity Count by Query")

        plt.savefig(os.path.join(hists_date_dir + "\\" + API + ".png"))

    # merged API HISTOGRAMS
    # plotting a histogram (popularity in function of queries) for a particular API
    fig, ax = plt.subplots()

    ax.bar(list(merged_top_results.keys()), merged_top_results.values())

    ax.set_ylabel("Merged Popularity Count of every APIs")
    ax.set_title("Popularity Count by Query")

    plt.savefig(os.path.join(hists_date_dir + "\\merged_all.png"))

    # grouped HISTOGRAM (popularity in function of queries) for every used API
    fig = pd.DataFrame(top_results).plot(kind="bar", title="Results", legend=True)
    plt.ylabel("Popularity Count")
    plt.title("Popularity Count by Query, grouped by used API")
    plt.savefig(os.path.join(hists_date_dir + "\\grouped_all.png"))

    # -------------------Converting dict to JSON-----------------
    json_object = json.dumps(results, indent=4)
    # Saving the JSON file
    with open(json_outputs + "\\" + str(current_date) + ".json", "w") as f:
        f.write(json_object)

    # Execution time measurment
    end_time = time.time()
    print("Duration: {}".format(end_time - start_time))


if __name__ == "__main__":
    main()