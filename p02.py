from tools import (get_input_as_list,)

class Submarine:
    def __init__(self):
        self.depth = 0
        self.horizontal = 0
        self.aim = 0

    def rise(self, magnitude):
        self.depth -= magnitude

    def dive(self, magnitude):
        self.depth += magnitude

    def move_forward(self, magnitude):
        self.horizontal += magnitude

    def aim_down(self, magnitude):
        self.aim += magnitude

    def aim_up(self, magnitude):
        self.aim -= magnitude

    def report_location(self):
        return self.depth, self.horizontal


def part1(input_list):
    s = Submarine()

    for instruction in input_list:
        inst, mag = instruction.split()
        if inst == "forward":
            s.move_forward(int(mag))
        elif inst == "up":
            s.rise(int(mag))
        elif inst == "down":
            s.dive(int(mag))

    depth, location = s.report_location()
    #print(depth, location)
    return depth * location

def part2(input_list):
    s = Submarine()

    for instruction in input_list:
        inst, mag = instruction.split()
        if inst == "forward":
            s.move_forward(int(mag))
            s.dive(s.aim * int(mag))
        elif inst == "up":
            s.aim_up(int(mag))
        elif inst == "down":
            s.aim_down(int(mag))

    depth, location = s.report_location()
    # print(depth, location)

    return depth * location


def p02():
    filename1 = "inputs/02.txt"
    input_list1 = get_input_as_list(filename1, "string")

    output1 = part1(input_list1)
    output2 = part2(input_list1)

    return output1, output2
