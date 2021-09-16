import random


class Nonogram:
    BOX = 1
    SPACE = 2

    def __init__(self, puzzle):
        self.col_clues = puzzle['columns']
        self.row_clues = puzzle['rows']

        self.row_size = len(self.col_clues)
        self.num_row = len(self.row_clues)

        self.col_size = len(self.row_clues)
        self.num_col = len(self.col_clues)

        self.board = [
            [False for _ in range(self.num_col)]
            for _ in range(self.num_row)
        ]

    def random(self):
        for i in range(self.num_row):
            for j in range(self.num_col):
                self.board[i][j] = random.getrandbits(1)

        return self

    def is_solved(self):
        pass
