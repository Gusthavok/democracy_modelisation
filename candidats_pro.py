##ces candidats n'ont aucune morale, ils se placent de manière à maximiser les voix qu'ils vont recevoir
import numpy as np

#class candidats_pro:
#    def __init__(population, nombre_candidats) -> None:
#        pass

#def placement(population):
#    def voix(population.candidats):
#        def eq(indiv, candi):
#            som = 0
#            for indice in range(population.taille_opinion):
#                som += (indiv.opinion[indice]-candi.programme_publique[indice])**2
#            return som
#        
#        if len(population.candidats) == 0:
#            raise ValueError("Impossible de réaliser une élection sans candidats")
#        
#        nombre_de_voix = [0 for _ in population.candidats]
#        for indiv in population.individus:
#            score = [eq(indiv, candi) for candi in population.candidats]
#            u = np.array(score).argmin()
#            if score[u]/population.taille_opinion < population.abstention_factor**2: # On compare l'ecart quadratique moyen du programme politique avec l'opinion du PAX
#                nombre_de_voix[np.array(score).argmin()]+=1
#        
#        return nombre_de_voix

def placement(n):
    candidats = []