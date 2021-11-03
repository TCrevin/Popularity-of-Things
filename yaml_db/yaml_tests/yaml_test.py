import yaml
import time


bird_counter=1

query = input("Insert query: ")

with open ("yaml_sample.yaml", "r+") as stream:
    #try:
        inputYaml = yaml.load(stream, Loader=yaml.FullLoader)
        #for key, item in inputYaml.items():
        #    if (key == "programming_languages"):
        #        for language in item:
        #            print("Bird{}: {}".format(key, item))
        #            bird_counter+=1
        queries = inputYaml.get('queries')[0].get(query)
        p1 = time.time()
        for count, item in enumerate(queries):
            print(count, ": ", item)
        p2 = time.time()-p1
        print("Time it took to loop through input: ", p2)
        #print(dict(queries[0]).get('programming_languages'))

            #print(inputYaml['queries']['programming_languages'][entry])

    #except:
    #    print("Oopsie.")
