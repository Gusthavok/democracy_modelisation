import population
import numpy as np
import individu
params_gaussienne = individu.params_gaussienne

pops = population.Population()

pops.initialisation_aleatoire_population(1000, 2, 0, type_population="representatif_de_la_realite")

pops.affiche_1()

pops.initialisation_aleatoire_candidats(5)

for c in pops.candidats:

    (esperance, variance) = params_gaussienne[np.random.randint(0, len(params_gaussienne))]
    c.set_ideaux_initiaux(np.random.normal(esperance, 0.5*variance, 2))

couleurs_votants = ['blue', 'green', 'red', 'cyan', 'magenta', 'yellow']*5
couleurs_candidats = ['black' for _ in range(5)]

pops.affiche_2(couleurs_votants, couleurs_candidats)

print("idiot d'Orsay")
print(pops.condorcet().programme_publique)
print(pops.mesure(pops.condorcet().programme_publique))

#pops.placement_strategique_candidats(1, pops.pts_std, nombre_iteration=25)


pops.affiche_2(couleurs_votants, couleurs_candidats)
print("2 tours hahaha crosse de OK")
print(pops.election_2tours().programme_publique)
print(pops.mesure(pops.election_2tours().programme_publique))
print("Génaik")
print(pops.election_geneK().programme_publique)
print(pops.mesure(pops.election_geneK().programme_publique))

for c in pops.candidats:
    c.programme_publique = c.ideaux_initiaux
#pops.placement_strategique_candidats(0.1, pops.pts_borda, nombre_iteration=20)
pops.affiche_2(couleurs_votants, couleurs_candidats)

print("borda bordel")
print(pops.election_borda().programme_publique)
print(pops.mesure(pops.election_borda().programme_publique))

for c in pops.candidats:
    c.programme_publique = c.ideaux_initiaux
#pops.placement_strategique_candidats(0.1, pops.pts_approbation, nombre_iteration=20)
pops.affiche_2(couleurs_votants, couleurs_candidats)
print("approuvence")
print(pops.election_approbation().programme_publique)
print(pops.mesure(pops.election_approbation().programme_publique))

print("représentativité maxmimale optimisée de batard par descente de gradient du turfu machine learnig apprentissage statistique de kheng")
print(pops.opinion_optimale())
print(pops.mesure(pops.opinion_optimale()))