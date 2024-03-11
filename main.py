import population
import parametres

type_interactions = parametres.type_interactions
taille_opinion = parametres.taille_opinion
taille_population = parametres.taille_population
taille_place_societe = parametres.taille_place_societe

pops = population.Population()

pops.initialisation_aleatoire_population(taille_population, taille_opinion, taille_place_societe, type_interactions=type_interactions)
pops.affiche_1(nom_fichier = "imgs/fichier_de_base")


for ind in range(20):
    pops.evolution(10, taille_opinion, type_interaction=type_interactions)
    pops.affiche_1(nom_fichier = "imgs/fichier_"+str(ind))

pops.initialisation_aleatoire_candidats(6)
pops.placement_strategique_candidats(1, pops.election_type_1, nombre_iteration=20)

couleurs_votants = ['blue', 'green', 'red', 'cyan', 'magenta', 'yellow']
couleurs_candidats = ['black' for _ in range(6)]

pops.affiche_2(couleurs_votants, couleurs_candidats)
pops.plot_opinion_statut()

print('ratio pos/neg : ', population.nb_pos/population.nb_neg)