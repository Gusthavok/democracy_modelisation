import population
import numpy as np
import individu

class cluster:
    def __init__(self, pop:population) -> None:
        self.pop = pop
        self.location = np.sum([k.location for k in pop.pop], axis = 0)/len(pop.pop)