import json
import os
import threading

from flask import Flask, render_template, request, session
from flask_socketio import SocketIO, emit

from src.nonogram import Nonogram
from src.solver import GeneticAlgorithmSolver, Population

PUZZLE_DIR = 'puzzles'

app = Flask(__name__)
app.secret_key = os.urandom(32)
socketio = SocketIO(app)

puzzles = sorted(os.listdir(PUZZLE_DIR))
solvers = dict()


@app.route("/")
def puzzle_list():
    return render_template('index.html', puzzles=puzzles)


@app.route('/solver')
def nonogram_solver():
    puzzle_name = os.path.join(PUZZLE_DIR, request.args.get('puzzle'))
    if not os.path.isfile(puzzle_name):
        return render_template('index.html', puzzles=puzzles)

    puzzle = json.loads(open(puzzle_name).read())
    session['user'] = os.urandom(32)
    solvers[session['user']] = GeneticAlgorithmSolver(puzzle)
    solver_thread = \
        threading.Thread(
            target=lambda solvers, id: solvers[id].generate_solutions(),
            args=[solvers, session['user']])
    solver_thread.setDaemon(True)
    solver_thread.start()

    test = Population.random(Nonogram(puzzle))
    return render_template('solver.html', puzzle=test.nonogram)


@socketio.on('connect')
def run_solver():
    if 'user' not in session:
        emit('on_connect', {})
    else:
        emit('on_connect', {'data': 'Running genetic algorithm solver..'})


@socketio.on('update')
def update_board(data):
    if 'user' not in session:
        emit('on_update', {})
    else:
        fittest, fitness = solvers[session['user']].get_fittest_population()
        emit('on_update', {
            'board': fittest.nonogram.board,
            'fitness': fitness
        })


if __name__ == '__main__':
    socketio.run(app)
