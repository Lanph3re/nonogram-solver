import json
from flask import Flask, render_template, request
from os import listdir, path
from src import nonogram, solver

app = Flask(__name__)
puzzles = listdir('puzzles')


@app.route("/")
def puzzle_list():
    return render_template('index.html', puzzles=puzzles)


@app.route('/solver')
def nonogram_solver():
    puzzle_name = 'puzzles/' + request.args.get('puzzle')
    if not path.isfile(puzzle_name):
        return render_template('index.html', puzzles=puzzles)

    puzzle = nonogram.Nonogram(json.loads(open(puzzle_name).read()))
    solver.solver(puzzle)
    return render_template('solver.html', puzzle=puzzle)


if __name__ == '__main__':
    app.run()
