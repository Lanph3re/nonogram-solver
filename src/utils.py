def block_size(blocks, idx):
    return blocks[idx]


def space_available(L, blocks, idx):
    sum = 0
    for i in range(len(blocks)):
        sum += 0 if i == idx else block_size(blocks, i)

    return L - len(blocks) + 1 - sum


# return zero-based index
def potential_first_cell(blocks, idx):
    if idx == 0:
        return 0

    ret_val = 0
    for i in range(idx):
        ret_val += (block_size(blocks, i) + 1)

    return ret_val


# return the size of potential sub-block and its size
# if no sub-block exists return (non_positive_value, -1)
def potential_sub_block(L, blocks, idx):
    sub_block_size = 2*block_size(blocks, idx) - \
        space_available(L, blocks, idx)
    sub_block_pos = - \
        1 if sub_block_size <= 0 else potential_sub_block_pos(L, blocks, idx)

    return sub_block_size, sub_block_pos


def potential_sub_block_pos(L, blocks, idx):
    return potential_first_cell(blocks, idx) \
        + space_available(L, blocks, idx) - block_size(blocks, idx)
