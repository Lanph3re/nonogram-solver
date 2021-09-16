from . import nonogram


class GeneticAlgorithmSolver:
    POPULATION_SIZE = 1000

    def __init__(self, puzzle):
        self.puzzle = puzzle
        self.current_generation = []
        pass

    def _initialize_population(self):
        for _ in range(self.POPULATION_SIZE):
            self.current_generation.append(
                nonogram.Nonogram(self.puzzle).random())

    def _select(self):
        pass

    def _crossover(self):
        pass

    def _mutate(self):
        pass

    def _evaluate_fitness(self):
        pass

    def generate_solutions(self):
        self._initialize_population()
        return self.current_generation
