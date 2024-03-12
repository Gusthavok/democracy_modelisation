import individu
import numpy as np
import matplotlib.pyplot as plt
import candidat
import parametres as param

coef_pos = param.coef_pos #à quel point une interaction positive te fais changer d'avis
coef_neg = param.coef_neg #à quel point une interaction négative te fais changer d'avis
c_opinion = param.c_opinion #à quel point des différences d'opinion produisent des interactions négatives
c_place = param.c_place #à quel point des différences de place dans la société produisent des interactions négatives
c_place_choix_interactions = param.c_place_choix_interactions #à quel point être distant socialement t'empèche d'interagir
l = param.l#norme l vis a vis des opinions
p = param.p#norme p vis a vis de la pop

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
        
        self.abstention_factor = 1

        self.nb_neg = 0
        self.nb_pos = 0

        self.elections = [self.election_2tours, self.election_approbation, self.election_geneK, self.condorcet, self.election_borda]

    def initialisation_aleatoire_population(self, taille_population:int, taille_opinion:int, taille_place_societe:int, type_population:str = "completement_aleatoire", type_interactions = "initiale"):

        self.taille_opinion = taille_opinion
        self.taille_place_societe = taille_place_societe

        if len(self.individus) != 0:
            raise ValueError("Initialisation aléatoire sur une population non vide")
        
        if type_population == "completement_aleatoire":
            for _ in range(taille_population):
                i = individu.Individu(taille_opinion, taille_place_societe)
                i.set_completement_aleatoire(self.ecart_type_influence, self.ecart_type_sociabilisation)
                self.individus.append(i)
            if type_interactions == "graph":
                for i in self.individus:
                    i.set_completement_aleatoire_suite(self, taille_population)
        elif type_population == "representatif_de_la_realite":
            for _ in range(taille_population):
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
        self.candidats = np.array(self.candidats)

    def placement_strategique_candidats(self, deplacement_moral_max:float, echantillon_type_election, nombre_iteration:int = 10):

        for k in range(nombre_iteration):
            pas = 1/(k+1)
            for ind, s in enumerate(self.candidats):
                nombre_vote = echantillon_type_election()[ind]
                for j in range(self.taille_opinion):

                    pas_plus = min(pas, s.ideaux_initiaux[j] + deplacement_moral_max - s.programme_publique[j]) # s.programme_publique ne doit pas dépasser s.ideaux_initiaux + deplacement_moral_max
                    pas_moins = max(-pas, s.ideaux_initiaux[j] - deplacement_moral_max - s.programme_publique[j])

                    s.programme_publique[j] += pas_plus
                    nombre_vote_plus = echantillon_type_election()[ind]
                    s.programme_publique[j] = s.programme_publique[j] - pas_plus + pas_moins
                    nombre_vote_moins = echantillon_type_election()[ind]
                    s.programme_publique[j] -= pas_moins

                    if nombre_vote_plus > nombre_vote_moins:
                        if nombre_vote_plus > nombre_vote:
                            s.programme_publique[j] += pas_plus
                    else:
                        if nombre_vote_moins > nombre_vote:
                            s.programme_publique[j] += pas_moins
    
    def etape_temporelle(self, taille_opinion):
        for a in range(len(self.individus)):
            for _ in range(len(self.individus[a].sociabilisation)):
                b = np.random.choice(len(self.individus))
                if np.random.binomial(1, self.proba_interactions[a][b]):
                    interaction(self.individus[a],self.individus[b])
        self.normalisation()
        self.lobotomisation(taille_opinion)
    
    def etape_temporelle_graph(self, taille_opinion):
        for a in self.individus:
            for b in a.sociabilisation:
                interaction(a, self.individus[b])
        if not(param.opinion_bornee):
            self.normalisation()
            self.lobotomisation(taille_opinion)

    def normalisation(self):
        sigma = np.std([i.opinion for i in self.individus])
        for i in self.individus:
            i.opinion = i.opinion/sigma

    def lobotomisation(self, taille_opinion):#aka fusillée sur la place plublique 
        for i in self.individus:
            if np.linalg.norm(i.opinion) > 5:
                i.opinion = np.array([0.0 for j in range(taille_opinion)])
        
    def evolution(self,n, taille_opinion, type_interaction:str="initiale"):
        if type_interaction == "initiale":
            if not hasattr(self, 'proba_interactions'):
                p = [[np.exp(-c_place_choix_interactions*np.linalg.norm(a.place_societe - b.place_societe)) for a in self.individus] for b in self.individus]
                self.proba_interactions = p
            for _ in range(n):
                self.etape_temporelle(taille_opinion)
        elif type_interaction == "graph":
            for _ in range(n):
                self.etape_temporelle_graph(taille_opinion)
    
    def affiche_1(self, nom_fichier = ""):
        if self.taille_opinion > 3:
            raise ValueError("impossible de plot en dimension > 3")
        if self.taille_opinion == 3:
            ax = plt.axes(projection='3d')
        if self.taille_opinion == 2:  
            ax = plt.axes()
        pts = [[a.opinion[i] for a in self.individus] for i in range(self.taille_opinion)]
        ax.scatter(*pts, c = "blue")
        pts = [[a.programme_publique[i] for a in self.candidats] for i in range(self.taille_opinion)]
        ax.scatter(*pts, c = "red")
        if nom_fichier != "":
            plt.savefig(nom_fichier+'.png')
        else:
            plt.show()
        ax.cla()
        plt.cla()
        plt.close("all")

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
            if score[u]/self.taille_opinion < self.abstention_factor**2:
                votants[u].append(indiv)   
            else:
                abstentionistes.append(indiv)
        
        
        pts = [[a.opinion[i] for a in abstentionistes] for i in range(self.taille_opinion)]
        ax.scatter(*pts, c = "gray")
        for ind in range(len(self.candidats)):
            pts = [[a.opinion[i] for a in votants[ind]] for i in range(self.taille_opinion)]
            ax.scatter(*pts, c = couleurs_individus[ind])
            pts = [[self.candidats[ind].programme_publique[i]] for i in range(self.taille_opinion)]
            ax.scatter(*pts, c = couleurs_candidats[ind])
        
        plt.show()
        ax.cla()
        plt.cla()
        plt.close("all")

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

    def pts_std(self):
        votes = np.zeros(len(self.candidats))
        for i in self.individus:
            votant, choix = i.vote(self.candidats)
            if votant:
                votes[choix] += 1
        return votes
    
    def election_2tours(self):
        votes = np.zeros(len(self.candidats))
        for i in self.individus:
            votant, choix = i.vote(self.candidats)
            if votant:
                votes[choix] += 1
        s = np.argsort(self.pts_std())
        passants = self.candidats[s]
        votes = np.zeros(len(passants))
        for i in self.individus:
            votant, choix = i.vote(passants)
            if votant:
                votes[choix] += 1
        return passants[np.argmax(votes)]

    def pts_approbation(self): 
        votes = np.zeros(len(self.candidats))
        for ind in self.individus:
            for i in range(len(self.candidats)):
                if ind.approuve(self.candidats[i]):
                    votes[i] += 1
        return votes

    def election_approbation(self):
        return self.candidats[np.argmax(self.pts_approbation())]
    
    def election_geneK(self, limite2ndtour = 0.1):
        votes = self.pts_std()
        nb_votants = np.sum(votes)
        passants = self.candidats[np.where(votes > limite2ndtour*nb_votants)]
        votes = np.zeros(len(passants))
        for i in self.individus:
            votant, choix = i.vote(passants)
            if votant:
                votes[choix] += 1
        return passants[np.argmax(votes)]
        
    def condorcet(self):
        for c1 in self.candidats:
            possible = True
            for c2 in self.candidats:
                v = [0,0]
                for i in self.individus:
                    votant, choix = i.vote([c1,c2])
                    if votant:
                        v[choix] += 1
                possible = possible and v[0] >= v[1]
            if possible:
                return c1
        return None
    
    def pts_borda(self, n = None):
        if n == None:
            n = len(self.candidats)
        pts = np.zeros(len(self.candidats))
        for i in self.individus:
            tri = i.trie(self.candidats)
            for k in range(n):
                pts[tri[k]] += n-k
        return pts
    
    def election_borda(self, n = None):
        return self.candidats[np.argmax(self.pts_borda(n))]
    
    def mesure(self, opinion):
        global l, p
        som = 0
        for i in self.individus:
            saum = 0
            for k in range (self.taille_opinion):
                saum += np.abs(opinion[k] - i.opinion[k])**l
            som += saum**(p/l)
        return (som/len(self.individus))**(1/p)

    def opinion_optimale(self):
        global coefficient_norme_l, coefficient_norme_p
        nombre_de_try = 10
        nombre_etape = 20
        l_opinon = []
        l_mesure = []

        for _ in range(nombre_de_try):
            opinion = np.random.random(self.taille_opinion)
            for etape in range(nombre_etape):
                pas = 1/(etape+3)
                for j in range(self.taille_opinion):

                    opinion[j] += pas
                    val_plus = self.mesure(opinion)
                    opinion[j] -= opinion[j] + pas*2
                    val_moins = self.mesure(opinion)
                    opinion[j] += pas

                    val = self.mesure(opinion)
                    if val_plus < val_moins:
                        if val_plus < val:
                            opinion[j] += pas
                    else:
                        if val_moins < val:
                            opinion[j] += pas
            
            l_opinon.append(opinion.copy())
            l_mesure.append(self.mesure(opinion))
        
        return l_opinon[np.argmin(l_mesure)]

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