import numpy as np
from timeit import default_timer as timer
import time
np.set_printoptions(linewidth= 150, formatter=None)

n = 4

class Board():
    def __init__(self, n):
        self.n = n
        self.board_size = n * n
        # Board with numbers representing # of attacks on each tile
        self.constraints = np.zeros((n,n), dtype=int)
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
        self.constraints[row, col] = 0

        # Increment diagonally
        #Left up
        if(col > 0 and row > 0):
            new_row = row-1
            new_col = col-1
            while(new_row >= 0 and new_col >= 0):
                self.constraints[new_row, new_col] += 1
                new_row -=1
                new_col -=1
        #Right up
        if (col < self.n-1 and row > 0):
            new_row = row - 1
            new_col = col + 1
            while (new_row >= 0 and new_col <= self.n-1):
                self.constraints[new_row, new_col] += 1
                new_row -= 1
                new_col += 1
        # Left down
        if (col > 0 and row < self.n-1):
            new_row = row + 1
            new_col = col - 1
            while (new_row <= self.n-1 and new_col >= 0):
                self.constraints[new_row, new_col] += 1
                new_row += 1
                new_col -= 1
        # Right down
        if (col < self.n - 1 and row < self.n-1):
            new_row = row + 1
            new_col = col + 1
            while (new_row <= self.n-1 and new_col <= self.n-1):
                self.constraints[new_row, new_col] += 1
                new_row += 1
                new_col += 1

    def remove_constraints(self, row):
        # This is basically the same as add_constraints except it does -= 1

        col = len(self.queens)
        print('removing queen {}:'.format(col))
        # Increment row
        self.constraints[row] -= 1
        # Increment column
        self.constraints[:, col] -= 1
        self.constraints[row, col] = 0
        # Increment diagonally

        # Increment diagonally
        #Left up
        if(col > 0 and row > 0):
            new_row = row-1
            new_col = col-1
            while(new_row >= 0 and new_col >= 0):
                self.constraints[new_row, new_col] -= 1
                new_row -=1
                new_col -=1
        #Right up
        if (col < self.n-1 and row > 0):
            new_row = row - 1
            new_col = col + 1
            while (new_row >= 0 and new_col <= self.n-1):
                self.constraints[new_row, new_col] -= 1
                new_row -= 1
                new_col += 1
        # Left down
        if (col > 0 and row < self.n-1):
            new_row = row + 1
            new_col = col - 1
            while (new_row <= self.n-1 and new_col >= 0):
                self.constraints[new_row, new_col] -= 1
                new_row += 1
                new_col -= 1
        # Right down
        if (col < self.n - 1 and row < self.n-1):
            new_row = row + 1
            new_col = col + 1
            while (new_row <= self.n-1 and new_col <= self.n-1):
                self.constraints[new_row, new_col] -= 1
                new_row += 1
                new_col += 1

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
    record = []
    print('----------------Starting board--------------------------')
    possible_moves = board.get_possible_moves()
    record.append(possible_moves)
    start = np.random.choice(possible_moves)
    board.place_queen(start)
    board.print_constraints(False)
    print('--------------------------------------------------------')

    while(True):

        if board.solution_found():
            print('SOLUTION FOUND!!!!!!!')
            print(board.print_constraints(False))
            print(board.queens)
            #for i in reversed(board.queens):
            #    board.remove_queen(i)
            #    board.print_constraints()
            #    time.sleep(1)
            break
        # For each column:
            # Get array of indices of zeros
            # Randomly pick
            # No backtrack logic yet
        print('-------------------- {} ---------------------------------'.format(len(board.queens)))
        possible_moves = board.get_possible_moves()

        if(len(possible_moves)==0):
            board.constraints = np.zeros((n,n), dtype=int)
            board.queens = []
            print('----------------Restarting board--------------------------')
            possible_moves = board.get_possible_moves()
            start = np.random.choice(possible_moves)
            board.place_queen(start)
            board.print_constraints(False)
            print('--------------------------------------------------------')
        possible_moves = board.get_possible_moves()
        print('possible moves: {}'.format(possible_moves))
        move = np.random.choice(possible_moves)
        print('picked: {}'.format(move))
        board.place_queen(move)
        board.print_constraints()
        print('--------------------------------------------------------')

