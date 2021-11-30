main.py file's goal is to use a user JSON input file of queries and qualifying terms to measure the popularity of these queries.

It returns and save different histograms (in_out_results/graph) and an output JSON file showing normalized values in function of the queries and the used API's

The JSON input file should be modified following the current format: a list of queries and a list of qualifying terms.

If the user doesn't want normalized data, he can change the 'norm' parameter in the function call to False (line 163).