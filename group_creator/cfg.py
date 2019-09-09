import pandas as pd

NUM_GROUPS = 7
entity_info = pd.read_csv("../data/raw/group_creation_sample1.csv")
ranked_attrs = ["Gender", "Country"]


POPULATION_SIZE = 100
NUM_GENERATIONS = 15
NUM_RETAIN = 20
MUTATION_FRAC = 0.05

BIG_VALUE = 1000
CLASS_SIZE = len(entity_info)

print(f"Will divide {CLASS_SIZE} individuals into {NUM_GROUPS} groups")

DEBUG = False
