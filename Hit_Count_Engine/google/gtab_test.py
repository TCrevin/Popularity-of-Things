import gtab
import time
import json

# import matplotlib.pyplot as plt
"""
Google Trends does filter out some types of searches, such as:
- Searches made by very few people: Trends only shows data for popular terms, so search terms with low volume appear as "0"
- Duplicate searches: Trends eliminates repeated searches from the same person over a short period of time.
- Special characters: Trends filters out queries with apostrophes and other special characters.
"""


"""
Programming: 31
    C & C++: 731
    Developer Jobs: 802
    Development Tools: 730
    Java: 732
    Scripting Languages: 733
    Windows & .NET: 734
"""
# languages = ["Python", "Java", "C++", "golang", "javascript", "C#", "C", "Rust", "PHP", "FORTRAN"]
languages = ["C", "C++", "Cpp", "C#"]
suffix = " programming language"
results = {"queries": {}}
my_path = "gtab"

t = gtab.GTAB(dir_path=my_path)
t.set_options(
    # pytrends_config={"geo": "", "timeframe": "now 7-d"},
    pytrends_config={"cat": "31", "geo": "", "timeframe": "now 7-d"},
    gtab_config={"anchor_candidates_file": "550_cities_and_countries.txt", "num_anchors": 100},
)
# t.set_options(pytrends_config={"geo": "", "timeframe": "now 7-d"})
# t.create_anchorbank()
t.set_active_gtab("google_anchorbank_geo=_timeframe=now 7-d_cat=31.tsv")
# plt.figure(figsize=(12, 8))
# queries = dict()
# averages = list()
for language in languages:
    query = {
        "count": str(round(t.new_query(language + " language").max_ratio.mean())),
        "timestamp": str(time.time()),
    }
    results["queries"][language.lower()] = query
    # averages.append(queries[language].max_ratio.mean())
    # plt.plot(queries[language].max_ratio, label=language)

print(results)

# print(queries.items())
# plt.bar(languages, averages)
# for language, values in queries.items():
# print(language, values.max_ratio.mean())
# qmean = values.max_ratio.mean()
# print(f"{language}: {qmean.max_ratio}\n")
# plt.bar()
# plt.legend(loc="upper left")
# plt.show()

# plt.plot(query_mac.max_ratio, label="Mac")
# plt.plot(query_linux.max_ratio, label="Linux")
# plt.plot(query_windows.max_ratio, label="Windows")
# plt.legend(loc="upper left")
# plt.show()
