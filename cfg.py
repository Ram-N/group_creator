import pandas as pd

POPULATION_SIZE = 100
NUM_RETAIN = 20
MUTATION_FRAC = 0.05

BIG_VALUE = 1000
NUM_GROUPS = 4
entity_info = pd.read_csv("data/raw/group_creation_sample1.csv")
CLASS_SIZE = len(entity_info)

print(f"Will divide {CLASS_SIZE} individuals into {NUM_GROUPS} groups")
ranked_attrs = ["Gender", "Country"]
