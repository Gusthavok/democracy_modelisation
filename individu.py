import numpy as np
import parametres

c_place_choix_interactions = parametres.c_place_choix_interactions
opinion_bornee = parametres.opinion_bornee

class Individu:
    def __init__(self, taille_opinion:int, taille_place_societe:int, abstension_factor = 0.5) -> None:
        self.taille_opinion = taille_opinion
        self.taille_place_societe = taille_place_societe

        self.opinion = np.array([0 for j in range(taille_opinion)])
        self.place_societe = np.array([0 for j in range(taille_place_societe)])

        self.influence = 1
        self.sociabilisation = [0]

        self.abstension_factor = abstension_factor

    def set_completement_aleatoire(self, ecart_type_influence, ecart_type_sociabilisation):
        # représentation très naive de la répartition des compétences et des avis en fonction du background social (tout est indépendants)
        self.influence = np.random.exponential(1/ecart_type_influence)
        self.sociabilisation = [0 for _ in range (round(1+ np.random.exponential(1/ecart_type_sociabilisation)))]
        if opinion_bornee:
            self.opinion = np.random.random(self.taille_opinion)
        else :
            self.opinion = np.random.normal(0,1,self.taille_opinion)
        self.place_societe = np.random.random(self.taille_place_societe)

    def set_completement_aleatoire_suite(self, population, taille_population):
        for _ in range(len(self.sociabilisation)):
            add = True
            while add:
                b = np.random.choice(taille_population)
                if population.individus[b] != self and not(population.individus[b] in self.sociabilisation):
                    if np.random.binomial(1, np.exp(-c_place_choix_interactions*np.linalg.norm(self.place_societe - population.individus[b].place_societe))):
                        self.sociabilisation.append(b)
                        add = False


    def set_representatif_de_la_realite():
        # but représenter de manière plus réaliste la répartition des individus en fonction de leur background social 
        # Et des liens entre l'influence et ce background
        # et des liens initiaux entre ce background et leurs opinions initiales (avant toute sociabilisation)
        pass

    def vote(self, lc):
        charismes = [c.charisme for c in lc]
        programmes = np.array([c.programme_publique for c in lc])
        d = np.linalg.norm(programmes - self.opinion, axis = 1)/charismes
        c = np.argmin(d)
        return d[c]/np.sqrt(self.taille_opinion) < self.abstension_factor, c #pas de vote utile dans ce modèle
    
    def approuve(self, c):
        return np.linalg.norm(c.programme_publique - self.opinion)/(np.sqrt(self.taille_opinion) * c.charisme) < self.abstension_factor 
    
    def trie(self, lc):
        charismes = np.array([c.charisme for c in lc])
        programmes = np.array([c.programme_publique for c in lc])
        d = np.linalg.norm(programmes - self.opinion, axis = 1)/charismes
        return np.argsort(d)