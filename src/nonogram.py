class Nonogram:
    def __init__(self, puzzle):
        self.col_clues = puzzle['columns']
        self.row_clues = puzzle['rows']

        self.board = [ \
            [False for _ in range(len(self.col_clues))] \
            for _ in range(len(self.row_clues))]

        self.row_size = len(self.col_clues)
        self.num_row= len(self.row_clues)

        self.col_size = len(self.row_clues)
        self.num_col = len(self.col_clues)

    # TODO: print board in gui
    def __repr__(self):
        max_blocks_col = -1
        for col in self.col_clues:
            max_blocks_col = len(col) \
                if len(col) > max_blocks_col \
                else max_blocks_col 
        max_blocks_row = -1
        for row in self.row_clues:
            max_blocks_row = len(row) \
                if len(row) > max_blocks_row \
                else max_blocks_row

        # print column constraints
        for row_idx in range(max_blocks_col):
            for _ in range(max_blocks_row):
                print('   ', end='')
            print('| ', end='')

            for col_idx in range(self.num_col):
                num_space = max_blocks_col - len(self.col_clues[col_idx])
                if row_idx < num_space:
                    print('   ', end='')
                else:
                    print('%2d ' % self.col_clues[col_idx][row_idx - num_space], end='')
            print('')

        print('-'*(self.num_col*5))

        # print row constraints and board
        for row_idx in range(self.num_row):
            num_space = max_blocks_row - len(self.row_clues[row_idx])
            for _ in range(num_space):
                print('   ', end='')
            for clue in self.row_clues[row_idx]:
                print('%2d ' % clue, end='')
            print('|', end='')

            for col_idx in range(self.num_col):
                if self.board[row_idx][col_idx] is True:
                    print('  ㅁ', end='')
                else:
                    print('   ', end='')
            print('')
        return ''
