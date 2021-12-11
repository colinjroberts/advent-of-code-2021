from tools import get_line_input_as_list


def part1(input_list):
    line_length = len(input_list[0])
    total_length = len(input_list) * line_length

    def get_adjacent_locations_indices(index, total_length, line_length):
        """Given an absolute index of a number, provides absolute indices of adjacent numbers"""
        adjacent_indices = []
        # left
        if index % line_length > 0:
            adjacent_indices.append(index-1)
        # right
        if index % line_length < line_length-1:
            adjacent_indices.append(index+1)
        # up
        if index > line_length-1:
            adjacent_indices.append(index-line_length)
        # down
        if index < total_length - line_length:
            adjacent_indices.append(index+line_length)

        return adjacent_indices

    local_minima = []
    local_minima_indices = []
    for line_number, line in enumerate(input_list):
        for index_in_line, number in enumerate(line):
            adjacent_location_indices = get_adjacent_locations_indices(index_in_line + line_number*line_length,
                                                                       total_length,
                                                                       line_length)

            adjacent_numbers = [int(input_list[index//line_length][index % line_length]) for index in adjacent_location_indices]
            is_minimum = [int(number) < adj_num for adj_num in adjacent_numbers]

            if all(is_minimum):
                local_minima.append(int(number))
                local_minima_indices.append(int(index_in_line + line_number*line_length))

    return local_minima, local_minima_indices


def part2(input_list, local_minima_indices):
    """Repeat similar approach to part1, but using a class, flatten list into one array, and add bitmask"""
    class LavaTubes():
        def __init__(self, input_list_of_rows_as_strings):
            self.vent_map = []
            self.line_length = len(input_list[0])
            self.total_length = len(input_list) * self.line_length

            for row in input_list_of_rows_as_strings:
                for item in row:
                    self.vent_map.append(int(item))

            self.vent_map_visit_mask = [False for vent in self.vent_map]

        def get_adjacent_locations_indices(self, index):
            """Given an absolute index of a number, provides absolute indices of adjacent numbers"""
            adjacent_indices = []
            # left
            if index % self.line_length > 0:
                adjacent_indices.append(index-1)
            # right
            if index % self.line_length < self.line_length-1:
                adjacent_indices.append(index+1)
            # up
            if index > self.line_length-1:
                adjacent_indices.append(index-self.line_length)
            # down
            if index < self.total_length - self.line_length:
                adjacent_indices.append(index+self.line_length)

            return adjacent_indices

        def recursive_non_9_sum(self, index):
            # print(f"recursively checking index:{index} with value:{self.vent_map[index]}")
            if self.vent_map_visit_mask[index] or self.vent_map[index] == 9:
                return 0
            else:
                self.vent_map_visit_mask[index] = True
                neighbors = self.get_adjacent_locations_indices(index)
                output = 0
                for neighbor in neighbors:
                    output += self.recursive_non_9_sum(neighbor)
                return 1 + output

    lt = LavaTubes(input_list)
    basin_sums = []
    for minimum in local_minima_indices:
        basin_sums.append(lt.recursive_non_9_sum(minimum))

    basin_sums.sort()
    top_3 = basin_sums[-3:]
    return top_3[0] * top_3[1] * top_3[2]


def p09():
    filename = "inputs/09"

    ext = ".txt"
    input_list = get_line_input_as_list(filename + ext, "string")
    input_list_test = get_line_input_as_list(filename + "-test" + ext, "string")

    # N.B. Part 2 relies on the work of Part 1, so inputs must be the same
    input_used_in_both = input_list
    local_minima, local_minima_indices = part1(input_used_in_both)
    output1 = sum(local_minima) + len(local_minima)
    output2 = part2(input_used_in_both, local_minima_indices)

    return output1, output2
