import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import random


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


def create_random_indiv(CLASS_SIZE, num_groups):

    if not isinstance(num_groups, int) or num_groups < 1:
        print(f"numgroups has to be a positive integer")
        return None

    nbase, nfloaters = CLASS_SIZE // num_groups, CLASS_SIZE % num_groups
    num_smaller_groups = num_groups - nfloaters
    team_counts = [nbase] * num_smaller_groups + [nbase + 1] * nfloaters

    groups = []
    shuffled = random.sample(range(CLASS_SIZE), CLASS_SIZE)
    start = 0
    for t in team_counts:
        end = start + t
        groups.append(shuffled[start:end])
        start = end
    return groups


def calc_indiv_fitness(indiv, attr, ideal_ratio):
    """    Score each individual in the population on one attribute

    In this case, an indiv is made up of "groups" or clusters
    We calculate how much each group composition varies from its ideal ratio

    :param indiv: one individual (a grouping)
    :type: list
    :param attrib: one column of a data frame (CSV) to calculate fitness
    :type: string
    :param ideal_ratio: what should each group have of this attribute, ideally
    :type: float
    """

    indiv_fitness = 0
    for g in indiv:
        gsize = len(g)
        actual_ratio = {}
        for atype in df[attr].value_counts().keys():
            actual_ratio[atype] = sum(df.loc[g][attr] == atype) / gsize

        indiv_fitness += sum((pd.Series(actual_ratio) - ideal_ratio) ** 2)

    return indiv_fitness


def display_group(grouping, attr, df):

    print(df[attr].value_counts())
    for g in grouping:
        sdf = df.loc[g]
        print(sdf[attr].value_counts())
        print(len(g))


def seed_individuals(CLASS_SIZE, NUM_GROUPS, NUM_RANDOM_INDIVIDUALS):
    population = {}
    for i in range(NUM_RANDOM_INDIVIDUALS):
        population[i] = create_random_indiv(CLASS_SIZE, NUM_GROUPS)
    return population


def calc_pop_fitness_for_attr(curr_population, attr, df):
    """Calculate the fitness score of the entire pop, based on given attr
    """
    ideal_ratio = df[attr].value_counts() / CLASS_SIZE

    fitness = {}
    for idx in range(NUM_RANDOM_INDIVIDUALS):
        fitness[idx] = calc_indiv_fitness(curr_population[idx], attr, ideal_ratio)
    return fitness


def assign_group_column(df, res_df, curr_population):

    df["Group"] = 0
    winner = curr_population[res_df.index[0]]
    for idx, g in enumerate(winner):
        df.loc[g, "Group"] = idx + 1

    print(df)


if __name__ == "__main__":

    # PARAMETERS
    NUM_RANDOM_INDIVIDUALS = 100
    KEEP_TOP = 20
    MUTATION_FRAC = 0.05

    NUM_GROUPS = 4
    df = pd.read_csv("../data/form_groups.csv")
    CLASS_SIZE = len(df)
    print(f"Will divide {CLASS_SIZE} individuals into {NUM_GROUPS} groups")

    # Create a starter Population of Individuals
    curr_population = seed_individuals(CLASS_SIZE, NUM_GROUPS, NUM_RANDOM_INDIVIDUALS)

    # Assign fitness score to curr_population
    attr = "Gender"
    attr = "Country"

    num_unique = df[attr].nunique()

    # for attr_type in range(num_unique):
    #     df[attr].value_counts()[attr_type] / CLASS_SIZE

    fitness = calc_pop_fitness_for_attr(curr_population, attr, df)

    res_df = pd.Series(fitness).sort_values().head(20)

    print(fitness)
    display_group(curr_population[res_df.index[0]], attr, df)

    assign_group_column(df, res_df, curr_population)
