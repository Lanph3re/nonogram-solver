import random


class Nonogram:
    BOX = 1
    SPACE = 2

    def __init__(self, puzzle):
        self.col_clues = puzzle['columns']
        self.row_clues = puzzle['rows']

        self.num_row = len(self.row_clues)
        self.num_col = len(self.col_clues)

        self.board = [[0 for _ in range(self.num_col)]
                      for _ in range(self.num_row)]

    def get_width(self):
        return self.num_col

    def get_height(self):
        return self.num_row

    def get_column(self, i):
        column = []
        for j in range(self.get_height()):
            column.append(self.board[j][i])
        return column

    def _get_num_blocks(self, arr):
        blocks = []
        cnt = 0
        for cell in arr:
            if cell == 1:
                cnt += 1
            elif cell == 0 and cnt != 0:
                blocks.append(cnt)
                cnt = 0
            else:
                pass

        if cnt != 0:
            blocks.append(cnt)

        return blocks

    def get_num_blocks_column(self, i):
        col = [row[i] for row in self.board]
        return self._get_num_blocks(col)

    def is_solved(self):
        pass
