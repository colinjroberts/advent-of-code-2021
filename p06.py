from tools import (get_csv_line_input_as_list, )
from collections import Counter
"""
Possible Approaches:
- Reproduce the system in the problem using integers in 
  a list as changing values
- This feels very calculable; the visual doesn't yield a clear pattern, but 
  it's clearly exponential growth. Part two definitely requires a different solution.
- Can I calculate the growth rate for one fish such that I know how many fish 
  it will have spawned on day n? Then, I will just do that for each input fish and
  add them all together.

    2-delay            1-delay                    2^(n-1)
1   (1) 0              (1) 0                      (1) 0
2   (2) 02             (2) 01                     (2) 00
3   (3) 012            (3) 001                    (4) 0000
4   (4) 0012           (5) 00011                  (8) 00000000
5   (6) 000122         (8) 00000111              (16) 0000000000000000
6   (9) 000011222     (12) 000000001111          (32) 00000000000000000000000000000000
7  (13) 0000001112222 (20) 00000000000011111111  (64) 0x64
   (19) 0000000001111222222                      

- Instead of trying to model growth and instead of keeping the data in a giant list, 
  just keep track of how many of each number there are in a dict and move those around.
"""

def process_day_list(input_list):
    input_list = input_list
    for i, fish in enumerate(input_list):
        new_fish_to_make = 0
        if fish > 0:
            input_list[i] -= 1
        elif fish == 0:
            new_fish_to_make += 1
            input_list[i] = 6
        for new_fish in range(new_fish_to_make):
            input_list.append(9)
    return input_list


def part1(input_list, days):
    for day in range(days):
        input_list = process_day_list(input_list)
    return len(input_list)


def part2(input_list, days):
    old_fish_dict = {0: 0,
                     1: 0,
                     2: 0,
                     3: 0,
                     4: 0,
                     5: 0,
                     6: 0,
                     7: 0,
                     8: 0,
                     9: 0}

    new_fish_dict = {0: 0,
                     1: 0,
                     2: 0,
                     3: 0,
                     4: 0,
                     5: 0,
                     6: 0,
                     7: 0,
                     8: 0,
                     9: 0}

    # Populate list
    for item in input_list:
        old_fish_dict[item] += 1

    # For each day, move items as needed
    # dict should I think preserve insertion order, so it should go bottom up
    for day in range(days):
        for key in old_fish_dict:
            if key == 0:
                old_fish_dict[7] += old_fish_dict[key]
                new_fish_dict[9] += old_fish_dict[key]
            else:
                old_fish_dict[key-1] += old_fish_dict[key]
            old_fish_dict[key] -= old_fish_dict[key]

        for key in new_fish_dict:
            if key == 0:
                old_fish_dict[6] += new_fish_dict[key]
                new_fish_dict[9] += new_fish_dict[key]
            else:
                new_fish_dict[key-1] += new_fish_dict[key]
            new_fish_dict[key] -= new_fish_dict[key]

    return sum(list(old_fish_dict.values()) + list(new_fish_dict.values()))


def p06():
    filename = "inputs/06"
    ext = ".txt"
    input_list = get_csv_line_input_as_list(filename + ext, "int")
    input_list_test = get_csv_line_input_as_list(filename + "-test" + ext, "int")

    part_one_days = 80
    part_one_days_test = 18
    part_two_days = 256

    output1 = part1(input_list_test.copy(), part_one_days_test)
    output2 = part2(input_list, part_two_days)

    return output1, output2
