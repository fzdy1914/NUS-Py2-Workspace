import time

from sudoku_A2_Final import Sudoku

time_start = time.time()

for i in range(1, 11):

    f = open('test' + str(i) + '.txt', 'r')

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
    # print sudoku.level

time_end = time.time()
print('totally cost', time_end-time_start)
