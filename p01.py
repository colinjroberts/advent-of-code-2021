from tools import get_input_as_list


def part1(input_list):
    output = []
    for i in range(len(input_list)-1):
        output.append(input_list[i] < input_list[i+1])

    return sum(output)


def part2(input_list):
    sums = []

    window_sum, window_start = 0.0, 0
    for window_end in range(len(input_list)):
        window_sum += input_list[window_end]

        if window_end >= 2:
            sums.append(window_sum)
            window_sum -= input_list[window_start]
            window_start += 1

    return part1(sums)


def p01():
    filename1 = "inputs/01.txt"
    input_list1 = get_input_as_list(filename1, "int")

    output1 = part1(input_list1)
    output2 = part2(input_list1)

    return output1, output2
