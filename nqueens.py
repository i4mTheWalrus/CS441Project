import numpy as np
from timeit import default_timer as timer
import time
np.set_printoptions(linewidth= 150, formatter=None)

n = 4


class Square:
    def __init__(self, state):
        self.state = state
    def update_square(self, new_state):
        if(self.state != -1):#it's not a queen
            self.state += new_state


class Board():
    def __init__(self, n):
        self.n = n
        self.board_size = n * n
        # Board with numbers representing # of attacks on each tile
        #self.constraints = np.zeros((n,n), dtype=int)
        self.constraints = np.zeros((n,n), Square)
        # List to hold Queen position for each column
        self.queens = []

    # Calling this with True will show where queens are placed
    def print_constraints(self, display_queens = False):
        if display_queens is True:
            board_display = self.constraints.astype(object)
            queens = self.queens
            for column, queen in zip(board_display.T, queens):
                column[queen] = 'Q'
            print('\n'.join(['\t'.join([str(cell) for cell in row]) for row in board_display]))
        else:
            print(self.constraints)

    # 1 Queen will be placed in each column
    def place_queen(self, space):
        self.queens.append(space)
        self.add_constraints(space)

    def remove_queen(self, space):
        self.queens.remove(space)
        self.remove_constraints(space)

    def add_constraints(self, row):
        col = len(self.queens) - 1
        # Increment row
        self.constraints[row] += 1
        # Increment column
        self.constraints[:,col] += 1

        # Increment diagonally

        rd_start = row + col
        ld_start = row - col

        # Flatten to 1D array
        self.constraints = np.ravel(self.constraints)
        for i in range(self.n):
            if rd_start > -1:
                self.constraints[self.rcToSpace(rd_start, i)] += 1
                rd_start -=1
            if ld_start < self.n:
                self.constraints[self.rcToSpace(ld_start, i)] += 1
                ld_start += 1
        # Change back to 2D array
        self.constraints = self.constraints.reshape(n,n)

    def remove_constraints(self, row):
        # This is basically the same as add_constraints except it does -= 1

        col = len(self.queens) - 1
        # Increment row
        self.constraints[row] -= 1
        # Increment column
        self.constraints[:, col] -= 1
        # Increment diagonally

        rd_start = row + col
        ld_start = row - col

        self.constraints = np.ravel(self.constraints)
        for i in range(self.n):
            if rd_start > -1:
                self.constraints[self.rcToSpace(rd_start, i)] -= 1
                rd_start -= 1
            if ld_start < self.n:
                self.constraints[self.rcToSpace(ld_start, i)] -= 1
                ld_start += 1

        self.constraints = self.constraints.reshape(n, n)

    def solution_found(self):
        return True if len(self.queens) == n else False

    def get_possible_moves(self):
        # Get list of 0's. If there are multiple 0's pick randomly
        next_column =  len(self.queens)
        possible_moves = np.where(self.constraints[:,next_column]== 0)[0]
        return possible_moves

    # This takes in row & col and returns corresponding index in 1D Array
    def rcToSpace(self, row, col):
        space = row * self.n + col
        if space >= self.board_size or space < 0:
            return -1
        else:
            return space

if __name__ == "__main__":
    board = Board(n)
    print('----------------Starting board--------------------------')
    possible_moves = board.get_possible_moves()
    start = np.random.choice(possible_moves)
    board.place_queen(start)
    board.print_constraints(True)
    print('--------------------------------------------------------')

    while(True):
        if board.solution_found():
            print('SOLUTION FOUND!!!!!!!')
            print(board.print_constraints(True))
            break
        # For each column:
            # Get array of indices of zeros
            # Randomly pick
            # No backtrack logic yet
        print('-------------------- {} ---------------------------------'.format(len(board.queens)))
        possible_moves = board.get_possible_moves()
        print('possible moves: {}'.format(possible_moves))
        move = np.random.choice(possible_moves)
        print('picked: {}'.format(move))
        board.place_queen(move)
        board.print_constraints(True)
        print('--------------------------------------------------------')
        time.sleep(1)
