from tools import (get_input_as_list,)

class Game:
    def __init__(self, input_list):
        self.numbers_to_be_called = self.make_called_number_list(input_list)
        self.game_boards = self.make_game_boards(input_list)
        self.boards_that_have_won = []

    def make_game_boards(self, input_list):
        """Creates and stores game boards as a list of integers

            I was strongly determined to run with my first idea of
            keeping the board data structure as simple as possible
            by using ONLY the numbers on the board rather both for
            their value and whether or not they have been called rather
            than having the numbers themselves as well as a boolean
            mask/flag or a separate/compound container for marked
            numbers like a tuple. But because these bingo cards can
            contain 0's and -0 is equal to 0 in Python, I decided to
            add 1 to all numbers on the board when it is made, then
            make adjustments later.
        """
        boards = []
        new_board = []
        for i, line in enumerate(input_list):
            if i > 1:
                if line != "":
                    new_board.extend([int(x)+1 for x in line.split(None, 5)])
                else:
                    boards.append(new_board)
                    new_board = []
        boards.append(new_board)
        return boards

    def make_called_number_list(self, input_list):
        """Returns a list of integers from the first line of input"""
        line = input_list[0].splitlines()
        return [int(x) for x in line[0].split(",")]

    def run_game(self):
        """Calls numbers and checks boards for wins, returning first winning board

        Goes through list of numbers to be called, calling one number
        each time. See mark_one_number_on_all_boards for details.
        After 5 number calls, starts checking every possible win option
        on every board. See check_all_boards_for_any_win for details.
        As soon as a winner is found, it is returned with the computed value.
        """
        for i, number in enumerate(self.numbers_to_be_called):
            if i < 5:
                self.mark_one_number_on_all_boards(number)
            else:
                self.mark_one_number_on_all_boards(number)
                result = self.check_all_boards_for_any_win()
                if result:
                    return self.get_sum_of_unmarked(result[0]) * number

    def run_game_last_winner(self):
        """Calls numbers and checks boards for wins, returning when all boards have won

        Goes through list of numbers to be called, calling one number
        each time. See mark_one_number_on_all_boards for details.
        After 5 number calls, starts checking every possible win option
        on every board. See check_all_boards_for_any_win for details. When a board has
        won, it is put in a separate list and no longer checked for wins.
        When all boards have won, the last board to win is returned with the computed value.
        """
        for i, number in enumerate(self.numbers_to_be_called):
            if self.game_boards:
                if i < 5:
                    self.mark_one_number_on_all_boards(number)
                else:
                    self.mark_one_number_on_all_boards(number)
                    winning_boards = self.check_all_boards_for_any_win()
                    if winning_boards:
                        for winning_board in winning_boards:
                            self.move_game_board_to_winners(winning_board,
                                                            number,
                                                            self.get_sum_of_unmarked(winning_board) * number)
        return self.boards_that_have_won[-1][0]

    def move_game_board_to_winners(self, board, number, score):
        """Move a winning game board from the list of acvtive boards to the list of winners"""
        # print((score, number, board))
        # print(f"boards remaining: {len(self.game_boards)}")
        self.boards_that_have_won.append((score, number, board))
        self.game_boards.remove(board)

    def mark_one_number_on_one_board(self, board, number):
        """Marks a number on a board by making it negative

            Remember that boards have all numbers+1 to make
            negative marking work, so number given needs one
            added to it
        """
        try:
            board.index(number+1)
            board[board.index(number+1)] *= -1
        except ValueError:
            pass

    def mark_one_number_on_all_boards(self, number):
        for board in self.game_boards:
            self.mark_one_number_on_one_board(board, number)

    def check_one_board_for_one_win(self, board, list_of_indices):
        for board_index in list_of_indices:
            if board[board_index] > 0:
                return False
        return True

    def check_one_board_for_any_win(self, board):
        """Checks a board for any win.

            Wins are boards with a full row or column of marked numbers.
            Indices of board spots are as follows:

            0,   1,  2,  3,  4
            5,   6,  7,  8,  9
            10, 11, 12, 13, 14
            15, 16, 17, 18, 19
            20, 21, 22, 23, 24

        """
        horizontal_wins = [list(range(5 * i, 5 * i + 5)) for i in range(0, 5)]
        vertical_wins = [list(range(i, i + 25, 5)) for i in range(0, 5)]
        for possible_win in horizontal_wins + vertical_wins:
            if self.check_one_board_for_one_win(board, possible_win):
                return True
        return False

    def check_all_boards_for_any_win(self):
        """Checks all boards for any win and returns all winning boards if any"""
        winning_boards = []
        for board in self.game_boards:
            if self.check_one_board_for_any_win(board):
                winning_boards.append(board)
        if len(winning_boards) > 0:
            return winning_boards
        else:
            return None

    def get_sum_of_unmarked(self, board):
        """Return sum of unmarked numbers

            Note that numbers on board a stored as 1 more than
            their actual value to make marking them as negative
            work correctly.
        """
        return sum([x-1 for x in board if x > 0])


def part1(input_list):
    game = Game(input_list)
    return game.run_game()


def part2(input_list):
    game = Game(input_list)
    return game.run_game_last_winner()




def p04():
    filename_test = "inputs/04-test.txt"
    input_list_test = get_input_as_list(filename_test, "string")

    filename = "inputs/04.txt"
    input_list = get_input_as_list(filename, "string")

    output1 = part1(input_list)
    output2 = part2(input_list)

    return output1, output2
