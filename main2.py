import population

pops = population.Population()

pops.initialisation_aleatoire_population(1000, 2, 0)

pops.initialisation_aleatoire_candidats(6)
pops.placement_strategique_candidats(1, population.Population.election_type_1, nombre_iteration=20)

couleurs_votants = ['blue', 'green', 'red', 'cyan', 'magenta', 'yellow']
couleurs_candidats = ['black' for _ in range(6)]

pops.affiche_2(couleurs_votants, couleurs_candidats)

for election in pops.elections:
    print(election().programme_publique)