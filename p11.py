from tools import (get_csv_line_input_as_list, get_line_input_as_list)
"""
General Approach:
    Take a similar approach to days 4 and 10 with a class that holds the input
    as a list along with a visited list to prevent repeats. On each day, it iterate
    through the list and processes each element and its overflows. It feels like there 
    might be a better way to do this, but nothing comes to mind before jumping in.
    
    Second thought: Perhaps there is an overlay approach I could take? Build a new list
    that is like a mask of numbers to add, then add it to he original list in the end?
    This doesn't seem too much different than the original approach.
"""


class Octopuses:
    def __init__(self, input_list):
        self.data = [ int(value) for value in "".join(input_list)]
        self.total_length = len(self.data)
        self.line_length = len(input_list[0])
        self.flashed = []
        self.flash_count = 0

    def __str__(self):
        output = []
        for line in range(self.total_length//self.line_length):
            line_as_str = [str(value) for value in self.data[line * self.line_length: line * self.line_length+self.line_length]]
            output.append("".join(line_as_str))
        return "\n".join(output)

    def get_adjacent_locations_indices(self, index):
        """Given an absolute index of a number, provides absolute indices of adjacent numbers"""
        adjacent_indices = []
        if index > self.total_length - 1:
            raise ValueError(f"index {index} used in get_adjacent_locations_indices is too large."
                              "Index must be between 0 and total_length:{self.total_length}")
        else:
            # left
            if index % self.line_length > 0:
                adjacent_indices.append(index - 1)
            # right
            if index % self.line_length < self.line_length - 1:
                adjacent_indices.append(index + 1)
            # up
            if index > self.line_length - 1:
                adjacent_indices.append(index - self.line_length)
            # down
            if index < self.total_length - self.line_length:
                adjacent_indices.append(index + self.line_length)
            # up-left
            if index > self.line_length - 1 and index % self.line_length > 0:
                adjacent_indices.append(index - 1 - self.line_length)
            # up-right
            if index > self.line_length - 1 and index % self.line_length < self.line_length - 1:
                adjacent_indices.append(index + 1 - self.line_length)
            # down-left
            if index < self.total_length - self.line_length and index % self.line_length > 0:
                adjacent_indices.append(index + self.line_length - 1)
            # down-right
            if index < self.total_length - self.line_length and index % self.line_length < self.line_length - 1:
                adjacent_indices.append(index + self.line_length + 1)
            return adjacent_indices

    def process_one_octopus(self, index):
        """Increment if not visited and increase neighbors if going over 9"""
        # print(f"Trying to process octopus at index: {index}")
        if not self.flashed[index]:
            if self.data[index] < 9:
                self.data[index] += 1
            else:
                self.data[index] = 0
                self.flashed[index] = True
                self.flash_count += 1
                neighbors = self.get_adjacent_locations_indices(index)
                for neighbor in neighbors:
                    self.process_one_octopus(neighbor)

    def process_all_octopuses(self):
        self.flashed = [False for item in range(self.total_length)]
        for i in range(self.total_length):
            self.process_one_octopus(i)

    def find_first_synchronous_flash(self):
        """Finds the first synchronous flash by looping until sum of octos is 0"""
        count_of_days = 0
        while sum(self.data) != 0:
            self.process_all_octopuses()
            count_of_days += 1
        return count_of_days


def part1(input_list):
    o = Octopuses(input_list)
    for x in range(100):
        o.process_all_octopuses()
    # print("After Day 100")
    # print(o)
    return o.flash_count

def part2(input_list):
    o = Octopuses(input_list)
    return o.find_first_synchronous_flash()


def p11():
    filename = "inputs/11"
    ext = ".txt"
    input_list = get_line_input_as_list(filename + ext, "string")
    input_list_test = get_line_input_as_list(filename + "-test" + ext, "string")

    output1 = part1(input_list)
    output2 = part2(input_list)

    return output1, output2
