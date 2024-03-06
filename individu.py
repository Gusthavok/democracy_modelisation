import numpy as np

class Individu:
    def __init__(self, taille_opinion:int, taille_statut_social:int) -> None:
        self.opinion = np.array([0 for j in range(taille_opinion)])
        self.statut_social = np.array([0 for j in range(taille_statut_social)])

        self.influence = 1
        self.sociabilisation = 1

    def set_completement_aleatoire():
        pass
    def set_representatif_de_la_realite():
        pass
    