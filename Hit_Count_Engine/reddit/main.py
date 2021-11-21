import numpy as np

from reddit_api import *

# reddit_api globam variables
from reddit_api import globalTags


print('Processing queries through Reddit')

timest = "month"
subreddit = "all"
sort = "relevance"

localTags = {}
localTags.update(globalTags)

queries = ["java"]

i=0
for query in queries:
    print("Process")
    """if query=="c":
        ctags = {"c++":-2}
        localTags.update(ctags)"""

    fetch = Fetch(query, subReddit=subreddit, timestamp=timest, tags=localTags, sortP=sort)

    # Saving score in JSON file
    iofile = fetch.readResults("results/results.json")
    input_file = ast.literal_eval(iofile)
    file = open("results/results.json", "r+")
    output_dict = fetch.appendCount(input_file)

    dict_val = []
    for value in output_dict.values():
        dict_val.append(int(value))
    dict_quantile = np.quantile(dict_val, 0.95)


    print("THIS THE 3 QUARTILE " + str(dict_quantile))
    if int(output_dict[query]) < dict_quantile:
        print("THIS THE OUTPUT DICT")
        print(output_dict)
        output_json = json.dumps("queries: " + str(output_dict))
        fetch.writeResults(file, output_json)
        print("Completed fetch, query added to the JSON results file")

    i+=1
    if(i >=3):
        break


