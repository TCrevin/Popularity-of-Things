import json

def JSONinputToPython(filename):
    # Opening JSON file
    with open(filename) as json_file:
        data = json.load(json_file)
        tools = data['tools']

    name = []
    for tool in tools:
        name.append(tool['tool']['nick'])

    return name


names = JSONinputToPython('tools.json')
print(names)


json_names = {}
json_names['queries']=names

json_object = json.dumps(json_names, indent = 4)
with open('simplified_nickname.json', 'w') as f:
    f.write(json_object)
