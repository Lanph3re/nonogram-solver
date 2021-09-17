from math import exp
import random

from .nonogram import Nonogram


class Population:
    MUTATION_RATE = 0.001

    def __init__(self, nonogram):
        self.nonogram = nonogram
        self.fitness = 0

    @classmethod
    def random(cls, nonogram: Nonogram):
        for i in range(nonogram.get_height()):
            for j in range(nonogram.get_width()):
                nonogram.board[i][j] = random.getrandbits(1)

        return Population(nonogram)

    def evaluate_fitness(self):
        nonogram = self.nonogram
        fitness = 0

        for i in range(nonogram.get_height()):
            clues = nonogram.row_clues[i]
            num_clues = len(clues)
            blocks = nonogram.get_num_blocks_row(i)
            num_blocks = len(blocks)

            if num_blocks <= num_clues:
                fitness += num_blocks*19
                for k in range(num_blocks):
                    if blocks[k] != clues[k]:
                        fitness -= abs(blocks[k] - clues[k])*10

        for j in range(nonogram.get_width()):
            clues = nonogram.col_clues[j]
            num_clues = len(clues)
            blocks = nonogram.get_num_blocks_column(j)
            num_blocks = len(blocks)

            if num_blocks <= num_clues:
                fitness += num_blocks*19
                for k in range(num_blocks):
                    if blocks[k] != clues[k]:
                        fitness -= abs(blocks[k] - clues[k])*10

        return fitness

    @ classmethod
    def crossover(cls, puzzle, a: 'Population', b: 'Population'):
        new = Nonogram(puzzle)
        for i in range(a.nonogram.get_height()):
            for j in range(a.nonogram.get_width()):
                if random.getrandbits(1):
                    new.board[i][j] = a.nonogram.board[i][j]
                else:
                    new.board[i][j] = b.nonogram.board[i][j]

        return Population(new)

    def mutate(self):
        for i in range(self.nonogram.get_height()):
            for j in range(self.nonogram.get_height()):
                if random.random() <= self.MUTATION_RATE:
                    self.nonogram.board[i][j] ^= 1

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
