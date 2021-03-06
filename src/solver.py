from src import utils
from copy import deepcopy


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
            if first_clue != nonogram.num_row:
                board[first_clue][col_idx] = nonogram.SPACE

        if board[-1][col_idx] == nonogram.BOX:
            last_clue = nonogram.col_clues[col_idx][-1]
            for i in range(last_clue):
                board[-1 - i][col_idx] = nonogram.BOX
            if -1 - last_clue != -(nonogram.num_row + 1):
                board[-1 - last_clue][col_idx] = nonogram.SPACE

    # rows
    for row_idx in range(nonogram.num_row):
        if board[row_idx][0] == nonogram.BOX:
            first_clue = nonogram.row_clues[row_idx][0]
            for i in range(first_clue):
                board[row_idx][i] = nonogram.BOX
            if first_clue != nonogram.num_col:
                board[row_idx][first_clue] = nonogram.SPACE

        if board[row_idx][-1] == nonogram.BOX:
            last_clue = nonogram.row_clues[row_idx][-1]
            for i in range(last_clue):
                board[row_idx][-1 - i] = nonogram.BOX
            if -1 - last_clue != -(nonogram.num_col + 1):
                board[row_idx][-1 - last_clue] = nonogram.SPACE


def get_firstbox_column(nonogram, col_idx):
    for i in range(nonogram.col_size):
        if nonogram.board[i][col_idx] == nonogram.BOX:
            return i
    return None


def get_lastbox_column(nonogram, col_idx):
    for i in range(nonogram.col_size):
        if nonogram.board[-(i + 1)][col_idx] == nonogram.BOX:
            return -(i + 1)
    return None


def get_firstbox_row(nonogram, row_idx):
    for i in range(nonogram.row_size):
        if nonogram.board[row_idx][i] == nonogram.BOX:
            return i
    return None


def get_lastbox_column(nonogram, row_idx):
    for i in range(nonogram.row_size):
        if nonogram.board[row_idx][-(i + 1)] == nonogram.BOX:
            return -(i + 1)
    return None


def glue(nonogram):
    board = nonogram.board
    # columns
    for col_idx in range(nonogram.num_col):
        first_box = get_firstbox_column(nonogram, col_idx)
        if first_box is not None:
            distance = first_box + 1
            first_clue = nonogram.col_clues[col_idx][0]
            if distance < first_clue:
                for i in range(first_clue - distance):
                    if first_box + 1 + i < nonogram.col_size:
                        board[first_box + 1 + i][col_idx] = nonogram.BOX

        last_box = get_lastbox_column(nonogram, col_idx)
        if last_box is not None:
            distance = -last_box
            last_clue = nonogram.col_clues[col_idx][-1]
            if distance < last_clue:
                for i in range(last_clue - distance):
                    if last_box + 1 + i < nonogram.col_size:
                        board[last_box - 1 - i][col_idx] = nonogram.BOX

    # rows
    for row_idx in range(nonogram.num_row):
        first_box = get_firstbox_row(nonogram, row_idx)
        if first_box is not None:
            distance = first_box + 1
            first_clue = nonogram.row_clues[row_idx][0]
            if distance < first_clue:
                for i in range(first_clue - distance):
                    if first_box + 1 + i < nonogram.col_size:
                        board[row_idx][first_box + 1 + i] = nonogram.BOX

        last_box = get_lastbox_column(nonogram, row_idx)
        if last_box is not None:
            distance = -last_box
            last_clue = nonogram.row_clues[row_idx][-1]
            if distance < last_clue:
                for i in range(last_clue - distance):
                    if last_box + 1 + i < nonogram.col_size:
                        board[row_idx][last_box - 1 - i] = nonogram.BOX


def get_possible_rows(nonogram,
                      row_idx,
                      clue_idx,
                      start_idx,
                      cur_row):
    if clue_idx == len(nonogram.row_clues[row_idx]):
        return cur_row

    clue = nonogram.row_clues[row_idx][clue_idx]
    if nonogram.row_size - start_idx < clue:
        return None

    ret_vec = []
    for i in range(start_idx, nonogram.row_size - clue + 1):
        temp_row = deepcopy(cur_row)
        for j in range(clue):
            temp_row[i + j] = nonogram.BOX
        ret = get_possible_rows(nonogram,
                                row_idx,
                                clue_idx + 1,
                                i + clue + 1,
                                temp_row)

        if ret is not None and len(ret) != 0:
            if clue_idx == len(nonogram.row_clues[row_idx]) - 1:
                ret_vec.append(ret)
            else:
                ret_vec += ret

    return ret_vec


