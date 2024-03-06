import individu
import numpy as np

class population:
    def __init__(self, n:int) -> None:
        self.pop = [individu.individu(k/n) for k in range (n + 1)]
        self.age = 0

    def evolution(self):
        interactions = []
        for k in range (len(self.pop)):
            interactions.extend([k for i in range (self.pop[k].sociabilisation)])
        interactions = np.random.permutation(interactions)
        j = 0
        k = 0
        while k < len(self.pop):
            i = 0
            while i < self.pop[k].sociabilisation:
                if k != interactions[k + j + i]:
                    self.pop[k].interaction(self.pop[interactions[k + j + i]])
                i+=1
            j+=i - 1
            k+=1