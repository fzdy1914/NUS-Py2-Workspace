import os
import sys
import Queue


# Use A* algorithm to solve 8-Puzzle
class Puzzle(object):
    def __init__(self, init_state, goal_state):
        self.init_state = init_state
        self.goal_state = goal_state
        self.actions = list()
        self.solvable = True

    def solve(self):
        # Return a list of actions like ["UP", "DOWN"] that represents the movement of the tiles in the direction towards the space

        start_node = Node(Board(init_state, goal_state, None), None)
        self.solvable = start_node.board.is_solvable()
        queue = Queue.PriorityQueue()
        queue.put(start_node)

        if not self.solvable:
            return ["UNSOLVABLE"]
        else:
            while not queue.empty():
                node = queue.get()
                if not node.is_goal_node():
                    neighbours = node.board.get_neighbours()
                    for i in neighbours:
                        if not (node.parent and node.parent.board.is_same_config(i)):
                            queue.put(Node(i, node))
                else:
                    while node.parent:
                        self.actions.append(node.board.move)
                        node = node.parent
                    break
            self.actions = reversed(self.actions)
            return self.actions
            
            
class Board(object):
    # Board class represents the configuration of the current progress
    def __init__(self, state, goal, move):
        self.state = state
        self.goal = goal
        self.hamming = self.hamming()
        self.manhattan = self.manhattan()
        self.move = move  # Indicates the direction of movement from the previous board to this, None if no parent node.
        
    def hamming(self):
        # Heuristic function using the hamming distance
        # Return the hamming distance cost of the configuration represented by this Board
        hamming = 0
        for i in range(3):
            for j in range(3):
                if self.state[i][j] == 0:
                    continue
                if self.state[i][j] != self.goal[i][j]:
                    hamming += 1 
        return hamming
         
    def manhattan(self):
        # Heuristic function using the manhattan distance
        # Return the manhattan distance cost of the configuration represented by this Board
        manhattan = 0
        for i in range(3):
            for j in range(3):
                if self.state[i][j] != 0 and 3 * i + j + 1 != self.state[i][j]:
                    ii = (self.state[i][j] - 1) // 3
                    jj = (self.state[i][j] - 1) % 3
                    manhattan += abs(ii - i) + abs(jj - j)
        return manhattan

    def exchange(self, i_old, j_old, i_new, j_new, move):
        # Swap the positions of the two tiles and it is used here to simulate the sliding the tiles
        new_board = [i[:] for i in self.state]
        new_board[i_old][j_old], new_board[i_new][j_new] = new_board[i_new][j_new], new_board[i_old][j_old]
        return Board(new_board, self.goal, move)

    def is_solvable(self):
        # Check whether a given configuration is solvable 
        lst = []
        for i in range(3):
            for j in range(3):
                lst.append(self.state[i][j])
        inversion_count = 0
        for i in range(0, 8):
            for j in range(i + 1, 9):
                if lst[j] != 0 and lst[i] > lst[j]:
                    inversion_count += 1
        return inversion_count % 2 == 0

    def get_neighbours(self):
        # Return a list of Board objects that represent the possible subsequent moves from this current configuration
        lst = []
        for i in range(3):
            for j in range(3):
                if self.state[i][j] == 0:
                    if i > 0:
                        lst += [self.exchange(i, j, i-1, j, "DOWN")]  # DOWN
                    if i < 2:
                        lst += [self.exchange(i, j, i+1, j, "UP")]  # UP
                    if j > 0:
                        lst += [self.exchange(i, j, i, j-1, "RIGHT")]  # RIGHT
                    if j < 2:
                        lst += [self.exchange(i, j, i, j+1, "LEFT")]  # LEFT
                    break
        return lst

    def is_same_config(self, other):
        # Check whether two Board objects have the same configuration
        state1 = self.state
        state2 = other.state
        for i in range(3):
            for j in range(3):
                if state1[i][j] != state2[i][j]:
                    return False
        return True
        

class Node(object):
    def __init__(self, board, parent):
        self.board = board
        self.parent = parent
        if not parent:
            self.path_cost = 0
        else:
            self.path_cost = parent.path_cost + 1
        self.evaluation = self.path_cost + self.board.manhattan

    def __lt__(self, other):
        # Compare the two nodes based on their evaluation function
        return self.evaluation < other.evaluation

    def is_goal_node(self):
        # Goal test
        state1 = self.board.state
        state2 = self.board.goal
        for i in range(3):
            for j in range(3):
                if state1[i][j] != state2[i][j]:
                    return False
        return True


if __name__ == "__main__":
    # do NOT modify below

    if len(sys.argv) != 3:
        raise ValueError("Wrong number of arguments!")

    try:
       f = open(sys.argv[1], 'r')
    except IOError:
        raise IOError("Input file not found!")

    init_state = [[0 for i in range(3)] for j in range(3)]
    goal_state = [[0 for i in range(3)] for j in range(3)]
    lines = f.readlines()

    i, j = 0, 0
    for line in lines:
        for number in line:
            if '0' <= number <= '8':
                init_state[i][j] = int(number)
                j += 1
                if j == 3:
                    i += 1
                    j = 0
    
    for i in range(1, 9):
        goal_state[(i-1) // 3][(i-1) % 3] = i
    goal_state[2][2] = 0
    
    puzzle = Puzzle(init_state, goal_state)
    ans = puzzle.solve()

    with open(sys.argv[2], 'a') as f:
        for answer in ans:
            f.write(answer+'\n')







