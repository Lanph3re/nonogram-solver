import json
from utils import *
from nonogram import *

def solver(nonogram):
    # Simple boxes - columns
    col_size = nonogram.col_size
    for col_idx in range(nonogram.num_col):
        for block_idx in range(len(nonogram.col_clues[col_idx])):
            sub_block_size, sub_block_pos = \
                potential_sub_block(col_size, nonogram.col_clues[col_idx], block_idx)

            if sub_block_pos == -1:
                continue

            for i in range(sub_block_size):
                nonogram.board[sub_block_pos + i][col_idx] = True

    # Simple boxes - rows 
    row_size = nonogram.row_size
    for row_idx in range(nonogram.num_row):
        for block_idx in range(len(nonogram.row_clues[row_idx])):
            sub_block_size, sub_block_pos = \
                potential_sub_block(row_size, nonogram.row_clues[row_idx], block_idx)

            if sub_block_pos == -1:
                continue

            for i in range(sub_block_size):
                nonogram.board[row_idx][sub_block_pos + i] = True

    print(nonogram)


if __name__ == '__main__':
    nonogram = Nonogram(json.loads(open('../samples/sample1.json').read()))
    solver(nonogram)
