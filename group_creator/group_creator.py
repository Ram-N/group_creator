import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import random

from .cfg import *
from .candidate import Candidate
from .crossover import crossover
from .fitness import sort_pop_by_fitness, calc_pop_fitness, calc_candidate_fitness
from .output import (
    display_candidate_fitness,
    display_group_details,
    print_topper_details,
    display_results,
)


# ## Equitable Groups Creator
#
# # Genetic Algorithm Attempt
#
# - Form NUMSEED Random groups
# - Calculate fitness of each grouping, by scoring them against equitableness criteria
# - Keep the TOP_N fit groupings
# - Crossover to get better groups
# - Introduce some level of "mutation"
# - Stop when satisfied


def create_random_grouping(CLASS_SIZE, num_groups):
    """A Randomly shuffled list of lists of 1 through CLASS_SIZE"""

    if not isinstance(num_groups, int) or num_groups < 1:
        print(f"numgroups has to be a positive integer")
        return None

    nbase, nfloaters = CLASS_SIZE // num_groups, CLASS_SIZE % num_groups
    num_smaller_groups = num_groups - nfloaters
    team_counts = [nbase] * num_smaller_groups + [nbase + 1] * nfloaters

    grouping = []
    shuffled = random.sample(range(CLASS_SIZE), CLASS_SIZE)
    start = 0
    for t in team_counts:
        end = start + t
        grouping.append(shuffled[start:end])
        start = end

    return grouping


def seed_individuals(CLASS_SIZE, NUM_GROUPS, POPULATION_SIZE):
    population = {}
    for i in range(POPULATION_SIZE):

        grouping = create_random_grouping(CLASS_SIZE, NUM_GROUPS)
        population[i] = Candidate(ID=i, grouping=grouping)

    return population


def add_column_to_entity_info(entity_info, res_df, curr_population):

    entity_info["Group"] = 0
    winner = curr_population[res_df.index[0]]
    for idx, g in enumerate(winner):
        entity_info.loc[g, "Group"] = idx + 1

    print(entity_info)


def keep_top_n(curr_population, NUM_RETAIN):
    """Keep N individuals for seeding the next Generation

        Based on Fitness, we retain N, and discard pop_n minus N
    """

    sorted_pop = sort_pop_by_fitness(curr_population)  # List of k,cand tuples

    for cull, cand in sorted_pop[NUM_RETAIN:]:
        del curr_population[cull]

    return curr_population


if __name__ == "__main__":

    # Create a starter Population of Individuals
    # {Number: Candidate} dictionary
    curr_population = seed_individuals(CLASS_SIZE, NUM_GROUPS, POPULATION_SIZE)
    genID_start = POPULATION_SIZE
    num_offspring = POPULATION_SIZE - NUM_RETAIN  # needed in Crossover step

    gen = 0
    while gen < NUM_GENERATIONS:
        gen += 1
        # Generate the initial population
        # Compute fitness
        # REPEAT
        #     compute Fitness
        #     Selection
        #     Crossover
        #     Mutation
        # UNTIL population has converged

        # Main Loop for each Generation

        # FITNESS
        calc_pop_fitness(curr_population, ranked_attrs, entity_info)

        # SELECTION: Cull the low fitness individuals
        curr_population = keep_top_n(curr_population, NUM_RETAIN)
        print(f"Gen:{gen} Population has {len(curr_population)} survivors.")

        display_results(curr_population, topk=5)
        # Add offspring to current population
        offspring = crossover(curr_population, num_offspring, genID_start)
        genID_start += num_offspring

        # merge curr_population and offspring
        curr_population = {**curr_population, **offspring}
        print(
            f" Generation {gen} Population now has {len(curr_population)} candidates."
        )

    # add_column_to_entity_info(entity_info, res_df, curr_population)
