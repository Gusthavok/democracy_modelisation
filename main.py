import population

pops = population.Population()

pops.initialisation_aleatoire_population(1000, 2, 1)
pops.affiche_1(nom_fichier = "imgs/fichier_de_base")


for ind in range(60):
    pops.evolution(5)
    pops.affiche_1(nom_fichier = "imgs/fichier_"+str(ind))

pops.initialisation_aleatoire_candidats(6)
pops.placement_strategique_candidats(1, population.Population.election_type_1, nombre_iteration=20)

couleurs_votants = ['blue', 'green', 'red', 'cyan', 'magenta', 'yellow']
couleurs_candidats = ['black' for _ in range(6)]

pops.affiche_2(couleurs_votants, couleurs_candidats)
pops.plot_opinion_statut()

print('ratio pos/neg : ', population.nb_pos/population.nb_neg)