import matplotlib.pyplot as plt
import json
import os
from operator import itemgetter

with open("name_search_results_2021-12-13.txt") as json_file:
    results = json.load(json_file)

results = dict(sorted(results.items(), key=itemgetter(1), reverse=True)[:10])

fig, ax = plt.subplots()
ax.bar(list(results.keys()), results.values())

ax.set_ylabel("ylabel")
ax.set_title("title")

plt.savefig(os.path.join("histogram.png"))