from itertools import permutations
from math import exp
import random
import copy

from .nonogram import Nonogram
from .rule_based_solver import RuleBasedSolver


class Population:
    CROSSOVER_RATE = 0.6

    def __init__(self, nonogram):
        self.nonogram = nonogram
        self.fitness = 0

    @classmethod
    def get_satisfying_arr(cls, size, clue):
        spaces = [1 for _ in range(len(clue) + 1)]
        spaces[0], spaces[-1] = 0, 0

        while sum(spaces) + sum(clue) < size:
            spaces[random.randint(0, len(spaces) - 1)] += 1

        arr = []
        for i in range(len(clue)):
            arr += [0 for _ in range(spaces[i])]
            arr += [1 for _ in range(clue[i])]
        arr += [0 for _ in range(spaces[-1])]

        return arr

    @classmethod
    def is_minimum(cls, nonogram: 'Nonogram', arr, min_arr):
        for j in range(nonogram.get_width()):
            if min_arr[j] == nonogram.BOX and arr[j] != nonogram.BOX:
                return False
        return True

    @classmethod
    def random(cls, nonogram: 'Nonogram', min_solution):
        for i in range(nonogram.get_height()):
            while True:
                row = Population.get_satisfying_arr(nonogram.get_width(),
                                                    nonogram.row_clues[i])
                if cls.is_minimum(nonogram, row, min_solution[i]):
                    break
            nonogram.board[i] = row

        return Population(nonogram)

    def update_fitness(self, column_pool):
        nonogram = self.nonogram
        fitness = 0

        for j in range(nonogram.get_width()):
            max_fitness_column = 0
            column = nonogram.get_column(j)
            for possible_column in column_pool[j]:
                fitness_column = 0
                for k in range(nonogram.get_height()):
                    if column[k] == possible_column[k]:
                        fitness_column += 10
                fitness_column /= nonogram.get_height()
                max_fitness_column = max(max_fitness_column, fitness_column)

            fitness += max_fitness_column

        self.fitness = fitness / nonogram.get_width()
        return self

    @classmethod
    def crossover(cls, a: 'Population', b: 'Population'):
        if random.random() <= cls.CROSSOVER_RATE:
            point = random.randint(0, a.nonogram.get_height() - 1)
            a.nonogram.board[point:], b.nonogram.board[point:] = \
                b.nonogram.board[point:], a.nonogram.board[point:]

        return a, b

    def mutate(self, mutation_rate):
        for _ in range(random.randint(1, 3)):
            if random.random() <= mutation_rate:
                i = random.randint(0, self.nonogram.get_height() - 1)
                self.nonogram.board[i] = Population.get_satisfying_arr(
                    self.nonogram.get_width(), self.nonogram.row_clues[i])

        return self


class GeneticAlgorithmSolver:
    POPULATION_SIZE = 100
    LINEAR_RANKING_PARAMETER = 1
    NUM_ELITES = 2

    def __init__(self, puzzle, max_generation=1000):
        self.is_running = True
        self.puzzle = puzzle
        self.nonogram = Nonogram(puzzle)
        self.current_generation = []
        self.max_generation = max_generation
        self.generation = 0
        self.max_fitness = 0
        self.mutation_rate = 0.2
        self.min_solution = \
            RuleBasedSolver(puzzle).generate_solution().board
        self.column_pool = [[
            Population.get_satisfying_arr(self.nonogram.get_height(),
                                          self.nonogram.col_clues[i])
            for _ in range(self.nonogram.get_height() * 2)
        ] for i in range(self.nonogram.get_width())]

    def _initialize_population(self):
        self.current_generation = [
            Population.random(Nonogram(self.puzzle), self.min_solution)
            for _ in range(self.POPULATION_SIZE)
        ]
        for population in self.current_generation:
            population.update_fitness(self.column_pool)

    def _exponential_ranking_select(self):
        weights = [1 - exp(-x) for x in range(1, self.POPULATION_SIZE + 1)]
        denominator = sum(weights)
        return random.choices(population=self.current_generation,
                              weights=[x / denominator for x in weights],
                              k=2)

    def _linear_ranking_select(self):
        weights = [
            ((2 - self.LINEAR_RANKING_PARAMETER) / self.POPULATION_SIZE) +
            (i * (self.LINEAR_RANKING_PARAMETER - 1) /
             sum(range(0, self.POPULATION_SIZE)))
            for i in range(0, self.POPULATION_SIZE)
        ]
        return random.choices(population=self.current_generation,
                              weights=weights,
                              k=2)

    def _select(self):
        return self._linear_ranking_select()

    def _update_mutation_rate(self):
        fitness_delta = abs(self.max_fitness -
                            self.current_generation[-1].fitness)
        if fitness_delta < 0.001:
            self.mutation_rate = min(self.mutation_rate + 0.001, 1)
        else:
            self.mutation_rate /= 2

        self.max_fitness = max(self.max_fitness,
                               self.current_generation[-1].fitness)

    def generate_solutions(self):
        self._initialize_population()
        while self.is_running \
                and self.generation < self.max_generation:
            next_generation = \
                copy.deepcopy(self.current_generation[-self.NUM_ELITES:])

            while len(next_generation) < self.POPULATION_SIZE:
                a, b = copy.deepcopy(self._select())
                a, b = Population.crossover(a, b)
                a = a.mutate(self.mutation_rate).update_fitness(
                    self.column_pool)
                b = b.mutate(self.mutation_rate).update_fitness(
                    self.column_pool)
                next_generation += [a, b]

            self.current_generation = \
                sorted(next_generation, key=lambda x: x.fitness)
            self._update_mutation_rate()
            self.generation += 1

        return self.current_generation

    def get_fittest_population(self):
        if len(self.current_generation) == 0:
            return 0, Nonogram(self.puzzle), 0, True

        fittest = self.current_generation[-1]
        is_running = self.generation != self.max_generation
        return self.generation, fittest, fittest.fitness, is_running
