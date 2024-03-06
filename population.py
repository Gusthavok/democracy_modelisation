import individu
import candidats

class Population:

    def __init__(self) -> None:
        self.individus = [] # liste d'individus
        self.candidats = [] # liste des candidats

        # parametre liés au type de société qu'on représente : beaucoup ou pas beaucoup d'intéraction, société très polarisée ou pas trop...
        
        self.ecart_type_influence = 1
        self.ecart_type_sociabilisation = 1

    def initialisation_aleatoire_population(self, taille_population:int, taille_opinion:int, taille_statut_social:int, type_population:int = "completement_aleatoire"):
        if len(self.individus) != 0:
            raise ValueError("Initialisation aléatoire sur une population non vide")
        
        if type_population == "completement_aleatoire":
            self.individus = [individu.Individu(taille_opinion, taille_statut_social).set_completement_aleatoire() for _ in range(taille_population)]
        elif type_population == "representatif_de_la_realite":
            self.individus = [individu.Individu(taille_opinion, taille_statut_social).set_representatif_de_la_realite() for _ in range(taille_population)]
        else:
            raise ValueError("le type de population utilisé n'est pas valide")

    ## différents modèles représentants l'arrivée des candidats en politique
    def placement_candidats_type_1():
        pass
    
    def placement_candidats_type_1():
        pass

    def etape_temporelle(self):
        pass
        # Boucle de interaction()
    
    def affiche(self):
        pass
    
    ## différents types d'élections possible
    def election_type_1(self):
        if len(self.candidats) == 0:
            raise ValueError("Impossible de réaliser une élection avec aucun candidats")
        pass

    def election_type_2(self):
        if len(self.candidats) == 0:
            raise ValueError("Impossible de réaliser une élection avec aucun candidats")
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