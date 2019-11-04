import sys
import copy


class Sudoku(object):
    def __init__(self, puzzle):
        # you may add more attributes if you need
        self.puzzle = puzzle  # self.puzzle is a list of lists
        self.ans = []  # self.ans is a list of lists

        # self.assignment = copy.deepcopy(puzzle)
        self.assignment = [[[self.puzzle[i][j]] for j in range(9)] for i in range(9)]
        self.level = 0

        for row in range(9):
            for col in range(9):
                if self.assignment[row][col] == [0]:
                    self.assignment[row][col].remove(0)
                    for i in range(1, 10):
                        if self.valid_assignment_assignment(row, col, [i]):
                            self.assignment[row][col].append(i)

    def find_least_remaining_location(self):
        # find the first empty location
        least = 10
        r_row = -1
        r_col = -1
        for row in range(9):
            for col in range(9):
                length = len(self.assignment[row][col])
                if 1 < length < least:
                    least = length
                    r_row = row
                    r_col = col
        return r_row, r_col

    def sort_least_constraining_value(self, assign_loc_row, assign_loc_col, possible_values):
        # This function takes in a list of all possible values and returns the values sorted based on the Least Constraining Heuristic. The frontmost item will be the least constraining variable.
        value_constraining = {}  # key is the allowable value, value of dictionary is the number of domain reductions caused by assigning this value
        for value in possible_values:
            num_conflict_current = 0
            # check its neighbors in the current row that contain the current value
            for i in range(9):
                if i != assign_loc_col and value in self.assignment[assign_loc_row][i]:
                    num_conflict_current += 1
            # check its neighbors in the current column that contain the current value
            for j in range(9):
                if j != assign_loc_row and value in self.assignment[j][assign_loc_col]:
                    num_conflict_current += 1

            # check its neighbors in the current square that contain the current value
            top_left_row = assign_loc_row - assign_loc_row % 3
            top_left_col = assign_loc_col - assign_loc_col % 3
            for i in range(3):
                for j in range(3):
                    if value in self.assignment[top_left_row + i][
                        top_left_col + j] and top_left_row + i != assign_loc_row and top_left_col + j != assign_loc_col:
                        num_conflict_current += 1

            value_constraining[value] = num_conflict_current

        return sorted(possible_values, key=lambda x: value_constraining[x])

    def valid_assignment_assignment(self, empty_loc_row, empty_loc_col, num_assigned):
        # check if the number is already in the row
        for col in range(9):
            if self.assignment[empty_loc_row][col] == num_assigned and col != empty_loc_col:
                return False

        # check if the number is already in the col.
        for row in range(9):
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

    def inference(self, empty_loc_row, empty_loc_col, num_assigned):
        # check if the number is already in the row
        for col in range(9):
            if num_assigned in self.assignment[empty_loc_row][col] and col != empty_loc_col:
                self.assignment[empty_loc_row][col].remove(num_assigned)
                if len(self.assignment[empty_loc_row][col]) == 0:
                    return False
                if len(self.assignment[empty_loc_row][col]) == 1:
                    return self.valid_assignment_assignment(empty_loc_row, col, self.assignment[empty_loc_row][col])

        # check if the number is already in the col.
        for row in range(9):
            if num_assigned in self.assignment[row][empty_loc_col] and row != empty_loc_row:
                self.assignment[row][empty_loc_col].remove(num_assigned)
                if len(self.assignment[row][empty_loc_col]) == 0:
                    return False
                if len(self.assignment[row][empty_loc_col]) == 1:
                    return self.valid_assignment_assignment(row, empty_loc_col, self.assignment[row][empty_loc_col])

        # check if it is in the box
        # get the location of the top-left location of the current square
        top_left_row = empty_loc_row - empty_loc_row % 3
        top_left_col = empty_loc_col - empty_loc_col % 3
        for i in range(3):
            for j in range(3):
                if num_assigned in self.assignment[top_left_row + i][top_left_col + j] and top_left_row + i != empty_loc_row and top_left_col + j != empty_loc_col:
                    self.assignment[top_left_row + i][top_left_col + j].remove(num_assigned)
                    if len(self.assignment[top_left_row + i][top_left_col + j]) == 0:
                        return False
                    if len(self.assignment[top_left_row + i][top_left_col + j]) == 1:
                        return self.valid_assignment_assignment(top_left_row + i, top_left_col + j, self.assignment[top_left_row + i][top_left_col + j])
        # not found in all three conditions, return True
        return True

    def solve_sudoku(self):
        self.level += 1
        empty_loc_row, empty_loc_col = self.find_least_remaining_location()
        if empty_loc_row == -1 or empty_loc_col == -1:
            # we are done if we don't find any empty cell
            return True

        backup = copy.deepcopy(self.assignment)
        temp = self.assignment[empty_loc_row][empty_loc_col][:]
        for value in self.sort_least_constraining_value(empty_loc_row, empty_loc_col, temp):
            if self.valid_assignment_assignment(empty_loc_row, empty_loc_col, [value]):
                self.assignment[empty_loc_row][empty_loc_col] = [value]
                if self.inference(empty_loc_row, empty_loc_col, value):

                    if self.solve_sudoku():
                        return True
                # if failure, put it back
                self.assignment = copy.deepcopy(backup)
                self.assignment[empty_loc_row][empty_loc_col].remove(value)
        # cannot find solution
        return False

    def solve(self):
        if not self.solve_sudoku():
            print('We cannot solve')
        self.ans = [[self.assignment[i][j][0] for j in range(9)] for i in range(9)]


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
