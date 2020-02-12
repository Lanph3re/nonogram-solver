class Nonogram:
    def __init__(self, puzzle):
        self.col_clues = puzzle['columns']
        self.row_clues = puzzle['rows']

        self.board = [
            [False for _ in range(len(self.col_clues))]
            for _ in range(len(self.row_clues))]

        self.row_size = len(self.col_clues)
        self.num_row = len(self.row_clues)

        self.col_size = len(self.row_clues)
        self.num_col = len(self.col_clues)

    # TODO: print board in gui
