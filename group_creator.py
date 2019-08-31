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
class Candidate:
    def __init__(self, ID, grouping):
        self.ID = ID
        self.grouping = grouping
        self.fitd = {}
        self.fitness = 0

    def __str__(self):
        istr = f"Candidate: {self.ID} \n"
        gstr = f"Grouping: {self.grouping} \n"
        fdstr = f"Fitness: {self.fitd} \n"
        fstr = f"Total Fitness: {self.fitness} \n"

        return istr + gstr + fdstr + fstr

    def display_grouping(self):
        gstr = f"Candidate:{self.ID} has {self.grouping}"
        return gstr


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


def seed_individuals(CLASS_SIZE, NUM_GROUPS, NUM_INDIVIDUALS):
    population = {}
    for i in range(NUM_INDIVIDUALS):

        grouping = create_random_grouping(CLASS_SIZE, NUM_GROUPS)
        population[i] = Candidate(ID=i, grouping=grouping)

    return population


def calc_candidate_fitness(candidate, attr, ideal_ratio, entity_info):
    """    Score each candidate in the population on one attribute

    In this case, a candidate is made up of "groups" or clusters
    We calculate how much each group composition varies from its ideal ratio

    :param candidate: one candidate (a grouping)
    :type: list
    :param attrib: one column of a data frame (CSV) to calculate fitness
    :type: string
    :param ideal_ratio: what should each group have of this attribute, ideally
    :type: float
    """

    candidate_fitness = 0
    for g in candidate.grouping:
        gsize = len(g)
        actual_ratio = {}
        for atype in entity_info[attr].value_counts().keys():
            actual_ratio[atype] = sum(entity_info.loc[g][attr] == atype) / gsize

        candidate_fitness += sum((pd.Series(actual_ratio) - ideal_ratio) ** 2)

    return candidate_fitness  # scalar


def calc_single_attr_pop_fitness(curr_population, attr, attr_importance, entity_info):
    """Calculate the fitness score of the entire pop, based on given attr

        Store it in the correct slot for that attr in the fitness dictionary
    """
    ideal_ratio = entity_info[attr].value_counts() / CLASS_SIZE

    for cand in range(len(curr_population)):
        curr_population[cand].fitd[attr] = calc_candidate_fitness(
            curr_population[cand], attr, ideal_ratio, entity_info
        )
        # add to total fitness
        curr_population[cand].fitness += curr_population[cand].fitd[attr]

    return curr_population


def calc_pop_fitness(curr_population, ranked_attrs, entity_info):

    ##fitness = {}
    # or idx in range(len(curr_population)):
    #    fitness[idx] = [BIG_VALUE] * len(ranked_attrs)

    for attr_importance, attr in enumerate(ranked_attrs):
        curr_population = calc_single_attr_pop_fitness(
            curr_population, attr, attr_importance, entity_info
        )

    return curr_population


def add_column_to_entity_info(entity_info, res_df, curr_population):

    entity_info["Group"] = 0
    winner = curr_population[res_df.index[0]]
    for idx, g in enumerate(winner):
        entity_info.loc[g, "Group"] = idx + 1

    print(entity_info)


def display_group(grouping, tanked_attrs, entity_info):

    for attr in ranked_attrs:
        unique_values = entity_info[attr].unique()
        for u in unique_values:
            print(f"{u}:\t", end=" ")
            for g in grouping:
                sdf = entity_info.loc[g]
                print((sdf[attr] == u).sum(), end=" ")
            print()

    for g in grouping:
        print(len(g), end=" ")

    print()


def keep_top_n(curr_population, NUM_RETAIN):
    """Keep N individuals for seeding the next Generation

        Based on Fitness, we retain N, and discard pop_n minus N
    """
    num_to_cull = NUM_INDIVIDUALS - NUM_RETAIN
    res_df = pd.Series(fitness).sort_values()

    # Get indices of the low fitness, to pop them off
    indivs_to_cull = res_df.tail(num_to_cull).index

    for k in indivs_to_cull:
        curr_population.pop(k, None)

    return curr_population


def sort_pop_by_fitness(curr_population):

    return sorted(curr_population.items(), key=lambda x: x[1].fitness)


def display_candidate_fitness(idx, curr_population, sorted_pop):

    fi = 0
    for f in sorted_pop[idx]:
        fi += f
    print(f"Fitness for {idx} {curr_population[idx]} is {fi}")


if __name__ == "__main__":

    # PARAMETERS
    NUM_INDIVIDUALS = 100
    NUM_RETAIN = 20
    MUTATION_FRAC = 0.05

    BIG_VALUE = 1000
    NUM_GROUPS = 4
    entity_info = pd.read_csv("data/raw/group_creation_sample1.csv")
    CLASS_SIZE = len(entity_info)
    print(f"Will divide {CLASS_SIZE} individuals into {NUM_GROUPS} groups")

    # Create a starter Population of Individuals
    curr_population = seed_individuals(CLASS_SIZE, NUM_GROUPS, NUM_INDIVIDUALS)

    # Assign fitness score to curr_population
    ranked_attrs = ["Gender", "Country"]

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
    curr_population = calc_pop_fitness(curr_population, ranked_attrs, entity_info)


    # SELECTION: Cull the low fitness individuals
    # curr_population = keep_top_n(curr_population, NUM_RETAIN)

    sorted_pop = sort_pop_by_fitness(curr_population)  # series

    for cand in sorted_pop[:20]:
        print(cand[1])
    # print(res_df.index)
    # topper_index = sorted_pop.index[0]  # list of lists
    # display_group(curr_population[topper_index], ranked_attrs, entity_info)
    # display_candidate_fitness(topper_index, curr_population, sorted_pop)

    # add_column_to_entity_info(entity_info, res_df, curr_population)
    # print(curr_population)
