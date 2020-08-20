import sys
import copy


class Sudoku(object):
    def __init__(self, puzzle):
        # you may add more attributes if you need
        self.puzzle = puzzle  # self.puzzle is a list of lists
        self.ans = []  # self.ans is a list of lists
        self.level = 0

        # self.assignment = copy.deepcopy(puzzle)
        self.assignment = [[[self.puzzle[i][j]] for j in range(9)] for i in range(9)]

        for row in range(9):
            for col in range(9):
                if self.assignment[row][col] == [0]:
                    self.assignment[row][col].remove(0)
                    for i in range(1, 10):
                        if self.valid_assignment_assignment(row, col, [i]):
                            self.assignment[row][col].append(i)
        
        self.constraints = set()
        # constraints are tuple of tuples, used for AC3
        # add constraint to each square
        for i in range(9):
          for j in range(9):
            current = (i,j)
            # add row constraints for neighbors in the same row
            for col in range(9):
              if col!=j:
                self.constraints.add((current, (i, col)))
            
            # add column constraints for neighbors in the same column 
            for row in range(9):
              if row!= i:
                self.constraints.add((current, (row, j)))
            
            # add square constraints for neighbors in the same square
            top_left_row = i - i%3
            top_left_col = j - j%3
      
            for add_i in range(3):
                for add_j in range(3):
                    if top_left_row + add_i != i or top_left_col + add_j != j:
                        
                        self.constraints.add((current, (top_left_row + add_i, top_left_col + add_j)))
            
            # print('after one cell, number of constraints become {}'.format(len(self.constraints)))


    def get_neighbors(self, loc_row, loc_col):
      # get all the neighbors of the location in list
      # the list elements are tuples consisting of (row, col )
      neighbors = set() # a set of neighbors
      # add row constraints for neighbors in the same row
      for col in range(9):
        if col!=loc_col:
          neighbors.add((loc_row, col))
      
      # add column constraints for neighbors in the same column 
      for row in range(9):
        if row!= loc_row:
          neighbors.add((row, loc_col))
      
      # add square constraints for neighbors in the same square
      top_left_row = loc_row - loc_row%3
      top_left_col = loc_col - loc_col%3

      for add_i in range(3):
          for add_j in range(3):
              if top_left_row + add_i != loc_row or top_left_col + add_j != loc_col:
                  neighbors.add((top_left_row + add_i, top_left_col + add_j))
    
      return neighbors
      
    def AC3(self):
      queue = list(self.constraints) # a queue of all constraints
      while len(queue) > 0:
          constraint = queue.pop(0)
          
          Xi = constraint[0]
          Xj = constraint[1]

          # print('constraint is {} and {}'.format(Xi, Xj))
          if self.revise(Xi, Xj):
              
              if len(self.assignment[Xi[0]][Xi[1]]) == 0 or len(self.assignment[Xj[0]][Xj[1]]) == 0:

                  return False
              neighbors = self.get_neighbors(Xi[0], Xi[1])
              neighbors.remove(Xj)
              for Xk in neighbors:
                  queue.append((Xk, Xi))

      if self.find_empty_location() == (-1,-1): # no emptyy location
          return True
      return False
   
    def revise(self, Xi, Xj):
        # Xj and Xi are both tuples
        revised = False
        domain_x = self.assignment[Xi[0]][Xi[1]][:]
        domain_y = self.assignment[Xj[0]][Xj[1]]
        
        for x_value in domain_x:
            # remove the value from the domain of x if there is no  value in y such that the constraint can be satisfied
            if sum([1 if y_value!=x_value else 0 for y_value in domain_y])==0:
                self.assignment[Xi[0]][Xi[1]].remove(x_value)
                revised = True
        return revised

    def find_empty_location(self):
        # find the first empty location
        # find the first empty location
        for row in range(9):
            for col in range(9):
                if len(self.assignment[row][col]) > 1:
                    return row, col
        return -1, -1

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

    def solve_sudoku(self):
        self.level += 1
        empty_loc_row, empty_loc_col = self.find_empty_location()
        if empty_loc_row == -1 or empty_loc_col == -1:
            # we are done if we don't find any empty cell
            return True
        temp = self.assignment[empty_loc_row][empty_loc_col][:]
        for value in copy.deepcopy(temp):
            # digit 1 to 9
            # if this is a valid assignment

            if self.valid_assignment_assignment(empty_loc_row, empty_loc_col, [value]):
                # try assigning first
                self.assignment[empty_loc_row][empty_loc_col] = [value]
                # if this is possible solution
                if self.solve_sudoku():
                    return True
            # if failure, put it back
            self.assignment[empty_loc_row][empty_loc_col] = temp

        # cannot find solution
        return False

    def solve(self):
        
        if not self.AC3():
            print('We cannot solve by just using arc consistency')
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


