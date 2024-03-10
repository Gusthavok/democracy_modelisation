import individu
import numpy as np
import matplotlib.pyplot as plt
import candidat

coef_pos = 0.05 #à quel point une interaction positive te fais changer d'avis
coef_neg = 0.1 #à quel point une interaction négative te fais changer d'avis
c_opinion = 0 #à quel point des différences d'opinion produisent des interactions négatives
c_place = 1.5 #à quel point des différences de place dans la société produisent des interactions négatives
c_place_choix_interactions = 0 #à quel point être distant socialement t'empèche d'interagir

opinion_bornee = individu.opinion_bornee

nb_neg = 0
nb_pos = 0

class Population:

    def __init__(self, ecart_type_influence = 1, ecart_type_sociabilisation= 1) -> None:
        self.individus = [] # liste d'individus
        self.candidats = [] # liste des candidats
        # parametre liés au type de société qu'on représente : beaucoup ou pas beaucoup d'intéraction, société très polarisée ou pas trop...
        
        self.ecart_type_influence = ecart_type_influence
        self.ecart_type_sociabilisation = ecart_type_sociabilisation

        self.taille_opinion = 0
        self.taille_place_societe = 0
        
        self.abstention_factor = 0.2

        self.nb_neg = 0
        self.nb_pos = 0

    def initialisation_aleatoire_population(self, taille_population:int, taille_opinion:int, taille_place_societe:int, type_population:str = "completement_aleatoire"):

        self.taille_opinion = taille_opinion
        self.taille_place_societe = taille_place_societe

        if len(self.individus) != 0:
            raise ValueError("Initialisation aléatoire sur une population non vide")
        
        if type_population == "completement_aleatoire":
            for _ in range(taille_population):
                i = individu.Individu(taille_opinion, taille_place_societe)
                i.set_completement_aleatoire(self.ecart_type_influence, self.ecart_type_sociabilisation)
                self.individus.append(i)
        elif type_population == "representatif_de_la_realite":
                i = individu.Individu(taille_opinion, taille_place_societe)
                i.set_representatif_de_la_realite(self.ecart_type_influence, self.ecart_type_sociabilisation)
                self.individus.append(i)
        else:
            raise ValueError("le type de population utilisé n'est pas valide")

    ## différents modèles représentants l'arrivée des candidats en politique
    def initialisation_aleatoire_candidats(self, nombre_candidat:int):
        if len(self.candidats) != 0:
            raise ValueError("Erreur car la liste de candidats est non vide")
        
        for _ in range(nombre_candidat):
            s = candidat.Candidat(self.taille_opinion)
            self.candidats.append(s)

    def placement_strategique_candidats(self, deplacement_moral_max:float, echantillon_type_election, nombre_iteration:int = 10):

        for k in range(nombre_iteration):
            pas = 1/(k+4)
            for ind, s in enumerate(self.candidats):
                nombre_vote = echantillon_type_election(self)[ind]
                for j in range(self.taille_opinion):

                    pas_plus = min(pas, s.ideaux_initiaux[j] + deplacement_moral_max - s.programme_publique[j]) # s.programme_publique ne doit pas dépasser s.ideaux_initiaux + deplacement_moral_max
                    pas_moins = max(-pas, s.ideaux_initiaux[j] - deplacement_moral_max - s.programme_publique[j])

                    s.programme_publique[j] += pas_plus
                    nombre_vote_plus = echantillon_type_election(self)[ind]
                    s.programme_publique[j] = s.programme_publique[j] - pas_plus + pas_moins
                    nombre_vote_moins = echantillon_type_election(self)[ind]
                    s.programme_publique[j] -= pas_moins

                    if nombre_vote_plus > nombre_vote_moins:
                        if nombre_vote_plus > nombre_vote:
                            s.programme_publique[j] += pas_plus
                    else:
                        if nombre_vote_moins > nombre_vote:
                            s.programme_publique[j] += pas_moins
    
    def etape_temporelle(self):
        for a in range(len(self.individus)):
            for _ in range(self.individus[a].sociabilisation):
                b = np.random.choice(len(self.individus))
                if np.random.binomial(1, self.proba_interactions[a][b]):
                    interaction(self.individus[a],self.individus[b])
        
    def evolution(self,n):
        if not hasattr(self, 'proba_interactions'):
            p = [[np.exp(-c_place_choix_interactions*np.linalg.norm(a.place_societe - b.place_societe)) for a in self.individus] for b in self.individus]
            self.proba_interactions = p
        for _ in range(n):
            self.etape_temporelle()
    
    def affiche_1(self, nom_fichier = ""):
        if self.taille_opinion > 3:
            raise ValueError("impossible de plot en dimension > 3")
        if self.taille_opinion == 3:
            ax = plt.axes(projection='3d')
        if self.taille_opinion == 2:  
            ax = plt.axes()
        pts = [[a.opinion[i] for a in self.individus] for i in range(self.taille_opinion)]
        ax.scatter(*pts, c = "blue")
        pts = [[a.programme_public[i] for a in self.candidats] for i in range(self.taille_opinion)]
        ax.scatter(*pts, c = "red")
        if nom_fichier != "":
            plt.savefig(nom_fichier+'.png')
        else:
            plt.show()
        plt.cla()

    
    def affiche_2(self, couleurs_individus, couleurs_candidats):
        if self.taille_opinion > 3:
            raise ValueError("impossible de plot en dimension > 3")
        if self.taille_opinion == 3:
            ax = plt.axes(projection='3d')
        if self.taille_opinion == 2:  
            ax = plt.axes()

        def eq(indiv, candi):
            som = 0
            for indice in range(self.taille_opinion):
                som += (indiv.opinion[indice]-candi.programme_publique[indice])**2
            return som
        
        if len(self.candidats) == 0:
            raise ValueError("Impossible de réaliser une élection sans candidats")
        
        votants = [[] for _ in self.candidats]
        abstentionistes = []

        for indiv in self.individus:
            score = [eq(indiv, candi) for candi in self.candidats]
            u = np.array(score).argmin()
            if score[u]/self.taille_opinion< self.abstention_factor**2:
                votants[u].append(indiv)   
            else:
                abstentionistes.append(indiv)
        
        
        pts = [[a.opinion[i] for a in abstentionistes] for i in range(self.taille_opinion)]
        ax.scatter(*pts, c = "gray")
        for ind in range(len(self.candidats)):
            pts = [[a.opinion[i] for a in votants[ind]] for i in range(self.taille_opinion)]
            ax.scatter(*pts, c = couleurs_individus[ind])
            pts = [[self.candidats[i].programme_publique[0]] for i in range(self.taille_opinion)]
            ax.scatter(*pts, c = couleurs_candidats[ind])
        
        plt.show()
        plt.cla()

    ## différents types d'élections possible
    def election_type_1(self): # candidat le plus proche en ecart quadratique
        def eq(indiv, candi):
            som = 0
            for indice in range(self.taille_opinion):
                som += (indiv.opinion[indice]-candi.programme_publique[indice])**2
            return som
        
        if len(self.candidats) == 0:
            raise ValueError("Impossible de réaliser une élection sans candidats")
        
        nombre_de_voix = [0 for _ in self.candidats]
        for indiv in self.individus:
            score = [eq(indiv, candi) for candi in self.candidats]
            u = np.array(score).argmin()
            if score[u]/self.taille_opinion < self.abstention_factor**2: # On compare l'ecart quadratique moyen du programme politique avec l'opinion du PAX
                nombre_de_voix[np.array(score).argmin()]+=1
        
        return nombre_de_voix

    def election_type_2(self):
        if len(self.candidats) == 0:
            raise ValueError("Impossible de réaliser une élection sans candidats")
        pass

    def plot_opinion_statut(self):
        ax = plt.axes(projection = '3d')
        ax.scatter([a.opinion[0] for a in self.individus], [a.opinion[1] for a in self.individus], [a.place_societe[0] for a in self.individus])
        plt.show()

