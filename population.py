import individu
import numpy as np
import matplotlib.pyplot as plt


coef_pos = 1.05
coef_neg = 1.1


class Population:

    def __init__(self) -> None:
        self.individus = [] # liste d'individus
        self.candidats = [] # liste des candidats
        # parametre liés au type de société qu'on représente : beaucoup ou pas beaucoup d'intéraction, société très polarisée ou pas trop...
        
        self.ecart_type_influence = 1
        self.ecart_type_sociabilisation = 1

    def initialisation_aleatoire_population(self, taille_population:int, taille_opinion:int, taille_statut_social:int, type_population:int = "completement_aleatoire"):

        self.taille_opinion = taille_opinion

        if len(self.individus) != 0:
            raise ValueError("Initialisation aléatoire sur une population non vide")
        
        if type_population == "completement_aleatoire":
            for _ in range(taille_population):
                i = individu.Individu(taille_opinion, taille_statut_social)
                i.set_completement_aleatoire(self.ecart_type_influence, self.ecart_type_sociabilisation)
                self.individus.append(i)
        elif type_population == "representatif_de_la_realite":
                i = individu.Individu(taille_opinion, taille_statut_social)
                i.set_representatif_de_la_realite(self.ecart_type_influence, self.ecart_type_sociabilisation)
                self.individus.append(i)
        else:
            raise ValueError("le type de population utilisé n'est pas valide")

    ## différents modèles représentants l'arrivée des candidats en politique
    def placement_candidats_type_1():
        pass
    
    def placement_candidats_type_1():
        pass


    def etape_temporelle(self):
        for a in self.individus:
            for i in range(a.sociabilisation):
                interaction(a,np.random.choice(self.individus))
        
    def evolution(self,n):
        for i in range(n):
            self.etape_temporelle
    
    def affiche(self):
        if self.taille_opinion > 2:
            raise ValueError("impossible de plot en dimension > 2")
        plt.scatter([a.opinion[0] for a in self.individus],[a.opinion[1] for a in self.individus])
        plt.show()
    
    ## différents types d'élections possible
    def election_type_1(self):
        if len(self.candidats) == 0:
            raise ValueError("Impossible de réaliser une élection avec aucun candidats")
        pass

    def election_type_2(self):
        if len(self.candidats) == 0:
            raise ValueError("Impossible de réaliser une élection avec aucun candidats")
        pass

def interaction(a,b):
    u = np.random.binomial(1, np.exp((-2) * np.linalg.norm(a.opinion - b.opinion)))
    if u:
        m = (a.influence*a.opinion + b.influence*b.opinion)/(a.influence + b.influence)
        a.opinion = a.opinion + coef_pos*(m - a.opinion)
        b.opinion = b.opinion + coef_pos*(m - b.opinion)
    else:
        a.opinion = a.opinion*(1-coef_neg)
        b.opinion = 1 - (1 - b.opinion)*(1-coef_neg)    
    
