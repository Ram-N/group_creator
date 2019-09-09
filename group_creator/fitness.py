import pandas as pd

from .cfg import ranked_attrs


def sort_pop_by_fitness(curr_population):
    return sorted(curr_population.items(), key=lambda x: x[1].fitness)


def calc_candidate_fitness(candidate, ranked_attrs, entity_info, CLASS_SIZE):
    """    Score one candidate on all attributes

    In this case, a candidate is made up of "groups" or clusters
    We calculate how much each group composition varies from its ideal ratio

    :param candidate: one candidate (a grouping)
    :type: list
    :param attrib: one column of a data frame (CSV) to calculate fitness
    :type: string
    :param ideal_ratio: what should each group have of this attribute, ideally
    :type: float
    """

    for attr_importance, attr in enumerate(ranked_attrs):
        ideal_ratio = entity_info[attr].value_counts() / CLASS_SIZE

        attr_fitness = 0
        for g in candidate.grouping:
            gsize = len(g)
            actual_ratio = {}
            for atype in entity_info[attr].value_counts().keys():
                actual_ratio[atype] = sum(entity_info.loc[g][attr] == atype) / gsize

            attr_fitness += sum((pd.Series(actual_ratio) - ideal_ratio) ** 2)

        candidate.fitd[attr] = attr_fitness
        candidate.fitness += attr_fitness  # add to total fitness


def calc_pop_fitness(curr_population, ranked_attrs, entity_info):

    for cand in list(curr_population.keys()):
        calc_candidate_fitness(curr_population[cand], ranked_attrs, entity_info)