def interaction(a,b):
    global nb_neg, nb_pos
    u = np.random.binomial(1, np.exp( -c_opinion*np.linalg.norm(a.opinion - b.opinion) - c_place*np.linalg.norm(a.place_societe - b.place_societe)))
    m = (a.influence*a.opinion + b.influence*b.opinion)/(a.influence + b.influence)
    if u:
        nb_pos += 1
        a.opinion += coef_pos*(m - a.opinion) # se rapproche du barycentre
        b.opinion += coef_pos*(m - b.opinion)
    else:
        #a.opinion = np.array([min(1.0, max(0.0, a.opinion[ind] - coef_neg*(m[ind] - a.opinion[ind]))) for ind in range(len(a.opinion))]) # s'écarte par rapport au barycentre
        #b.opinion = np.array([min(1.0, max(0.0, b.opinion[ind] - coef_neg*(m[ind] - b.opinion[ind]))) for ind in range(len(b.opinion))])
        a.opinion -= coef_neg*(m - a.opinion) # s'eloigne du barycentre
        b.opinion -= coef_neg*(m - b.opinion)
        if opinion_bornee:
            a.opinion = np.clip(a.opinion, 0, 1)
            b.opinion = np.clip(b.opinion, 0, 1)
        nb_neg += 1
        
    
