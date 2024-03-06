import numpy as np
import parametres

class individu:
    def __init__(self, opinion:float) -> None:
        self.opinion = opinion
        self.charisme = np.random.exponential(1)
        self.sociabilisation = int(self.charisme) + 1
        self.location = np.random.uniform(-1, 1, 2)
##individu [opinion, charisme, sociabilisation], opinion (entre 0 et 1), 
#charisme (change la moyenne (peut être aussi plus de chance d'avoir une interaction positive)),
#socialbilisation: nombre d'interaction par step (1 et plus)
    
    def interaction(self, b):
        if self.opinion > b.opinion:
            return individu.interaction(b, self)
        else:
            u = np.random.binomial(1, np.exp((-2) * (b.opinion - self.opinion)))
            if u:
                individu.interaction_positive(self, b)
            else:
                individu.interaction_negative(self, b)
    
    def interaction_positive(self, b):
        m = (self.opinion * self.charisme + b.opinion * b.charisme)/(self.charisme + b.charisme)
        self.opinion = m + (self.opinion - m)/parametres.l_pos
        b.opinion = m + (b.opinion - m)/parametres.l_pos
    
    def interaction_negative(self, b):
        self.opinion = self.opinion/parametres.l_neg
        b.opinion = 1 - (1 - b.opinion)/parametres.l_neg