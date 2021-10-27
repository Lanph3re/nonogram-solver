from os import path
import sys

from pstats import Stats
import cProfile
import json

sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
from src import genetic_algorithm_solver


def perf_test():
    puzzle = json.loads(open('../puzzles/qr.json').read())
    solver = genetic_algorithm_solver.GeneticAlgorithmSolver(puzzle, 20)
    solver.generate_solutions()
    return


profiler = cProfile.Profile()
profiler.runcall(perf_test)

stats = Stats(profiler)
stats.strip_dirs()
stats.sort_stats('cumulative')
stats.print_stats()
