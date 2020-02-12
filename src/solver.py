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
                nonogram.board[sb_pos + i][col_idx] = nonogram.BOX

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
                nonogram.board[row_idx][sb_pos + i] = nonogram.BOX


# fill clues that are at both end of row or column
def simple_end(nonogram):
    board = nonogram.board
    # columns
    for col_idx in range(nonogram.num_col):
        if board[0][col_idx] == nonogram.BOX:
            first_clue = nonogram.col_clues[col_idx][0]
            for i in range(first_clue):
                board[i][col_idx] = nonogram.BOX
            board[first_clue][col_idx] = nonogram.SPACE

        if board[-1][col_idx] == nonogram.BOX:
            last_clue = nonogram.col_clues[col_idx][-1]
            for i in range(last_clue):
                board[-1 - i][col_idx] = nonogram.BOX
            board[-1 - last_clue][col_idx] = nonogram.SPACE

    # rows
    for row_idx in range(nonogram.num_row):
        if board[row_idx][0] == nonogram.BOX:
            first_clue = nonogram.row_clues[row_idx][0]
            for i in range(first_clue):
                board[row_idx][i] = nonogram.BOX
            board[row_idx][first_clue] = nonogram.SPACE

        if board[row_idx][-1] == nonogram.BOX:
            last_clue = nonogram.row_clues[row_idx][-1]
            for i in range(last_clue):
                board[row_idx][-1 - i] = nonogram.BOX
            board[row_idx][-1 - last_clue] = nonogram.SPACE


def solver(nonogram):
    simple_boxes(nonogram)
    for _ in range(2):
        simple_end(nonogram)
