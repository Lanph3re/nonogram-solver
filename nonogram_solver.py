import json
from flask import Flask, render_template
from src import nonogram, solver

app = Flask(__name__)
test_puzzle = '/samples/sample1.json'


@app.route("/")
def nonogram_solver():
    # TODO: support solver arbitrary puzzle via file upload
    puzzle = nonogram.Nonogram(json.loads(open(test_puzzle).read()))
    solver.solver(puzzle)

    return render_template('index.html')


if __name__ == '__main__':
    app.run()
