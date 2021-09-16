import json
from os import listdir, path

from flask import Flask, render_template, request

from src.nonogram import Nonogram
from src.solver import GeneticAlgorithmSolver


PUZZLE_DIR = 'puzzles'

app = Flask(__name__)
puzzles = sorted(listdir(PUZZLE_DIR))


@app.route("/")
def puzzle_list():
    return render_template('index.html', puzzles=puzzles)


@app.route('/solver')
def nonogram_solver():
    puzzle_name = path.join(PUZZLE_DIR, request.args.get('puzzle'))
    if not path.isfile(puzzle_name):
        return render_template('index.html', puzzles=puzzles)

    puzzle = json.loads(open(puzzle_name).read())
    solver = GeneticAlgorithmSolver(puzzle)
    solutions = solver.generate_solutions()

    return render_template('solver.html', puzzle=solutions[0])


if __name__ == '__main__':
    app.run()
