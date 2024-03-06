import numpy as np

class Individu:
    def __init__(self, taille_opinion:int, taille_statut_social:int) -> None:
        self.taille_opinion = taille_opinion
        self.taille_statut_social = taille_statut_social

        self.opinion = np.array([0 for j in range(taille_opinion)])
        self.statut_social = np.array([0 for j in range(taille_statut_social)])

        self.influence = 1
        self.sociabilisation = 1

    def set_completement_aleatoire(self, ecart_type_influence, ecart_type_sociabilisation):
        # représentation très naive de la répartition des compétences et des avis en fonction du background social (tout est indépendants)
        self.influence = np.random.exponential(1/ecart_type_influence)
        self.sociabilisation = round(1+ np.random.exponential(1/ecart_type_sociabilisation))

        self.opinion = np.random.random(self.taille_opinion)
        self.statut_social = np.random.random(self.taille_statut_social)


    def set_representatif_de_la_realite():
        # but représenter de manière plus réaliste la répartition des individus en fonction de leur background social 
        # Et des liens entre l'influence et ce background
        # et des liens initiaux entre ce background et leurs opinions initiales (avant toute sociabilisation)
        pass
    