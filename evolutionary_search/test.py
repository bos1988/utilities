# -*- coding: utf-8 -*-
from time import perf_counter

from evo_searcher import EvoSearcher


# --------------------------------------------------


def fitness_function1(a):
    if sum(a) > len(a) * 0.6:
        return 0
    return sum([i * elem for i, elem in enumerate(a, 1)])


def fitness_function2(a):
    if sum(a) > len(a) * 0.2:
        return 0
    result = 0
    for i, elem in enumerate(a, 1):
        if i % 2 == 0:
            result += elem
        else:
            result -= elem
    return result


NUMBER_OF_GENES = 20  # 20
POSITIVE_SAMPLE_SIZE = int(NUMBER_OF_GENES / 2)
INITIAL_POPULATION_SIZE = 1000
NUMBER_OF_CHILDREN = 800
MUTATION_RATE = 0.1
NUMBER_OF_BEST = 10

searcher1 = EvoSearcher(
    fitness_function1,
    NUMBER_OF_GENES,
    positive_sample_size=POSITIVE_SAMPLE_SIZE,
    initial_population_size=INITIAL_POPULATION_SIZE,
    number_of_children=NUMBER_OF_CHILDREN,
    repeat_parents=False,
    mutation_rate=MUTATION_RATE,
    number_of_best=NUMBER_OF_BEST,
)
searcher2 = EvoSearcher(
    fitness_function2,
    NUMBER_OF_GENES,
    positive_sample_size=POSITIVE_SAMPLE_SIZE,
    initial_population_size=INITIAL_POPULATION_SIZE,
    number_of_children=NUMBER_OF_CHILDREN,
    repeat_parents=False,
    mutation_rate=MUTATION_RATE,
    number_of_best=NUMBER_OF_BEST,
)

if __name__ == "__main__":
    # t_0 = perf_counter()
    # brute_force_result = searcher1.run_brute_force()
    # t_res = perf_counter() - t_0
    # print("\n--------------------------------------------------")
    # print(f"brute_force_result:\n{searcher1.population.shape}")
    # print(f"brute_force_result:\n{brute_force_result[0]}")
    # print(f"brute_force_result:\n{brute_force_result[1]}")
    # print(f"Execution time = {t_res:.6f} sec")
    #
    # t_0 = perf_counter()
    # brute_force_result = searcher2.run_brute_force()
    # t_res = perf_counter() - t_0
    # print("\n--------------------------------------------------")
    # print(f"brute_force_result:\n{searcher2.population.shape}")
    # print(f"brute_force_result:\n{brute_force_result[0]}")
    # print(f"brute_force_result:\n{brute_force_result[1]}")
    # print(f"Execution time = {t_res:.6f} sec")

    print("=" * 20, end="\n\n")

    t_0 = perf_counter()
    # test_result = searcher1.run(50)
    test_result = searcher2.run(50)
    t_res = perf_counter() - t_0
    print("\n--------------------------------------------------")
    print(f"test_result:\n{test_result[0]}")
    print(f"test_result:\n{test_result[1]}")
    print(f"Execution time = {t_res:.6f} sec")

    print()
