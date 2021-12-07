import math
from tools import get_csv_line_input_as_list


def part1(input_list):
    """Sort crabs, try every horizontal position, keep track of min"""
    min_fuel_cost = math.inf
    for n in range(input_list[0], input_list[len(input_list)-1]):
        total_steps = 0
        for crab in input_list:
            total_steps += abs(n - crab)
        min_fuel_cost = min(min_fuel_cost, total_steps)
    return min_fuel_cost


def part2(input_list):
    """Sort crabs, calculate and save fuel cost for steps, try every possible position

    Take the largest distance (min crab to max crab), and add
    all of possible sums into a dict, then for the rest of the crabs,
    just lookup the steps to find the minimum
    """

    # sort the crabs
    fuel_cost_dict = {}
    input_list_reverse = input_list[::-1].copy()

    # Calculate the most steps it could possibly take
    # Then make a dict of all of the fuel costs for step counts 0 -> most steps
    s1 = input_list_reverse[0]
    s2 = input_list[0]
    max_number_of_steps = abs(s2 - s1) * (abs(s2 - s1)+1) // 2
    min_fuel_cost = math.inf
    fuel_cost_dict[0] = 0
    for step in range(1, max_number_of_steps):
        fuel_cost_dict[step] = fuel_cost_dict[step-1] + step  # Calculate using previous number
        # fuel_cost_dict[step] = step * (step+1) // 2  # Calculate directly

    # for every possible goal position, make a list of the steps it would take
    # each crab to get there, then use the lookup table to sum the cost of each
    # of all of those changes. Before trying the next possible goal position,
    # save the fuel cost if it is the smallest one tried so far. At the end
    # return the min fuel cost
    for n in range(input_list_reverse[0], input_list[0]-1, -1):
        step_counts = []
        for crab_position in input_list:
            step_counts.append(abs(n - crab_position))

        fuel_sum = 0
        for step_count in step_counts:
            fuel_sum += fuel_cost_dict[step_count]
            # print(f"from {step_count+n} to goal {n} is {step_count + n} steps costing {fuel_cost_dict[step_count]}")
        # print(f"which is a sum of {fuel_sum} ")
        min_fuel_cost = min(min_fuel_cost, fuel_sum)
    return min_fuel_cost


def p07():
    filename = "inputs/07"
    ext = ".txt"
    input_list = get_csv_line_input_as_list(filename + ext, "int")
    input_list_test = get_csv_line_input_as_list(filename + "-test" + ext, "int")

    input_list.sort()
    input_list_test.sort()

    output1 = part1(input_list)
    output2 = part2(input_list)

    return output1, output2
