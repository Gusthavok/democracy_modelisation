import numpy as np

class Candidat:
    def __init__(self, taille_ideaux:int) -> None:
        self.ideaux_initiaux = np.random.random(taille_ideaux)
        self.ideaux_modifies = self.ideaux_initiaux.copy()
    
    def set_ideaux_initiaux(self, ideaux):
        self.ideaux_initiaux = ideaux
        self.ideaux_modifies = self.ideaux_initiaux.copy()
