from itertools import permutations
from math import exp
import random
import copy

from .nonogram import Nonogram


class Population:
    CROSSOVER_RATE = 0.6
    SAMPLING_COLUMN_SIZE = 20

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
    def random(cls, nonogram: 'Nonogram'):
        for i in range(nonogram.get_height()):
            nonogram.board[i] = Population.get_satisfying_arr(
                nonogram.get_width(), nonogram.row_clues[i])

        return Population(nonogram)

    def update_fitness(self):
        nonogram = self.nonogram
        fitness = 0

        for j in range(nonogram.get_width()):
            clue = nonogram.col_clues[j]

            max_fitness_column = 0
            possible_columns = [
                self.get_satisfying_arr(nonogram.get_height(), clue)
                for _ in range(self.SAMPLING_COLUMN_SIZE)
            ]

            column = nonogram.get_column(j)
            for possible_column in possible_columns:
                fitness_column = sum([
                    10 if column[k] == possible_column[k] else 0
                    for k in range(nonogram.get_height())
                ])
                fitness_column /= nonogram.get_height()
                max_fitness_column = max(max_fitness_column, fitness_column)

            fitness += max_fitness_column

        self.fitness = fitness / nonogram.get_width()
        return self

    @classmethod
    def crossover(cls, puzzle, a: 'Population', b: 'Population'):
        if random.random() <= cls.CROSSOVER_RATE:
            point = random.randint(0, a.nonogram.get_height() - 1)
            a.nonogram.board[point:], b.nonogram.board[point:] = \
                b.nonogram.board[point:], a.nonogram.board[point:]

        return a, b

    def mutate(self, mutation_rate):
        for _ in range(random.randint(0, 3)):
            if random.random() <= mutation_rate:
                i = random.randint(0, self.nonogram.get_height() - 1)
                self.nonogram.board[i] = Population.get_satisfying_arr(
                    self.nonogram.get_width(), self.nonogram.row_clues[i])

        return self


class GeneticAlgorithmSolver:
    POPULATION_SIZE = 100
    MAX_GENERATION = 1000
    LINEAR_RANKING_PARAMETER = 1
    NUM_ELITES = 2

    def __init__(self, puzzle):
        self.puzzle = puzzle
        self.current_generation = []
        self.generation_cnt = 0
        self.max_fitness = 0
        self.mutation_rate = 0.001

    def _initialize_population(self):
        for _ in range(self.POPULATION_SIZE):
            population = Population.random(Nonogram(self.puzzle))
            self.current_generation.append(population.update_fitness())

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

    def generate_solutions(self):
        self._initialize_population()

        while True:
            next_generation = copy.deepcopy(
                self.current_generation[-self.NUM_ELITES:])
            while len(next_generation) < self.POPULATION_SIZE:
                a, b = copy.deepcopy(self._select())
                a, b = Population.crossover(self.puzzle, a, b)
                a = a.mutate(self.mutation_rate)
                b = b.mutate(self.mutation_rate)
                a.update_fitness()
                b.update_fitness()
                next_generation.extend([a, b])

            self.current_generation = \
                sorted(next_generation, key=lambda x: x.fitness)

            fitness_delta = abs(self.max_fitness -
                                self.current_generation[-1].fitness)
            if fitness_delta < 0.001:
                self.mutation_rate = min(self.mutation_rate + 0.001, 1)
            else:
                self.mutation_rate = max(self.mutation_rate - 0.001, 0)

            self.max_fitness = max(self.max_fitness,
                                   self.current_generation[-1].fitness)
            self.generation_cnt += 1

        return self.current_generation

    def get_fittest_population(self):
        fittest = self.current_generation[-1]
        return fittest, fittest.fitness
