import yaml
import time

query = input("Insert query: ")
print("Query: ", query.lower())
with open ("yaml_sample.yaml", "r+") as stream:
        items = []
        inputYaml = yaml.load(stream, Loader=yaml.FullLoader)
        print("DEBUG inputYaml(): ", type(inputYaml))
        for x, item in enumerate(inputYaml.get('queries')): # check for duplicates
            print(inputYaml.get('queries').get(item))
            item_container = inputYaml.get('queries').get(item)
            lower_iterator = (map(lambda x: x.lower(), item_container)) # iterate through items, return new list where items are lowercase
            lower_container = list(lower_iterator) # construct list
            if query in lower_container: # check if search query in list
                #print("Found")
                items.append(item) # add category to list
            else:
                pass


        if len(items) == 0:
            print("No such item in list.")
            exit()
        print("Please define category from the following: ")
        for item in items: print(query, ": ",item) # list of categories where query was found in

        while True:
            category = input("Category : ")
            if category in items:
                print("Chosen category: ", category)
                print(inputYaml.get('queries').get(category)) # return this to use as list of inputs for API to loop through
                break
            else:
                print("Error. Please check input")

