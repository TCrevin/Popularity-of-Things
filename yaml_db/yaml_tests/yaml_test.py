import yaml

bird_counter=1

with open ("test.yaml", "r") as stream:
    try:
        inputYaml = yaml.load(stream)
        for key, item in inputYaml.items():
            if (key == "calling-birds"):
                for bird in item:
                    print("Bird{}: {}".format(bird_counter, bird))
                    bird_counter+=1

    except:
        print("Oopsie.")
