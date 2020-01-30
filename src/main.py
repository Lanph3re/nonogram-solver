import json

def solver(puzzle):
    num_col = len(puzzle['columns'])
    num_row = len(puzzle['rows'])

    board = [[False for _ in range(num_col)] for _ in range(num_row)]



if __name__ == '__main__':
    puzzle = json.loads(open('../samples/sample1.json').read())
    solver(puzzle)
