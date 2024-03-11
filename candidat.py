import numpy as np
import individu

opinion_bornee = individu.opinion_bornee

class Candidat:
    def __init__(self, taille_ideaux:int) -> None:
        if opinion_bornee:
            self.ideaux_initiaux = np.random.random(taille_ideaux)
        else:
            self.ideaux_initiaux = np.random.normal(0,1.5,taille_ideaux)
        self.programme_publique = self.ideaux_initiaux.copy()
        self.charisme = np.max(np.random.normal(1,0.5),0) #les votants percoivent leur distance avec le candidat multiplié par un facteur 1/charisme
    
    def set_ideaux_initiaux(self, ideaux):
        self.ideaux_initiaux = ideaux
        self.programme_publique = self.ideaux_initiaux.copy()