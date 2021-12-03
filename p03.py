from tools import (get_input_as_list,)


def part1(input_list):

    matrix = []
    for line in input_list:
        matrix.append([int(d) for d in line])

    most_common_bits_per_column = get_most_common_bit_per_column(matrix)
    value1 = convert_binary_list_to_int(most_common_bits_per_column)

    # invert binary to get second output
    most_common_bits_per_column2 = [abs(item - 1) for item in most_common_bits_per_column]
    value2 = convert_binary_list_to_int(most_common_bits_per_column2)

    return value1 * value2


def get_most_common_bit_per_column(matrix):
    # need counts for each column and total lines
    # if column count is greater than column_total//2, 1 is most frequent, otherwise 0s

    # sum values of each column
    new_matrix = [0 for r in matrix[0]]
    for row in matrix:
        for i, column in enumerate(row):
            new_matrix[i] += column

    # identify most used item in each column
    most_common_bit_per_column = [0 for item in new_matrix]
    for i, item in enumerate(new_matrix):
        if item >= len(matrix)/2 :
            most_common_bit_per_column[i] = 1
        else:
            most_common_bit_per_column[i] = 0

    return most_common_bit_per_column


def part2(input_list):
    matrix = []
    for line in input_list:
        matrix.append([int(d) for d in line])

    output1 = recursive_list_search_for_number(matrix, 0, "most")
    output2 = recursive_list_search_for_number(matrix, 0, "least")
    return convert_binary_list_to_int(output1) * convert_binary_list_to_int(output2)


def convert_binary_list_to_int(binary_list):
    binary_string = [str(item) for item in binary_list]
    output = int("".join(binary_string), 2)
    return output


def recursive_list_search_for_number(matrix, bit, search_direction):

    most_common_bit_per_column = get_most_common_bit_per_column(matrix)

    if len(matrix) == 1 or bit > len(most_common_bit_per_column):
        return matrix[0]

    next_list = []

    for row in matrix:
        if search_direction == "most":
            if row[bit] == most_common_bit_per_column[bit]:
                next_list.append(row)
        else:
            if row[bit] == abs(most_common_bit_per_column[bit] -1):
                next_list.append(row)

    return recursive_list_search_for_number(next_list, bit+1, search_direction)


def p03():
    # Day 2
    filename_test = "inputs/03-test.txt"
    input_list_test = get_input_as_list(filename_test, "string")

    filename = "inputs/03.txt"
    input_list = get_input_as_list(filename, "string")

    output1 = part1(input_list)
    output2 = part2(input_list)

    return output1, output2
