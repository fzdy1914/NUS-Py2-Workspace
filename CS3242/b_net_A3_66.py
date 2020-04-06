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
                    for variable in entry.keys():
                        if variable != 'probability' and entry[variable] != cmp_entry[variable]:
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

    def normalize(self):
        prob_sum = 0
        for entry in self.table:
            prob_sum += entry['probability']

        if prob_sum != 0:
            for entry in self.table:
                entry['probability'] /= prob_sum

    @classmethod
    def multiply(cls, factor1, factor2):
        new_factor = Factor()
        all_var = set(factor1.keys + factor2.keys)
        common_var = set(factor2.keys) - (all_var - set(factor1.keys))
        new_factor.keys = list(all_var)
        for entry1 in factor1.table:
            for entry2 in factor2.table:
                should_add = True
                for var in common_var:
                    if entry1[var] != entry2[var]:
                        should_add = False
                        break
                if should_add:
                    probability = entry1['probability'] * entry2['probability']
                    temp = dict()
                    temp.update(entry1)
                    temp.update(entry2)
                    temp['probability'] = probability
                    new_factor.table.append(temp)
        return new_factor


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
                new_dict = dict()
                new_dict[key] = value
                new_dict['probability'] = self.prior_probabilities[key][value]

                new_factor.table.append(new_dict)

            self.factors.append(new_factor)

    def infer(self):
        # TODO: Your code here to answer the queries given using the Bayesian
        # network built in the construct() method.
        self.answer = []  # your code to find the answer
        # for the given example:
        # self.answer = [{"index": 1, "answer": 0.01}, {"index": 2, "answer": 0.71}]
        # the format of the answer returned SHOULD be as shown above.

        for query in self.queries:
            index = query['index']
            given = query['given']
            to_find = query['tofind']
            hidden = self.all_variables[:]
            for key in to_find:
                hidden.remove(key)
            for key in given:
                hidden.remove(key)

            factors = copy.deepcopy(self.factors)

            # restrict the given variable
            for key, value in given.items():
                for factor in factors[:]:
                    if key in factor.keys:
                        factor.restrict(key, value)
                        if len(factor.keys) == 0:
                            factors.remove(factor)
            while len(hidden) > 0:
                # find the variable to eliminate
                next_var = hidden[0]
                min_degree = BayesianNetwork.degree(next_var, factors)
                for hidden_var in hidden:
                    new_degree = BayesianNetwork.degree(hidden_var, factors)
                    if new_degree < min_degree:
                        min_degree = new_degree
                        next_var = hidden_var
                hidden.remove(next_var)

                # find the related factors of next_var
                related_factor = []
                for factor in factors[:]:
                    if next_var in factor.keys:
                        related_factor.append(factor)
                        factors.remove(factor)

                if len(related_factor) > 0:
                    result_factor = related_factor[0]

                    for i in range(len(related_factor) - 1):
                        result_factor = Factor.multiply(result_factor, related_factor[i + 1])

                    result_factor.sum_out(next_var)
                    if len(result_factor.keys) > 0:
                        # append back if it is valid
                        factors.append(result_factor)

            final_result_factor = factors[0]
            for i in range(len(factors) - 1):
                final_result_factor = Factor.multiply(final_result_factor, factors[i + 1])

            final_result_factor.normalize()
            result = None

            for entry in final_result_factor.table:
                print entry

            for entry in final_result_factor.table:
                found = True
                for key, value in to_find.items():
                    if entry[key] != value:
                        found = False
                        break
                if found:
                    result = entry['probability']
                    break

            self.answer.append({'index': index, 'answer': result})

        return self.answer

    # You may add more classes/functions if you think is useful. However, ensure
    # all the classes/functions are in this file ONLY and used within the
    # BayesianNetwork class.

    @classmethod
    def degree(cls, variable, factor_list):
        dependent_variable = []
        for factor in factor_list:
            if variable in factor.keys:
                for key in factor.keys:
                    if key != variable and key not in dependent_variable:
                        dependent_variable.append(key)
        return len(dependent_variable)



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
    print(answers)


if __name__ == "__main__":
    main()
