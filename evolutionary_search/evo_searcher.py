# -*- coding: utf-8 -*-
from itertools import product
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
        fitness_function: Callable = None,
        number_of_genes: int = 1,
        initial_population_size: int = 1,
        number_of_children: int = 0,
        repeat_parents: bool = False,
        mutation_rate: float = 0,
        number_of_best: int = 1,
    ) -> None:
        """
        :param fitness_function: function for calculating the score
        """
        if mutation_rate > 1:
            raise ValueError("mutation_rate must be between 0 and 1")

        self.fitness_function = np.vectorize(fitness_function, signature="(n)->()")
        self.number_of_genes = number_of_genes
        self.initial_population_size = initial_population_size
        self.number_of_children = number_of_children
        self.repeat_parents = repeat_parents
        self.mutation_rate = mutation_rate
        self.number_of_best = number_of_best

        self.reset_to_zero()
        self.fitnesses = np.empty(0)
        self.population = np.empty(0)

    def run(self, number_of_generations: int = 0) -> tuple[np.ndarray, np.ndarray]:
        self.reset_to_zero()
        self.generate_initial_population()
        self.update_best()

        for _generation in range(number_of_generations):
            print("DEBUG: _generation: ", _generation)
            print("DEBUG:", self.best_fitness)
            # print("DEBUG:", self.best_chromosomes)
            # print("DEBUG:", self.fitnesses)
            # print("DEBUG:\n", self.population)
            # print(">>>")

            chosen_parents = self.parent_selection()
            # print("DEBUG: chosen_parents:\n", chosen_parents)

            children = self.reproduce_children(chosen_parents)
            # print("DEBUG: children:\n", children)

            children = self.mutate_children(children)
            # print("DEBUG: mutated children:\n", children)

            self.update_generation(children)

            # print("\n>>>>>>>>>\n>>>>>>>>>\n")

        return self.best_fitness, self.best_chromosomes

    def reset_to_zero(self):
        self.best_fitness = np.zeros(self.number_of_best, dtype=int)
        self.best_chromosomes = np.zeros(
            (self.number_of_best, self.number_of_genes), dtype=int
        )

    def generate_initial_population(self) -> None:
        self.population = np.random.randint(
            2, size=(self.initial_population_size, self.number_of_genes)
        )
        self.calculate_population_fitness()

    def calculate_population_fitness(self) -> None:
        self.fitnesses = self.fitness_function(self.population)

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
        self.best_fitness = np.concatenate([self.fitnesses[order], self.best_fitness])
        self.best_chromosomes = np.concatenate(
            [self.population[order], self.best_chromosomes]
        )

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
            p=self.fitnesses.argsort().argsort() ** 2
            / sum(np.arange(len_population) ** 2),
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

    def mutate_children(self, children: np.ndarray) -> np.ndarray:
        return np.where(
            np.random.random(children.shape) < self.mutation_rate,
            1 - children,
            children,
        )

    def update_generation(self, children):
        children_fitness = self.fitness_function(children)
        self.population = np.concatenate([self.population, children])
        self.fitnesses = np.concatenate([self.fitnesses, children_fitness])

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
