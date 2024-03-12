import population

pops = population.Population()

pops.initialisation_aleatoire_population(1000, 2, 0, type_population="representatif_de_la_realite")

pops.initialisation_aleatoire_candidats(10)

couleurs_votants = ['blue', 'green', 'red', 'cyan', 'magenta', 'yellow']*5
couleurs_candidats = ['black' for _ in range(10)]

##print(pops.condorcet().programme_publique)

pops.placement_strategique_candidats(1, pops.pts_std, nombre_iteration=15)

pops.affiche_1()

pops.affiche_2(couleurs_votants, couleurs_candidats)
print(pops.election_2tours().programme_publique)
print(pops.election_geneK().programme_publique)

for c in pops.candidats:
    c.programme_publique = c.ideaux_initiaux
pops.placement_strategique_candidats(0.1, pops.pts_borda, nombre_iteration=20)
pops.affiche_2(couleurs_votants, couleurs_candidats)
print(pops.election_borda().programme_publique)

for c in pops.candidats:
    c.programme_publique = c.ideaux_initiaux
pops.placement_strategique_candidats(0.1, pops.pts_approbation, nombre_iteration=20)
pops.affiche_2(couleurs_votants, couleurs_candidats)
print(pops.election_approbation().programme_publique)