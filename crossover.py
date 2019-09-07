import random

from candidate import Candidate
from cfg import *
from fitness import *


def init_new(grouping1):
    numg = len(grouping1)
    new = []  # create placeholders for each group inside new candidate
    for _ in range(numg):
        new.append([])
    new_slots = [len(x) for x in grouping1]
    return new, new_slots


def p1_contribution(grouping1, new, new_slots, placed):

    numg = len(grouping1)
    numg1 = numg // 2
    g1_retain = random.sample(range(numg), numg1)
    # print(g1_retain)

    for g in g1_retain:
        new[g] = grouping1[g]
        new_slots[g] = 0  # all slots filled up
        for indiv in grouping1[g]:
            placed.append(indiv)

    return new, new_slots, placed


def calc_p2nums_tbplaced_by_g(grouping2, placed):
    p2_nums_available = []
    for g2 in grouping2:
        num_looking = 0
        for indiv in g2:
            if indiv not in placed:
                num_looking += 1
        p2_nums_available.append(num_looking)

    return p2_nums_available


def add_to_1_group(new, new_slots, groupnum_to_append, p2_indivs, placed):

    # if anyone in p2_indivs in not placed, add to groupnum_to_append
    for indiv in p2_indivs:
        # indiv has not been place & there are slots in this groupnum_to_append
        if indiv not in placed and (new_slots[groupnum_to_append] > 0):
            new[groupnum_to_append].append(indiv)
            placed.append(indiv)
            new_slots[groupnum_to_append] -= 1
    return new, new_slots, placed


def xfer_from_best_p2_group(
    new, new_slots, groupnum_to_append, grouping2, p2_nums_available, placed, split_flag
):

    time_to_split = False
    num_needed = new_slots[groupnum_to_append]

    while num_needed != 0:
        for p2_gnum, na in enumerate(p2_nums_available):
            # print(f'{na} available in P2 Group {p2_gnum} num needed: {num_needed}')

            if split_flag:
                if na == num_needed:
                    new, new_slots, placed = add_to_1_group(
                        new, new_slots, groupnum_to_append, grouping2[p2_gnum], placed
                    )

                    return new, new_slots, placed, time_to_split
            else:
                if na > num_needed:  # splitting
                    new, new_slots, placed = add_to_1_group(
                        new, new_slots, groupnum_to_append, grouping2[p2_gnum], placed
                    )
                    # print('Done splitting')
                    return new, new_slots, placed, time_to_split

        num_needed -= 1  # decrement

    time_to_split = True
    return new, new_slots, placed, time_to_split


def add_to_new(
    new, new_slots, groupnum_to_append, grouping2, p2_nums_available, placed
):

    # print(f'New group {groupnum_to_append} has {new_slots[groupnum_to_append]} slots')

    # Go through each grp in p2.
    # There is a particular new group that we can to add to.
    # if the WANT (of new) is >= AVAILABLE...place all the individuals

    new, new_slots, placed, time_to_split = xfer_from_best_p2_group(
        new,
        new_slots,
        groupnum_to_append,
        grouping2,
        p2_nums_available,
        placed,
        split_flag=False,
    )

    if time_to_split:  # allow P2 group to be split
        new, new_slots, placed, time_to_split = xfer_from_best_p2_group(
            new,
            new_slots,
            groupnum_to_append,
            grouping2,
            p2_nums_available,
            placed,
            split_flag=True,
        )  # splitting allowed

    return new, new_slots, placed


def mate(cand1, cand2):
    """CROSSOVER between two Candidates

    :param cand1: one candidate (which is a grouping)
    :type: Candidate
    :param cand1: one candidate (which is a grouping)
    :type: Candidate
    :rtype: Candidate
        
    """

    grouping1 = cand1.grouping
    grouping2 = cand2.grouping

    DEBUG = False
    placed = []

    new, new_slots = init_new(grouping1)
    # print(placed)
    new, new_slots, placed = p1_contribution(grouping1, new, new_slots, placed)
    # print(placed)
    # print(new)

    # The rest of the groups come from the other parent
    loops = 0
    while sum(new_slots) or loops == 10:
        p2_nums_available = calc_p2nums_tbplaced_by_g(grouping2, placed)
        # print(f'p2 groups can give {p2_nums_available} to new')

        # find which groupnum inside new has most openings. Let's fill that first
        new_gnum_to_append = max(range(len(new_slots)), key=new_slots.__getitem__)

        new, new_slots, placed = add_to_new(
            new, new_slots, new_gnum_to_append, grouping2, p2_nums_available, placed
        )
        if DEBUG:
            print(f"new {new}")
            print(f"placed {placed}")
            print(f"new slots {new_slots}")
            print(f"\n\n")
        loops += 1

    return new


def crossover(curr_population, num_offspring, gen_start):

    offspring = {}
    for cID in range(gen_start, gen_start + num_offspring):
        ID1 = random.choice(list(curr_population.keys()))
        ID2 = random.choice(list(curr_population.keys()))
        cand1 = curr_population[ID1]
        cand2 = curr_population[ID2]

        # CROSSOVER between two Candidates
        new_cand = mate(cand1, cand2)

        # print(f"Parent 1:{cand1}")
        # print(f"Parent 2:{cand2}")
        offspring[cID] = Candidate(ID=cID, grouping=new_cand)
        # calc its fitness
        calc_candidate_fitness(offspring[cID], ranked_attrs, entity_info)
        print(offspring[cID])

    return offspring
