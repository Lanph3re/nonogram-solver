from src import utils


# fill boxes that are self-explanatory
def simple_boxes(nonogram):
    # columns
    csize = nonogram.col_size
    for col_idx in range(nonogram.num_col):
        col_clue = nonogram.col_clues[col_idx]

        for block_idx in range(len(col_clue)):
            sb_size, sb_pos = \
                utils.potential_sub_block(csize, col_clue, block_idx)

            if sb_pos == -1:
                continue

            for i in range(sb_size):
                nonogram.board[sb_pos + i][col_idx] = True

    # rows
    rsize = nonogram.row_size
    for row_idx in range(nonogram.num_row):
        row_clue = nonogram.row_clues[row_idx]

        for block_idx in range(len(row_clue)):
            sb_size, sb_pos = \
                utils.potential_sub_block(rsize, row_clue, block_idx)

            if sb_pos == -1:
                continue

            for i in range(sb_size):
                nonogram.board[row_idx][sb_pos + i] = True


# fill clues that are at both end of row or column
def simple_end(nonogram):
    # columns
    for col_idx in range(nonogram.num_col):
        if nonogram.board[0][col_idx] == True:
            for i in range(nonogram.col_clues[col_idx][0]):
                nonogram.board[i][col_idx] = True

        if nonogram.board[-1][col_idx] == True:
            for i in range(nonogram.col_clues[col_idx][-1]):
                nonogram.board[-1 - i][col_idx] = True
    # rows
    for row_idx in range(nonogram.num_row):
        if nonogram.board[row_idx][0] == True:
            for i in range(nonogram.row_clues[row_idx][0]):
                nonogram.board[row_idx][i] = True

        if nonogram.board[row_idx][-1] == True:
            for i in range(nonogram.row_clues[row_idx][-1]):
                nonogram.board[row_idx][-1 - i] = True


def solver(nonogram):
    simple_boxes(nonogram)
    for _ in range(2):
        simple_end(nonogram)
