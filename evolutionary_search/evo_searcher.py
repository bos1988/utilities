# -*- coding: utf-8 -*-
from itertools import product
from multiprocessing import Pool
from typing import Callable

import numpy as np


class EvoSearcher:
    """
    The theory of evolution suggests that organisms evolve through reproduction by producing children of mixed genes
    from their parents; and given the fitness of these individuals in their environment,
    stronger individuals have a higher likelihood of survival.

    Binary encoding is used to encode chromosomes.
    """

    def __init__(
        self,
        fitness_function: Callable,
        number_of_genes: int,
        positive_sample_size: int = 5,
        initial_population_size: int = 1,
        number_of_children: int = 0,
        repeat_parents: bool = False,
        mutation_rate: float = 0,
        randomize_mutation_rate: bool = False,
        mutate_parents: bool = False,
        number_of_best: int = 1,
        n_jobs: int = 1,
    ) -> None:
        """
        :param fitness_function: function for calculating the score
        """
        if mutation_rate > 1:
            raise ValueError("mutation_rate must be between 0 and 1")

        self.fitness_function = fitness_function
        self.number_of_genes = number_of_genes
        self.positive_sample_size = positive_sample_size
        self.initial_population_size = initial_population_size
        self.number_of_children = number_of_children
        self.repeat_parents = repeat_parents
        self.mutation_rate = mutation_rate
        self.randomize_mutation_rate = randomize_mutation_rate
        self.mutate_parents = mutate_parents
        self.number_of_best = number_of_best
        self.n_jobs = n_jobs

        self.reset_to_zero()
        self.fitnesses = np.empty(0)
        self.population = np.empty(0)
        self.best_fitness = np.zeros(number_of_best)
        self.best_chromosomes = np.zeros((number_of_best, number_of_genes))

    def run(self, number_of_generations: int = 0) -> tuple[np.ndarray, np.ndarray]:
        self.reset_to_zero()
        self.generate_initial_population()
        self.update_best()
        print("DEBUG:", self.best_fitness[:10], self.best_fitness.sum())

        for _generation in range(number_of_generations):
            print("DEBUG: _generation: ", _generation)

            chosen_parents = self.parent_selection()
            children = self.reproduce_children(chosen_parents)
            children = self.mutate(children)
            self.update_generation(children)

            if self.mutate_parents:
                self.update_generation(self.mutate(chosen_parents))

            self.update_best()
            print("DEBUG:", self.best_fitness[:10], self.best_fitness.sum())

        return self.best_fitness, self.best_chromosomes

    def calculate_fitness_function(self, array):
        with Pool(self.n_jobs) as pool:
            res = pool.map(self.fitness_function, array)
        return np.array(res)

    def reset_to_zero(self):
        self.best_fitness = np.zeros(self.number_of_best, dtype=int)
        self.best_chromosomes = np.zeros(
            (self.number_of_best, self.number_of_genes), dtype=int
        )

    def generate_initial_population(self) -> None:
        # self.population = np.random.randint(2, size=(self.initial_population_size, self.number_of_genes))
        population = []
        for _ in range(self.initial_population_size):
            sample = np.ones(self.positive_sample_size, dtype=int)
            sample.resize(self.number_of_genes)  # fill zeros
            np.random.shuffle(sample)  # random position
            population.append(sample)
        self.population = np.vstack(population)
        self.calculate_population_fitness()

    def calculate_population_fitness(self) -> None:
        self.fitnesses = self.calculate_fitness_function(self.population)

    def sort_population(self):
        order = np.flip(self.fitnesses.argsort())
        self.fitnesses = self.fitnesses[order]
        self.population = self.population[order]

    def update_best(self) -> None:
        if len(self.population) != len(self.fitnesses):
            raise ValueError(
                "Length of 'fitnesses' is not equal to length of 'population'"
            )

        order = np.flip(self.fitnesses.argsort())[: self.number_of_best]
        self.best_chromosomes = np.unique(
            np.concatenate([self.population[order], self.best_chromosomes]), axis=0
        )
        self.best_fitness = self.calculate_fitness_function(self.best_chromosomes)

        order_best = np.flip(self.best_fitness.argsort())[: self.number_of_best]
        self.best_fitness = self.best_fitness[order_best]
        self.best_chromosomes = self.best_chromosomes[order_best]

    def parent_selection(self) -> np.ndarray:
        # Implemented "Rank selection" + squaring
        # (there is also "Roulette wheel selection", "Tournament selection" and "Elitism selection")
        # TODO add factory class Selector

        len_population = len(self.population)
        parents_indexes = np.random.choice(
            len_population,
            size=self.number_of_children,
            replace=self.repeat_parents,
            p=self.fitnesses.argsort().argsort() / sum(np.arange(len_population)),
            # p=self.fitnesses.argsort().argsort()**2 / sum(np.arange(len_population)**2),
        )
        # print(f"DEBUG: selected parents {parents_indexes} from {self.fitnesses.argsort()} (right - best)")
        return self.population[parents_indexes]

    def reproduce_children(self, parents: np.ndarray) -> np.ndarray:
        children = []
        for parent_index in range(0, len(parents) - 1, 2):
            children.extend(
                self.crossover(
                    parents[parent_index],
                    parents[parent_index + 1],
                )
            )
        return np.vstack(children)

    def crossover(
        self, parent_a: np.ndarray, parent_b: np.ndarray
    ) -> tuple[np.ndarray, np.ndarray]:
        # Implemented "Uniform crossover"
        # (there is also "Single-point crossover" and "Two-point crossover")
        # TODO add factory class Crossover

        # prepare mask:
        mask = np.ones(self.number_of_genes // 2, dtype=int)  # exactly half of gens
        mask.resize(self.number_of_genes)  # fill zeros
        np.random.shuffle(mask)  # random position

        child_a = np.where(mask, parent_a, parent_b)
        child_b = np.where(mask, parent_b, parent_a)
        return child_a, child_b

    def mutate(self, individuals: np.ndarray) -> np.ndarray:
        mutation_prob = np.random.random() if self.randomize_mutation_rate else 1
        return np.where(
            np.random.random(individuals.shape) < self.mutation_rate * mutation_prob,
            1 - individuals,
            individuals,
        )

    def update_generation(self, new_individuals):
        new_fitness = self.calculate_fitness_function(new_individuals)
        self.population = np.concatenate([self.population, new_individuals])
        self.fitnesses = np.concatenate([self.fitnesses, new_fitness])

        self.sort_population()
        self.population = self.population[: self.initial_population_size]
        self.fitnesses = self.fitnesses[: self.initial_population_size]

    def run_brute_force(self) -> tuple[np.ndarray, np.ndarray]:
        """
        Run the brute force algorithm

        Binary encoding is used to encode chromosomes.

        :return: sorted scores, sorted individuals
        """

        self.population = np.array(list(product([0, 1], repeat=self.number_of_genes)))
        self.calculate_population_fitness()
        self.sort_population()

        return (
            self.fitnesses[: self.number_of_best],
            self.population[: self.number_of_best],
        )
