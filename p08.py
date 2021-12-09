from tools import get_line_input_as_list


def part1(input_list):

    def count_uniques(str_input):
        """Given a left side of a line, count the occurrences of unique word lengths"""
        unique_lengths = set([2, 3, 4, 7])
        count = 0
        for item in str_input.split(" "):
            if len(item.strip()) in unique_lengths:
                count += 1
        return count

    # Sum all of the occurrences of unique word lengths
    total_count = 0
    for line in input_list:
        split_line = line.split("|")
        total_count += count_uniques(split_line[1])

    return total_count


def part2(input_list):
    """
      0:      1:      2:      3:      4:
     aaaa    ....    aaaa    aaaa    ....
    b    c  .    c  .    c  .    c  b    c
    b    c  .    c  .    c  .    c  b    c
     ....    ....    dddd    dddd    dddd
    e    f  .    f  e    .  .    f  .    f
    e    f  .    f  e    .  .    f  .    f
     gggg    ....    gggg    gggg    ....
      5:      6:      7:      8:      9:
     aaaa    aaaa    aaaa    aaaa    aaaa
    b    .  b    .  .    c  b    c  b    c
    b    .  b    .  .    c  b    c  b    c
     dddd    dddd    ....    dddd    dddd
    .    f  e    f  .    f  e    f  .    f
    .    f  e    f  .    f  e    f  .    f
     gggg    gggg    ....    gggg    gggg

    Occurrences of Segments in Each Number
    =========================================
            top  0,    2, 3,    5, 6, 7, 8, 9 = 8
        topleft  0,          4, 5, 6,    8, 9 = 6*
       topright  0, 1, 2, 3, 4,       7, 8, 9 = 8
         middle        2, 3, 4, 5, 6,    8, 9 = 7
     bottomleft  0,    2,          6,    8    = 4*
    bottomright  0, 1,    3, 4, 5, 6, 7, 8, 9 = 9*
         bottom  0,    2, 3,    5, 6,    8, 9 = 7
    =========================================
         counts  6  2  5  5  4  5  6  3  7  6
                    *        *        *  *

    counts of letter occurrences for topleft, bottomleft, and bottomright are unique
    combined with 1, 4, and 7 give us top, middle, and topright and therefore bottom

    letters will be stored in a list: [top, topleft, topright, middle, bottomleft, bottomright, bottom]

    Algorithm:
    - take left side
        - parse letters into list of letters with location in list representing which bar
        - e.g. dacedgfb cdfbe gcdfa fbcad dab cefabd cdfgeb eafb cagedb ab | cdfeb fcadb cdfeb cdbaf
               above [d, e, a, f, g, b, c] is [top, topleft, topright, middle, bottomleft, bottomright, bottom]
        - use list of bars to create list of sets of letters using list index to represent the display number
        - e.g. [{cagedb}, {ca}, {gcdfa}, {fbcad}, {cefa}, {cdfbe}, {cdfgeb}, {cab}, {dfgabce}, {cefabd}]
    - take right side
        - for each item, get its index in the list and add the index it to a string to make the number
        - convert int to string and save it
    - return sum of all the ints
    """

    def create_word_to_number_map_list(one_line_of_input):
        letter_options = ['a', 'b', 'c', 'd', 'e', 'f', 'g']
        letter_to_position_map = ['', '', '', '', '', '', '']
        # letter_to_position_map = [top, topleft, topright, middle, bottomleft, bottomright, bottom]

        # counts of letter occurrences determine topleft, bottomleft, and bottomright
        # because they are unique, so set them directly
        left = one_line_of_input.split("|")[0]
        for letter in letter_options:
            # bottomleft
            if left.count(letter) == 4:
                letter_to_position_map[4] = letter
            # topleft
            elif left.count(letter) == 6:
                letter_to_position_map[1] = letter
            # bottomright
            elif left.count(letter) == 9:
                letter_to_position_map[5] = letter

        # 1, 4, 7, and 8 have unique numbers of bars, so we can make the sets of those words
        # from the beginning
        word_list = [set() for i in range(10)]
        for word in left.split(" "):
            word = word.strip()
            if len(word) == 2:
                word_list[1] = set(word)
            elif len(word) == 4:
                word_list[4] = set(word)
            elif len(word) == 3:
                word_list[7] = set(word)
            elif len(word) == 7:
                word_list[8] = set(word)

        # Use 1, 4, 7, and 8 along with the above to derive the rest

        # Derive letter used for topright using the number 1
        # We have bottom right (letter_to_position_map[5]), so top right the letter that isn't that one
        letter_to_position_map[2] = list(word_list[1].difference(set(letter_to_position_map)))[0]

        # Derive letter used for top by using the number 7
        # We have bottom and top right (letter_to_position_map 2 and 5), so top is the one remaining
        letter_to_position_map[0] = list(word_list[7].difference(set(letter_to_position_map)))[0]

        # Derive letter used for middle by using number 4
        # We have bottom and top right and top left (letter_to_position_map 2, 3, 5),
        # so middle is the one remaining
        letter_to_position_map[3] = list(word_list[4].difference(set(letter_to_position_map)))[0]

        # Derive letter used for bottom by using the number 8
        # Now there is only one letter remaining, use 8 to get bottom
        letter_to_position_map[6] = list(word_list[8].difference(set(letter_to_position_map)))[0]

        # Now that we know which letter is used to represent which bar
        # Fill in the rest of the word_list
        # letter_to_position_map = [top, topleft, topright, middle, bottomleft, bottomright, bottom]

        # Set of letters used in 0
        word_list[0] = {letter_to_position_map[0],
                        letter_to_position_map[1],
                        letter_to_position_map[2],
                        letter_to_position_map[4],
                        letter_to_position_map[5],
                        letter_to_position_map[6]}

        # Set of letters used in 2
        word_list[2] = {letter_to_position_map[0],
                        letter_to_position_map[2],
                        letter_to_position_map[3],
                        letter_to_position_map[4],
                        letter_to_position_map[6]}

        # Set of letters used in 3
        word_list[3] = {letter_to_position_map[0],
                        letter_to_position_map[2],
                        letter_to_position_map[3],
                        letter_to_position_map[5],
                        letter_to_position_map[6]}

        # Set of letters used in 5
        word_list[5] = {letter_to_position_map[0],
                        letter_to_position_map[1],
                        letter_to_position_map[3],
                        letter_to_position_map[5],
                        letter_to_position_map[6]}

        # Set of letters used in 6
        word_list[6] = {letter_to_position_map[0],
                        letter_to_position_map[1],
                        letter_to_position_map[3],
                        letter_to_position_map[4],
                        letter_to_position_map[5],
                        letter_to_position_map[6]}

        # Set of letters used in 9
        word_list[9] = {letter_to_position_map[0],
                        letter_to_position_map[1],
                        letter_to_position_map[2],
                        letter_to_position_map[3],
                        letter_to_position_map[5],
                        letter_to_position_map[6]}

        return word_list

    def get_number_from_right_side(one_line, listmap_of_letters):
        # get right side
        one_line = one_line.split("|")[1]
        one_line = one_line.strip()
        output_number = ""

        # for each word representing a number on the right side of the line
        # lookup its index in the list and concat it to the output number
        # then return the int of the output number
        for word in one_line.split(" "):
            output_number += str(listmap_of_letters.index(set(word)))
        return int(output_number)

    # Get numbers from each line as a list for easy inspection if needed
    list_of_output_numbers = []
    for line in input_list:
        listmap_of_numbers_to_letters = create_word_to_number_map_list(line)
        number = get_number_from_right_side(line, listmap_of_numbers_to_letters)
        list_of_output_numbers.append(number)

    # print(list_of_output_numbers)
    return sum(list_of_output_numbers)


def p08():
    filename = "inputs/08"
    ext = ".txt"
    input_list = get_line_input_as_list(filename + ext, "string")
    input_list_test = get_line_input_as_list(filename + "-test" + ext, "string")

    output1 = part1(input_list_test)
    output2 = part2(input_list)

    return output1, output2