def filter_row(nonogram, possible_row, row_idx):
    cur_row_with_clues = nonogram.board[row_idx]
    for i in range(nonogram.row_size):
        if cur_row_with_clues[i] == nonogram.BOX \
                and possible_row[i] != nonogram.BOX:
            return False
        if cur_row_with_clues[i] == nonogram.SPACE \
                and possible_row[i] != nonogram.SPACE:
            return False
    return True


def filter_promise_rows(nonogram, possible_rows, row_idx):
    filtered_rows = []
    for possible_row in possible_rows:
        if filter_row(nonogram, possible_row, row_idx):
            filtered_rows.append(possible_row)

    return filtered_rows


def semi_check(nonogram, board, row_idx):
    cur_board_with_clues = nonogram.board
    for i in range(row_idx + 1):
        for j in range(nonogram.col_size):
            if cur_board_with_clues[i][j] == nonogram.BOX\
                    and board[i][j] != nonogram.BOX:
                return False
            if cur_board_with_clues[i][j] == nonogram.SPACE \
                    and board[i][j] != nonogram.SPACE:
                return False
    return True


def get_nextbox_column(nonogram, board, col_idx, cur_idx):
    for i in range(cur_idx, nonogram.col_size):
        if nonogram.board[i][col_idx] == nonogram.BOX:
            return i
    return None


def column_check(nonogram, board, col_idx):
    col_clue = nonogram.col_clues[col_idx]
    cur_idx = 0

    for clue in col_clue:
        next_block_idx = get_nextbox_column(nonogram, board, col_idx, cur_idx)
        if next_block_idx is None:
            return False

        for i in range(clue):
            if board[next_block_idx + i][col_idx] != nonogram.BOX:
                return False

        if clue != col_clue[-1] \
                and board[next_block_idx + clue][col_idx] != nonogram.SPACE:
            return False

        cur_idx = next_block_idx + clue + 1

    return True


def is_complete(nonogram, board):
    for i in range(nonogram.num_col):
        if not column_check(nonogram, board, i):
            return False
    return True


def dfs(nonogram, board, possible_rows, row_idx):
    print(row_idx)
    if row_idx == nonogram.num_row:
        return board if is_complete(nonogram, board) else None

    for possible_row in possible_rows[row_idx]:
        temp_board = deepcopy(board)
        temp_board[row_idx] = possible_row

        # It's hard to decide
        # if current board satisfy all the constraints
        # because current board is not completed.
        # so semi-check instead of whole check
        if not semi_check(nonogram, temp_board, row_idx):
            continue

        res = dfs(nonogram, temp_board, possible_rows, row_idx + 1)
        if res is not None:
            return res

    return None


def solver(nonogram):
    # loop with deterministic algorithms
    for _ in range(5):
        simple_boxes(nonogram)
        simple_end(nonogram)
        glue(nonogram)

    # now it's time to dfs
    # get all possible combinations
    all_possible_rows = []
    for i in range(nonogram.num_row):
        all_possible_rows.append(
            get_possible_rows(
                nonogram,
                i,
                0,
                0,
                [nonogram.SPACE for _ in range(nonogram.row_size)]
            ))

    # rows that we get above is all possible rows
    # with no considering the constraints(clues)
    # so it has to be filtered
    filtered_rows = []
    for i in range(nonogram.num_row):
        filtered_rows.append(
            filter_promise_rows(
                nonogram,
                all_possible_rows[i],
                i
            ))

    for x in filtered_rows:
        print(len(x))

    # do final solving algorithm!
    temp_board = [
        [0 for _ in range(nonogram.num_col)]
        for _ in range(nonogram.num_row)
    ]
    dfs(nonogram, temp_board, all_possible_rows, 0)
