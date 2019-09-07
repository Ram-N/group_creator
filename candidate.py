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

    def display_group_detailsing(self):
        gstr = f"Candidate:{self.ID} has {self.grouping}"
        return gstr

