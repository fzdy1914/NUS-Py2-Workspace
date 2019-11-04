import copy
import sys
import json


class Factor:
    def __init__(self):
        self.keys = []
        self.table = []

    def restrict(self, key, value):
        if key in self.keys:
            new_table = []

            for entry in self.table:
                if entry[key] == value:
                    del entry[key]
                    new_table.append(entry)

            self.keys.remove(key)
            self.table = new_table
        else:
            print('Can not restric the variable ' + key)

    def sum_out(self, key):
        if key in self.keys:
            new_table = []

            for entry in self.table:
                found = False
                found_entry = None
                del entry[key]
                for cmp_entry in new_table:
                    inside_found = True
                    for varaible in entry.keys():
                        if varaible != 'probability' and entry[varaible] != cmp_entry[varaible]:
                            inside_found = False
                            break
                    if inside_found:
                        found = True
                        found_entry = cmp_entry
                        break

                if found:
                    found_entry['probability'] = found_entry['probability'] + entry['probability']
                else:
                    new_table.append(entry)

            self.keys.remove(key)
            self.table = new_table
        else:
            print('Can not sum out the variable ' + key)


class BayesianNetwork(object):
    def __init__(self, structure, values, queries):
        # you may add more attributes if you need
        self.variables = structure["variables"]
        self.dependencies = structure["dependencies"]
        self.conditional_probabilities = values["conditional_probabilities"]
        self.prior_probabilities = values["prior_probabilities"]
        self.queries = queries
        self.answer = []

        self.all_variables = []
        self.factors = []

    def construct(self):
        for key in self.variables:
            self.all_variables.append(key)

        for key, value in self.variables.items():
            continue

        for key in self.conditional_probabilities:
            new_factor = Factor()
            for element in self.conditional_probabilities[key]:
                # probability = element['probability']
                element[key] = element['own_value']
                del element['own_value']
                new_factor.table.append(element)

            for inner_key in self.conditional_probabilities[key][0]:
                if inner_key != 'probability':
                    new_factor.keys.append(inner_key)

            self.factors.append(new_factor)

        for key in self.prior_probabilities:
            new_factor = Factor()
            new_factor.keys.append(key)
            for value in self.prior_probabilities[key]:
                # probability = element['probability']
                new_dict = {}
                new_dict[key] = value
                new_dict['probability'] = self.prior_probabilities[key][value]

                new_factor.table.append(new_dict)

            self.factors.append(new_factor)

        # for factor in self.factors:
        factor = self.factors[0]
        print(factor.table)
        factor.sum_out('Alarm')
        print(factor.table)
        print(factor.keys)

    def infer(self):
        # TODO: Your code here to answer the queries given using the Bayesian
        # network built in the construct() method.
        self.answer = []  # your code to find the answer
        # for the given example:
        # self.answer = [{"index": 1, "answer": 0.01}, {"index": 2, "answer": 0.71}]
        # the format of the answer returned SHOULD be as shown above.


        # print (self.conditional_probabilities)
        # print (self.prior_probabilities)

        return self.answer

    # You may add more classes/functions if you think is useful. However, ensure
    # all the classes/functions are in this file ONLY and used within the
    # BayesianNetwork class.


def main():
    # STRICTLY do NOT modify the code in the main function here
    if len(sys.argv) != 4:
        print ("\nUsage: python b_net_A3_xx.py structure.json values.json queries.json \n")
        raise ValueError("Wrong number of arguments!")

    structure_filename = sys.argv[1]
    values_filename = sys.argv[2]
    queries_filename = sys.argv[3]

    try:
        with open(structure_filename, 'r') as f:
            structure = json.load(f)
        with open(values_filename, 'r') as f:
            values = json.load(f)
        with open(queries_filename, 'r') as f:
            queries = json.load(f)

    except IOError:
        raise IOError("Input file not found or not a json file")

    # testing if the code works
    b_network = BayesianNetwork(structure, values, queries)
    b_network.construct()
    answers = b_network.infer()


if __name__ == "__main__":
    main()
