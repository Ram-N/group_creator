from .cfg import *
from .fitness import sort_pop_by_fitness


def display_candidate_fitness(candID, curr_population):
    print(f"Fitness for {candID}:  {curr_population[candID].fitness}\n")


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


def print_topper_details(topper_ID, curr_population):
    print(f"THE Topper {topper_ID}")
    display_group_details(curr_population[topper_ID], ranked_attrs, entity_info)
    display_candidate_fitness(topper_ID, curr_population)


def display_results(curr_population, topk):

    sorted_pop = sort_pop_by_fitness(curr_population)  # List of (ID,Cand)
    [print(cand) for ID, cand in sorted_pop[:topk]]  # print the top k candidates
    print_topper_details(sorted_pop[0][0], curr_population)
