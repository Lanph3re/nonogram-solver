from math import exp
import random

from .nonogram import Nonogram


class Population:
    MUTATION_RATE = 0.1

    def __init__(self, nonogram):
        self.nonogram = nonogram
        self.fitness = 0

    @classmethod
    def get_satisfying_arr(cls, size, clue):
        spaces = [1 for _ in range(len(clue) + 1)]
        spaces[0] = 0
        spaces[-1] = 0
        while sum(spaces) < size - sum(clue):
            spaces[random.randint(0, len(spaces) - 1)] += 1

        arr = []
        for i in range(len(clue)):
            arr.extend([0 for _ in range(spaces[i])] +
                       [1 for _ in range(clue[i])])
        arr.extend([0 for _ in range(spaces[-1])])

        return arr

    @classmethod
    def random(cls, nonogram: Nonogram):
        for i in range(nonogram.get_height()):
            nonogram.board[i] = Population.get_satisfying_arr(
                nonogram.get_width(), nonogram.row_clues[i])

        return Population(nonogram)

    def evaluate_fitness(self):
        nonogram = self.nonogram
        fitness = 0

        for j in range(nonogram.get_width()):
            clues = nonogram.col_clues[j]
            blocks = nonogram.get_num_blocks_column(j)

            if len(blocks) > len(clues):
                fitness -= 100

            for k in range(min(len(blocks), len(clues))):
                fitness -= abs(blocks[k] - clues[k])*30

        return fitness

    @ classmethod
    def crossover(cls, puzzle, a: 'Population', b: 'Population'):
        new = Nonogram(puzzle)
        for i in range(a.nonogram.get_height()):
            if random.getrandbits(1):
                new.board[i] = a.nonogram.board[i]
            else:
                new.board[i] = b.nonogram.board[i]

        return Population(new)

    def mutate(self):
        if random.random() <= self.MUTATION_RATE:
            i = random.randint(0, self.nonogram.get_height() - 1)
            self.nonogram.board[i] = Population.get_satisfying_arr(
                self.nonogram.get_width(), self.nonogram.row_clues[i])

        if random.random() <= self.MUTATION_RATE:
            i = random.randint(0, self.nonogram.get_height() - 1)
            j = random.randint(0, self.nonogram.get_height() - 1)
            if i > j:
                i, j = j, i

            while i < j:
                self.nonogram.board[i] = Population.get_satisfying_arr(
                    self.nonogram.get_width(), self.nonogram.row_clues[i])
                i += 1

        return self


class GeneticAlgorithmSolver:
    POPULATION_SIZE = 100
    LINEAR_RANKING_PARAMETER = 1
    MAX_GENERATION = 1000
    NUM_ELITES = 4

    def __init__(self, puzzle):
        self.puzzle = puzzle
        self.current_generation = []
        self.generation_cnt = 0

    def _initialize_population(self):
        for _ in range(self.POPULATION_SIZE):
            population = Population.random(Nonogram(self.puzzle))
            population.fitness = population.evaluate_fitness()
            self.current_generation.append(population)

    def _exponential_ranking_select(self):
        weights = [i for i in range(1, self.POPULATION_SIZE + 1)]
        weights = [1 - exp(-x) for x in weights]
        denominator = sum(weights)
        return random.choices(
            population=self.current_generation,
            weights=[x / denominator for x in weights],
            k=2)

    def _select(self):
        weights = [i for i in range(0, self.POPULATION_SIZE)]
        weights = [(2 - self.LINEAR_RANKING_PARAMETER) / self.POPULATION_SIZE +
                   i*(self.LINEAR_RANKING_PARAMETER - 1) / sum(weights) for i in weights]
        return random.choices(
            population=self.current_generation,
            weights=weights,
            k=2)

    def generate_solutions(self):
        self._initialize_population()
        while True:
            next_generation = []
            next_generation.extend(self.current_generation[-self.NUM_ELITES:])
            for _ in range(self.POPULATION_SIZE - self.NUM_ELITES):
                a, b = self._select()
                new = Population.crossover(self.puzzle, a, b).mutate()
                new.fitness = new.evaluate_fitness()
                next_generation.append(new)

            self.current_generation = sorted(
                next_generation, key=lambda x: x.fitness)
            self.generation_cnt += 1

        return self.current_generation

    def get_fittest_population(self):
        return self.current_generation[-1]
