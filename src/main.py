import json
from utils import *


def solver(puzzle):
    cols = puzzle['columns']
    rows = puzzle['rows']

    board = [[False for _ in range(len(cols))] for _ in range(len(rows))]

    # Simple boxes
    for col in cols:
        pass


if __name__ == '__main__':
    puzzle = json.loads(open('../samples/sample1.json').read())
    solver(puzzle)
