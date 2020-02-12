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


def solver(nonogram):
    simple_boxes(nonogram)
