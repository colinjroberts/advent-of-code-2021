from tools import (get_csv_line_input_as_list, get_line_input_as_list)


def part1(input_list):
    """Identify incorrect closing marks

    Search through line checking for properly closing brackets.
    Stop at the first incorrect closing character on each corrupted line and return it.

    General approach:
    - For each opening tag, put a closing tag onto a stack.
    - For each closing tag, pop one off and compare
    - If it doesn't match, report corrupted line and wrong character
    - Calculate points using characters

    Example 1:
    [<>({}){}[([])<>]]
    ^
    s = ]
    --------------------
    [<>({}){}[([])<>]]
     ^
    s = ]>
    --------------------
    [<>({}){}[([])<>]]
                     ^
    s = ]
    ====================

    Example 2 (at the end):
    <([]){()}[{}])
                 ^
    s = >
    --------------------

    :return: sum of point values of all first errors
    """

    point_lookup = {
        ")": 3,
        "]": 57,
        "}": 1197,
        ">": 25137,
    }

    opening_brackets = ["(", "{", "[", "<"]

    opening_closing_bracket_map = {
        "(": ")",
        "[": "]",
        "{": "}",
        "<": ">",
    }

    def find_syntax_error(string_of_brackets):
        """Find first syntax error

        :return: character of first syntax error or empty string if none
        """
        s = []
        for bracket in string_of_brackets:
            if bracket in opening_brackets:
                s.append(opening_closing_bracket_map[bracket])
            else:
                popped_bracket = s.pop()
                if bracket != popped_bracket:
                    return bracket
        return ""

    # Lots of extra lists for easier debugging
    errors = []
    errors_points = []
    indices_of_rows_with_errors = []
    for i, row in enumerate(input_list):
        error = find_syntax_error(row)
        if error:
            errors.append(error)
            errors_points.append(point_lookup[error])
            indices_of_rows_with_errors.append(i)

    # print(errors, errors_points)
    return indices_of_rows_with_errors, sum(errors_points)


def part2(input_list, indices_of_row_errors):
    """Complete lines with incomplete brackets

    Use a similar approach to part 1 to generate a list of brackets.

    For each line of input (skipping it if it is a line with syntax errors)
    find the missing brackets at the end and score them.
    """
    point_lookup = {
        ")": 1,
        "]": 2,
        "}": 3,
        ">": 4,
    }

    opening_brackets = ["(", "{", "[", "<"]

    opening_closing_bracket_map = {
        "(": ")",
        "[": "]",
        "{": "}",
        "<": ">",
    }

    def get_list_of_missing_brackets(string_of_brackets):
        """Finds brackets missing from a string

        Expects only valid strings of brackets that are truncated.
        Uses a stack to keep track of expected closing tag while iterating
        though brackets, popping closing brackets off the stack if they
        are found in the list. At the end of the list, the remaining stack
        will be the missing closing tags in reverse order.

        :return: list of closing brackets in correct order
        """
        s = []
        for b in string_of_brackets:
            if b in opening_brackets:
                s.append(opening_closing_bracket_map[b])
            else:
                popped_bracket = s.pop()
        return s[::-1]

    scores = []
    for i, row in enumerate(input_list):
        # discard if it has syntax errors
        if i in indices_of_row_errors:
            continue

        # get missing brackets and score
        missing_brackets_points = []
        missing_brackets = get_list_of_missing_brackets(row)
        if missing_brackets:
            score = 0
            for bracket in missing_brackets:
                missing_brackets_points.append(point_lookup[bracket])
                score *= 5
                score += point_lookup[bracket]
            scores.append(score)

    # sort scores and choose middle
    scores.sort()
    return scores[len(scores)//2]


def p10():
    filename = "inputs/10"
    ext = ".txt"
    input_list = get_line_input_as_list(filename + ext, "string")
    input_list_test = get_line_input_as_list(filename + "-test" + ext, "string")

    # N.B. Part 2 relies on the work of Part 1, so inputs must be the same
    input_used_in_both = input_list

    indices_of_row_errors, sum_of_error_points = part1(input_used_in_both)
    output1 = sum_of_error_points
    output2 = part2(input_used_in_both, indices_of_row_errors)

    return output1, output2
