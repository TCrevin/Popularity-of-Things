import numpy as np
import statistics

from reddit_api import *

#queries = ["python", "javascript", "java", "c", "c++", "cpp", "cplusplus", "c#", "csharp", "php", "fortran", "golang"]
queries = ["c"]

from reddit_api import Fetch

# reddit_api globam variables
from reddit_api import globalTags

import matplotlib.pyplot as plt

timest = "month"
subreddit = "all"
sort = "relevance"

localTags = {}
localTags.update(globalTags)

for query in queries:
    print("Proce")
    if query=="c":
        ctags = {"c++":-2}
        localTags.update(ctags)

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

plt.bar(list(output_dict.keys()), output_dict.values())
plt.show()