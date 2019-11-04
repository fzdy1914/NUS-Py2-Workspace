import sys
import copy


class Sudoku(object):
    def __init__(self, puzzle):
        # you may add more attributes if you need
        self.puzzle = puzzle  # self.puzzle is a list of lists
        self.ans = copy.deepcopy(puzzle)  # self.ans is a list of lists

        self.assignment = [[[self.puzzle[i][j]] for j in range(9)] for i in range(9)]

        for row in range(9):
            for col in range(9):
                if self.assignment[row][col] == [0]:
                    self.assignment[row][col].remove(0)
                    for i in range(1, 10):
                        if self.valid_assignment(row, col, i):
                            self.assignment[row][col].append(i)

    def find_empty_location(self):
        # find the first empty location
        for row in range(9):
            for col in range(9):
                if self.puzzle[row][col] == 0:
                    return row, col
        return -1, -1

    def valid_assignment(self, empty_loc_row, empty_loc_col, num_assigned):
        # check if the number is already in the row
        for col in range(9):
            if self.puzzle[empty_loc_row][col] == num_assigned:
                return False

        # check if the number is already in the col.
        for row in range(9):
            if self.puzzle[row][empty_loc_col] == num_assigned:
                return False

        # check if it is in the box
        # get the location of the top-left location of the current square
        top_left_row = empty_loc_row - empty_loc_row % 3
        top_left_col = empty_loc_col - empty_loc_col % 3
        for i in range(3):
            for j in range(3):
                if self.puzzle[top_left_row + i][top_left_col + j] == num_assigned:
                    return False
        # not found in all three conditions, return True
        return True

    def solve_sudoku(self):
        empty_loc_row, empty_loc_col = self.find_empty_location()
        if empty_loc_row == -1 or empty_loc_col == -1:
            # we are done if we don't find any empty cell
            return True
        for value in self.assignment[empty_loc_row][empty_loc_col]:
            # digit 1 to 9
            # if this is a valid assignment
            if self.valid_assignment(empty_loc_row, empty_loc_col, value):
                # try assigning first
                self.puzzle[empty_loc_row][empty_loc_col] = value
                # if this is possible solution
                if self.solve_sudoku():
                    return True
            # if failure, put it back
            self.puzzle[empty_loc_row][empty_loc_col] = 0

        # cannot find solution
        return False

    def solve(self):
        if not self.solve_sudoku():
            print('We cannot solve')
        self.ans = self.puzzle

        # don't print anything here. just resturn the answer
        # self.ans is a list of lists
        return self.ans

    # you may add more classes/functions if you think is useful
    # However, ensure all the classes/functions are in this file ONLY


if __name__ == "__main__":
    # STRICTLY do NOT modify the code in the main function here
    if len(sys.argv) != 3:
        print ("\nUsage: python sudoku_A2_v1.py input.txt output.txt\n")
        raise ValueError("Wrong number of arguments!")

    try:
        f = open(sys.argv[1], 'r')
    except IOError:
        print ("\nUsage: python sudoku_A2_v1.py input.txt output.txt\n")
        raise IOError("Input file not found!")

    puzzle = [[0 for i in range(9)] for j in range(9)]
    lines = f.readlines()

    i, j = 0, 0
    for line in lines:
        for number in line:
            if '0' <= number <= '9':
                puzzle[i][j] = int(number)
                j += 1
                if j == 9:
                    i += 1
                    j = 0

    sudoku = Sudoku(puzzle)
    ans = sudoku.solve()

    with open(sys.argv[2], 'a') as f:
        for i in range(9):
            for j in range(9):
                f.write(str(ans[i][j]) + " ")
            f.write("\n")
