import json

def JSONinputToPython(filename):
    # Opening JSON file
    with open(filename) as json_file:
        data = json.load(json_file)
        tools = data['tools']

    name = []
    for tool in tools:
        try:
            for site in tool['tool']['urls']:
                name.append(site)
        except KeyError:
            print("No key 'URLS'")

    return name


names = JSONinputToPython('tools.json')
print(names)


json_names = {}
json_names['queries']=names

json_object = json.dumps(json_names, indent = 4)
with open('simplified_websites.json', 'w') as f:
    f.write(json_object)