import sys
import copy


class Sudoku(object):
    def __init__(self, puzzle):
        # you may add more attributes if you need
        self.puzzle = puzzle  # self.puzzle is a list of lists
        self.ans = copy.deepcopy(puzzle)  # self.ans is a list of lists
        self.assignment = copy.deepcopy(puzzle)
        self.f = open('log.txt', 'a')

        for row in range(len(self.puzzle)):
            for col in range(len(self.puzzle)):
                self.assignment[row][col] = []
                if self.puzzle[row][col] == 0:
                    for i in range(1, 10):
                        if self.valid_assignment(row, col, i):
                            self.assignment[row][col].append(i)
                else:
                    self.assignment[row][col].append(self.puzzle[row][col])

        print (self.assignment)

    def find_empty_location(self):
        # find the first empty location
        for row in range(len(self.assignment)):
            for col in range(len(self.assignment[0])):
                if len(self.assignment[row][col]) > 1:
                    return row, col
        return -1, -1

    def valid_assignment(self, empty_loc_row, empty_loc_col, num_assigned):
        # check if the number is already in the row
        for col in range(len(self.puzzle[0])):
            if self.puzzle[empty_loc_row][col] == num_assigned:
                return False

        # check if the number is already in the col.
        for row in range(len(self.puzzle)):
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

    def valid_assignment_list(self, empty_loc_row, empty_loc_col, num_assigned):
        # check if the number is already in the row
        for col in range(len(self.assignment[0])) :
            if self.assignment[empty_loc_row][col] == num_assigned and col != empty_loc_col:
                return False

        # check if the number is already in the col.
        for row in range(len(self.assignment)):
            if self.assignment[row][empty_loc_col] == num_assigned and row != empty_loc_row:
                return False

        # check if it is in the box
        # get the location of the top-left location of the current square
        top_left_row = empty_loc_row - empty_loc_row % 3
        top_left_col = empty_loc_col - empty_loc_col % 3
        for i in range(3):
            for j in range(3):
                if self.assignment[top_left_row + i][top_left_col + j] == num_assigned and top_left_row + i != empty_loc_row and top_left_col + j != empty_loc_col:
                    return False
        # not found in all three conditions, return True
        return True

    def forward_check(self, empty_loc_row, empty_loc_col, num_removed):
        for col in range(len(self.assignment[0])):
            if num_removed in self.assignment[empty_loc_row][col] and col != empty_loc_col and len(self.assignment[empty_loc_row][col]) == 1:
                return False

        for row in range(len(self.assignment)):
            if num_removed in self.assignment[row][empty_loc_col] and row != empty_loc_row and len(self.assignment[row][empty_loc_col]) == 1:
                return False

        top_left_row = empty_loc_row - empty_loc_row % 3
        top_left_col = empty_loc_col - empty_loc_col % 3
        for i in range(3):
            for j in range(3):
                if num_removed in self.assignment[top_left_row + i][top_left_col + j] \
                        and top_left_row + i != empty_loc_row and top_left_col + j != empty_loc_col and len(self.assignment[top_left_row + i][top_left_col + j]) == 1:
                    return False

        return True

    def solve_sudoku(self):
        empty_loc_row, empty_loc_col = self.find_empty_location()
        self.f.write(str(empty_loc_row) + " " + str(empty_loc_col))
        if empty_loc_row == -1 or empty_loc_col == -1:
            # we are done if we don't find any empty cell
            return True
        temp = copy.deepcopy(self.assignment[empty_loc_row][empty_loc_col])
        backup = copy.deepcopy(self.assignment)

        if (self.assignment[1][8] == [9]):
            return False

        for value in temp:
            if self.valid_assignment_list(empty_loc_row, empty_loc_col, [value]):
                # try assigning first
                self.assignment[empty_loc_row][empty_loc_col] = [value]
                # if this is possible solution
                self.f.write(str(self.assignment))
                self.f.write("\n")
                if not self.forward_check(empty_loc_row, empty_loc_col, value):
                    self.assignment = backup
                    return False

                if self.solve_sudoku():
                    return True
            # if failure, put it back
            self.assignment = backup

        # cannot find solution
        return False

    def solve(self):
        if not self.solve_sudoku():
            print('We cannot solve')
        self.ans = self.assignment
        # don't pr int anything here. just resturn the answer
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
