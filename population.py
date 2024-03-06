import individu
import candidats



class Population:

    def __init__(self, opinion:Opinion) -> None:
        self.individus # liste d'individus
        self.candidats # liste des candidats

        # D'autres parametre liés au type de société qu'on représente : beaucoup ou pas beaucoup d'intéraction, société très polarisée ou pas trop...
        #self. ...

    def etape_temporelle(self):
        pass
        # Boucle de interaction()
    
    def affiche(self):
        pass

    def election_type_1(self):
        pass

    def election_type_2(self):
        pass

def interaction(self): # A refaire
    if self.opinion > b.opinion:
        return individu.interaction(b, self)
    else:
        u = np.random.binomial(1, np.exp((-2) * (b.opinion - self.opinion)))
        if u:
            individu.interaction_positive(self, b)
        else:
            individu.interaction_negative(self, b)

def interaction_positive(self, b):
    pass

def interaction_negative(self, b):
    pass