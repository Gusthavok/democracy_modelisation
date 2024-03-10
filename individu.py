import numpy as np

opinion_bornee = True

class Individu:
    def __init__(self, taille_opinion:int, taille_place_societe:int, abstension_factor = 0.2) -> None:
        self.taille_opinion = taille_opinion
        self.taille_place_societe = taille_place_societe

        self.opinion = np.array([0 for j in range(taille_opinion)])
        self.place_societe = np.array([0 for j in range(taille_place_societe)])

        self.influence = 1
        self.sociabilisation = 1

        self.abstension_factor = abstension_factor

    def set_completement_aleatoire(self, ecart_type_influence, ecart_type_sociabilisation):
        # représentation très naive de la répartition des compétences et des avis en fonction du background social (tout est indépendants)
        self.influence = np.random.exponential(1/ecart_type_influence)
        self.sociabilisation = round(1+ np.random.exponential(1/ecart_type_sociabilisation))
        if opinion_bornee:
            self.opinion = np.random.random(self.taille_opinion)
        else :
            self.opinion = np.random.normal(0,1,self.taille_opinion)
        self.place_societe = np.random.random(self.taille_place_societe)


    def set_representatif_de_la_realite():
        # but représenter de manière plus réaliste la répartition des individus en fonction de leur background social 
        # Et des liens entre l'influence et ce background
        # et des liens initiaux entre ce background et leurs opinions initiales (avant toute sociabilisation)
        pass

    def vote(self, lc):
        d = np.linalg.norm(lc - self.opinion, axis = 1)
        c = np.argmin(d)
        return d[c]/np.sqrt(self.taille_opinion) < self.abstention_factor, c #pas de vote utile dans ce modèle
    
    def approuve(self, c):
        return np.linalg.norm(c - self.opinion)/np.sqrt(self.taille_opinion) < self.abstension_factor 