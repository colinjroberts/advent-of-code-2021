from tools import (get_csv_line_input_as_list, get_line_input_as_list) 


class Origami():
    def __init__(self, input_list):
        self.list_of_points = []
        self.height = 0
        self.width = 0
        for item in input_list:
            points = item.split(",")
            x = int(points[0])
            y = int(points[1])
            self.list_of_points.append((x, y))
            self.width = max(self.width, x+1)
            self.height = max(self.height, y+1)

        self.matrix = [[False for w in range(self.width)] for h in range(self.height)]
        for item in self.list_of_points:
            self.matrix[item[1]][item[0]] = True

    def __str__(self):
        output = []
        for row in range(self.height):
            output_line = []
            for column in range(self.width):
                if self.matrix[row][column]:
                    output_line.append("#")
                else:
                    output_line.append(".")
            output.append("".join(output_line))
        return "\n".join(output) + "\n" + f"w:{self.width}, h:{self.height}"

    def fold(self, axis, number):
        # print(axis, number, self.width, self.height, len(self.matrix), len(self.matrix[0]))
        # folds the matrix along the given axis
        if axis == "x":
            for row in range(self.height):
                for column in range(number - (self.width - 1 - number), number):
                    self.matrix[row][column] = self.matrix[row][column] or self.matrix[row][number + number - column]
            self.width = self.width // 2

        elif axis == "y":
            # for each rows in the matrix less than y:
            for row in range(number - (self.height - 1 - number), number):
                for column in range(self.width):
                    self.matrix[row][column] = self.matrix[row][column] or self.matrix[number + number - row][column]
            self.height = self.height // 2

        else:
            raise ValueError("for fold(axis, number) axis must be x or y")

        return

    def get_visible_dots(self):
        count = 0
        for row in range(self.height):
            for col in range(self.width):
                count += self.matrix[row][col]
        return count


def part1(input_list):

    # Take only the points and feed them into Origami
    space_loc = input_list.index('')
    o = Origami(input_list[:space_loc])
    # print(str(o))

    # Transform folds into usable input
    folds_to_make = []
    for item in input_list[space_loc+1:]:
        op = item.split(" ")[2]
        folds_to_make.append(op.split("="))
    for i, fold_op in enumerate(folds_to_make):
        if i == 0:
            o.fold(fold_op[0], int(fold_op[1]))
    # print(str(o))

    print(o.get_visible_dots())


def part2(input_list):

    # Take only the points and feed them into Origami
    space_loc = input_list.index('')
    o = Origami(input_list[:space_loc])
    # print(str(o))

    # Transform folds into usable input
    folds_to_make = []
    for item in input_list[space_loc+1:]:
        op = item.split(" ")[2]
        folds_to_make.append(op.split("="))
    for i, fold_op in enumerate(folds_to_make):
        o.fold(fold_op[0], int(fold_op[1]))
    print(str(o))


def p13():
    filename = "inputs/13"
    ext = ".txt"
    input_list = get_line_input_as_list(filename + ext, "string")
    input_list_test = get_line_input_as_list(filename + "-test" + ext, "string")

    output1 = part1(input_list)
    output2 = part2(input_list)

    return output1

# 897 is too high
# 102 is too low