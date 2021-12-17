from tools import (get_csv_line_input_as_list, get_line_input_as_list) 
from collections import Counter
import time
"""
Thought process:
- First did simple iterative approach part1 and the perform_replacements
  method. Not super efficient.
- For part2, tried to make it more efficient by recursively splitting 
  the problem and caching solutions (recursive_modify method). Cached solutions
  saved some time, but not quite enough to make it fast enough.
- While on a plane, thought through a more breadth first approach
  involving building a graph where each node represents a letter pair 
  with children (the two resulting pairs) as pointers to other node pairs. 
  It would involve first going through the translation rules and building 
  the graph of all possible pairs that will be used, then the method would
  just run through the graph and add the results
- At some point, I realized that I was building the whole strings which are
  going to be huuuuuuge, but I don't need to. I just needed to keep track of
  the counts of letters, so before building the graph structure, I thought
  to modify the recursive one to just hold Counters instead. It turns out, 
  with little surprise, that adding integers in a Counter is muuuuuuch more
  time efficient than building super long strings.
"""

class Polymer():
    def __init__(self, input_list):
        self.insertion_rules = {}
        self.solutions = {}
        self.template = []
        for i, line in enumerate(input_list):
            if i == 0:
                self.template = [x for x in line]
            elif line != "":
                split_line = line.split(" -> ")
                self.insertion_rules[split_line[0]] = split_line[1]

    def __str__(self):
        return "\n".join([f"{x}: {self.insertion_rules[x]}" for x in self.insertion_rules]) + "\n" + "".join(self.template)

    def perform_replacements(self):
        """Move a two pointer window across template and iteratively generate list of insertions"""
        window_start = 0
        new_template = [self.template[window_start]]
        for window_end in range(1, len(self.template)):
            first_letter = self.template[window_start]
            second_letter = self.template[window_end]
            item_to_insert = self.insertion_rules.get(first_letter + second_letter, "")
            new_template.append(item_to_insert)
            new_template.append(second_letter)
            window_start += 1
        self.template = "".join(new_template)

    def recursive_modify(self, pair, number_of_steps):
        """Recursively depth first search problem space, building a string with returns

        :param pair: a string of a pair of characters like "ab" or "nn"
        :param number_of_steps: an int representing the number of recursions left to go
        :return: a string of characters that eventually becomes the full end result string
        """

        if pair not in self.insertion_rules:
            return pair
        elif str(number_of_steps) + pair in self.solutions:
            return self.solutions[str(number_of_steps) + pair]
        elif number_of_steps <= 0:
            return pair
        else:
            result = self.recursive_modify(pair[0] + self.insertion_rules[pair], number_of_steps-1)[:-1] + \
                   self.recursive_modify(self.insertion_rules[pair] + pair[1], number_of_steps-1)
            self.solutions[str(number_of_steps) + pair] = result
            return result

    def recursive_counter_modify(self, pair, number_of_steps):
        """Recursively depth first search problem space, building a Counter with returns

        :param pair: a string of a pair of characters like "ab" or "nn"
        :param number_of_steps: an int representing the number of recursions left to go
        :return: a Counter of the numbers of letters in the string
        """
        if pair not in self.insertion_rules:
            return Counter(pair)
        elif str(number_of_steps) + pair in self.solutions:
            return self.solutions[str(number_of_steps) + pair]
        elif number_of_steps <= 0:
            return Counter(pair)
        else:
            result = self.recursive_counter_modify(pair[0] + self.insertion_rules[pair], number_of_steps-1) + \
                     self.recursive_counter_modify(self.insertion_rules[pair] + pair[1], number_of_steps-1)
            result.subtract(self.insertion_rules[pair])
            self.solutions[str(number_of_steps) + pair] = result
            return result


def part1(input_list, number_of_steps):
    p = Polymer(input_list)
    for i in range(number_of_steps):
        p.perform_replacements()

    counts = Counter(p.template)
    min_count = min(counts.values())
    max_count = max(counts.values())

    return max_count - min_count


def part2(input_list, number_of_steps):
    """Recursively split and build strings with caching"""
    p = Polymer(input_list)
    output = Counter()
    for i in range(1, len(p.template)):
        pair = "".join(p.template[i-1] + p.template[i])
        pair_results = p.recursive_counter_modify(pair, number_of_steps)
        p.solutions[str(number_of_steps) + pair] = pair_results
        output += pair_results
        if i != len(p.template)-1:
            output.subtract(p.template[i])

    min_count = min(output.values())
    max_count = max(output.values())

    return max_count - min_count


def p14():
    filename = "inputs/14"
    ext = ".txt"
    input_list = get_line_input_as_list(filename + ext, "string")
    input_list_test = get_line_input_as_list(filename + "-test" + ext, "string")

    t1_1 = time.time()
    output1 = part1(input_list, 10)
    t1_2 = time.time()
    t2_1 = time.time()
    output2 = part2(input_list, 40)
    t2_2 = time.time()

    print(f"part1: {(t1_2-t1_1)} part2:{(t2_2-t2_1)}")
    return output1, output2
