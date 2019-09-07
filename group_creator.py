import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import random

from candidate import Candidate
from crossover import crossover
from cfg import *
from fitness import *

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


def display_group_details(candidate, ranked_attrs, entity_info):

    for attr in ranked_attrs:
        unique_values = entity_info[attr].unique()
        for u in unique_values:
            print(f"{u}:\t", end=" ")
            for g in candidate.grouping:
                sdf = entity_info.loc[g]
                print((sdf[attr] == u).sum(), end=" ")
            print()

    print(f"Group Lengths:", end="")
    for g in candidate.grouping:
        print(len(g), end=" ")

    print()


def sort_pop_by_fitness(curr_population):
    return sorted(curr_population.items(), key=lambda x: x[1].fitness)


def keep_top_n(curr_population, NUM_RETAIN):
    """Keep N individuals for seeding the next Generation

        Based on Fitness, we retain N, and discard pop_n minus N
    """

    sorted_pop = sort_pop_by_fitness(curr_population)  # List of k,cand tuples

    for cull, cand in sorted_pop[NUM_RETAIN:]:
        del curr_population[cull]

    return curr_population


def display_candidate_fitness(candID, curr_population):
    print(f"Fitness for {candID}:  {curr_population[candID].fitness}\n")


def print_topper_details(topper_ID, curr_population, ranked_attrs, entity_info):
    print(f"THE Topper {topper_ID}")
    display_group_details(curr_population[topper_ID], ranked_attrs, entity_info)
    display_candidate_fitness(topper_ID, curr_population)


if __name__ == "__main__":

    # Create a starter Population of Individuals
    # {Number: Candidate} dictionary
    curr_population = seed_individuals(CLASS_SIZE, NUM_GROUPS, POPULATION_SIZE)
    gen_start = POPULATION_SIZE

    # Generate the initial population
    # Compute fitness
    # REPEAT
    #     Selection
    #     Crossover
    #     Mutation
    #     Compute fitness
    # UNTIL population has converged

    # Main Loop for each Generation

    # FITNESS
    calc_pop_fitness(curr_population, ranked_attrs, entity_info)

    # SELECTION: Cull the low fitness individuals
    curr_population = keep_top_n(curr_population, NUM_RETAIN)
    print(f"Population now has {len(curr_population)} survivors.")

    sorted_pop = sort_pop_by_fitness(curr_population)  # List of (ID,Cand)
    [print(cand) for ID, cand in sorted_pop[:5]]  # print the top 5
    print_topper_details(sorted_pop[0][0], curr_population, ranked_attrs, entity_info)

    num_offspring = POPULATION_SIZE - NUM_RETAIN  # needed in Crossover step

    # Add offspring to current population
    offspring = crossover(curr_population, num_offspring, gen_start)
    gen_start += num_offspring

    # add_column_to_entity_info(entity_info, res_df, curr_population)
