from .nonogram import Nonogram


class RuleBasedSolver:
    def __init__(self, puzzle):
        self.nonogram = Nonogram(puzzle)

    def _space_available(self, size, clues, idx):
        space = 0
        for i in range(len(clues)):
            space += clues[i] if i != idx else 0

        return size - (len(clues) - 1) - space

    def _potential_first_cell(self, clues, idx):
        ret_val = 0
        for i in range(idx):
            ret_val += clues[i] + 1

        return ret_val

    def _potential_sub_block_pos(self, size, clues, idx):
        return self._potential_first_cell(clues, idx) \
            + self._space_available(size, clues, idx) - clues[idx]

    def _potential_sub_block(self, size, clues, i):
        sub_block_size = clues[i] - \
            (self._space_available(size, clues, i) - clues[i])
        sub_block_pos = -1 \
            if sub_block_size <= 0 \
            else self._potential_sub_block_pos(size, clues, i)

        return sub_block_size, sub_block_pos

    def _get_firstbox_column(self, i):
        for j in range(self.nonogram.get_height()):
            if self.nonogram.board[j][i] == self.nonogram.BOX:
                return j
        return None

    def _get_lastbox_column(self, i):
        for j in range(self.nonogram.get_height()):
            if self.nonogram.board[-(j + 1)][i] == self.nonogram.BOX:
                return -(j + 1)
        return None

    def _get_firstbox_row(self, i):
        for j in range(self.nonogram.get_width()):
            if self.nonogram.board[i][j] == self.nonogram.BOX:
                return j
        return None

    def _get_lastbox_row(self, i):
        for j in range(self.nonogram.get_width()):
            if self.nonogram.board[i][-(j + 1)] == self.nonogram.BOX:
                return -(j + 1)
        return None

    def _simple_boxes(self):
        for j in range(self.nonogram.get_width()):
            col_clue = self.nonogram.col_clues[j]
            for k in range(len(col_clue)):
                sb_size, sb_pos = \
                    self._potential_sub_block(
                        self.nonogram.get_height(), col_clue, k)
                if sb_pos != -1:
                    for i in range(sb_size):
                        self.nonogram.board[sb_pos + i][j] = self.nonogram.BOX

        for j in range(self.nonogram.get_height()):
            row_clue = self.nonogram.row_clues[j]
            for k in range(len(row_clue)):
                sb_size, sb_pos = \
                    self._potential_sub_block(
                        self.nonogram.get_width(), row_clue, k)
                if sb_pos != -1:
                    for i in range(sb_size):
                        self.nonogram.board[j][sb_pos + i] = self.nonogram.BOX

    def _simple_end(self):
        board = self.nonogram.board
        for j in range(self.nonogram.get_width()):
            if board[0][j] == self.nonogram.BOX:
                for i in range(self.nonogram.col_clues[j][0]):
                    board[i][j] = self.nonogram.BOX

            if board[-1][j] == self.nonogram.BOX:
                for i in range(self.nonogram.col_clues[j][-1]):
                    board[-1 - i][j] = self.nonogram.BOX

        for j in range(self.nonogram.get_height()):
            if board[j][0] == self.nonogram.BOX:
                for i in range(self.nonogram.row_clues[j][0]):
                    board[j][i] = self.nonogram.BOX

            if board[j][-1] == self.nonogram.BOX:
                for i in range(self.nonogram.row_clues[j][-1]):
                    board[j][-1 - i] = self.nonogram.BOX

    def _glue(self):
        board = self.nonogram.board
        for j in range(self.nonogram.get_width()):
            first_box = self._get_firstbox_column(j)
            if first_box is not None:
                distance = first_box + 1
                first_clue = self.nonogram.col_clues[j][0]
                if distance < first_clue:
                    for i in range(first_clue - distance):
                        if first_box + 1 + i < self.nonogram.get_height():
                            board[first_box + 1 + i][j] = self.nonogram.BOX

            last_box = self._get_lastbox_column(j)
            if last_box is not None:
                distance = -last_box
                last_clue = self.nonogram.col_clues[j][-1]
                if distance < last_clue:
                    for i in range(last_clue - distance):
                        if last_box + 1 + i < self.nonogram.get_height():
                            board[last_box - 1 - i][j] = self.nonogram.BOX

        for j in range(self.nonogram.get_height()):
            first_box = self._get_firstbox_row(j)
            if first_box is not None:
                distance = first_box + 1
                first_clue = self.nonogram.row_clues[j][0]
                if distance < first_clue:
                    for i in range(first_clue - distance):
                        if first_box + 1 + i < self.nonogram.get_width():
                            board[j][first_box + 1 + i] = self.nonogram.BOX

            last_box = self._get_lastbox_row(j)
            if last_box is not None:
                distance = -last_box
                last_clue = self.nonogram.row_clues[j][-1]
                if distance < last_clue:
                    for i in range(last_clue - distance):
                        if last_box + 1 + i < self.nonogram.get_width():
                            board[j][last_box - 1 - i] = self.nonogram.BOX

    def generate_solution(self):
        for _ in range(5):
            self._simple_boxes()
            self._simple_end()
            self._glue()
        return self.nonogram
