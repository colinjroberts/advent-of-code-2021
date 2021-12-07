from tools import (get_line_input_as_list, )

"""
Possible Approaches:
- Build a collection of lines, then check every point on the 
  grid for overlapping spots.
- Read in lines and calculate the grid locations covered by
  each line, adding them to a Counter, then return the count of 
  all keys with values > 1. !-Went with this one. Seemed faster.
  
Notes:
- Lines can be drawn in either direction (L->R or R->L, T->B, B->T)
- Diagonal lines at 45 degrees will have the same number of changes
  in x values as y values, but vertical or horizontal lines will not
"""

def parse_line_of_input_into_tuple_of_points(line_of_input):
    """Converts line of input from 'x1,y1 -> x2,y2' to (x1,y1,x2,y2)"""
    coordinates = line_of_input.split(" -> ")
    start = [int(n) for n in coordinates[0].split(",")]
    end = [int(n) for n in coordinates[1].split(",")]
    return start[0], start[1], end[0], end[1]


def filter_for_vertical_lines(list_of_line_tuples):
    return [point_tuple for point_tuple in list_of_line_tuples if point_tuple[1] == point_tuple[3]]


def filter_for_horizontal_lines(list_of_line_tuples):
    return [point_tuple for point_tuple in list_of_line_tuples if point_tuple[0] == point_tuple[2]]


def parse_one_line_tuple_into_list_of_points(line_tuple):
    """Converts line of input from (x1,y1,x2,y2) to [(x1,y1)...(x2,y2)]

    Handles both interesting cases which is a line with points that
    decrease in value (e.g. (9,5,2,1)) and the differences between
    vertical/horizontal lines and diagonal lines which have different
    numbers of points that change.

    """
    list_of_points = []

    if line_tuple[0] <= line_tuple[2]:
        list_of_x_values = [x for x in range(line_tuple[0], line_tuple[2]+1)]
    else:
        list_of_x_values = [x for x in range(line_tuple[0], line_tuple[2]-1, -1)]

    if line_tuple[1] <= line_tuple[3]:
        list_of_y_values = [y for y in range(line_tuple[1], line_tuple[3]+1)]
    else:
        list_of_y_values = [y for y in range(line_tuple[1], line_tuple[3]-1, -1)]

    if len(list_of_x_values) == len(list_of_y_values):
        for x, y in zip(list_of_x_values, list_of_y_values):
            list_of_points.append((x, y))
    else:
        for x in list_of_x_values:
            for y in list_of_y_values:
                list_of_points.append((x, y))

    return list_of_points


def part1(input_list):

    # Extract points into tuples
    list_of_line_tuples = []
    for line in input_list:
        list_of_line_tuples.append(parse_line_of_input_into_tuple_of_points(line))

    # Filter for only horizontal and vertical lines
    v_lines = filter_for_vertical_lines(list_of_line_tuples)
    h_lines = filter_for_horizontal_lines(list_of_line_tuples)

    # Create dict of points with counts
    dict_of_points = dict()
    for line in h_lines + v_lines:
        points_in_line = parse_one_line_tuple_into_list_of_points(line)
        for point in points_in_line:
            if point not in dict_of_points:
                dict_of_points[point] = 1
            else:
                dict_of_points[point] += 1

    return len([point for point in dict_of_points.keys() if dict_of_points[point] > 1])


def part2(input_list):
    # Extract points into tuples
    list_of_line_tuples = []
    for line in input_list:
        list_of_line_tuples.append(parse_line_of_input_into_tuple_of_points(line))

    # Create dict of points with counts
    dict_of_points = dict()
    for line in list_of_line_tuples:
        points_in_line = parse_one_line_tuple_into_list_of_points(line)
        for point in points_in_line:
            if point not in dict_of_points:
                dict_of_points[point] = 1
            else:
                dict_of_points[point] += 1

    # for item in dict_of_points:
    #     print(item, dict_of_points[item])

    return len([point for point in dict_of_points.keys() if dict_of_points[point] > 1])


def p05():
    filename_test = "inputs/05-test.txt"
    input_list_test = get_line_input_as_list(filename_test, "string")

    filename = "inputs/05.txt"
    input_list = get_line_input_as_list(filename, "string")

    output1 = part1(input_list)
    output2 = part2(input_list)

    return output1, output2
