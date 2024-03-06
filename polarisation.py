import matplotlib.pyplot as plt
import population
import parametres

popu = population.population(parametres.taille_pop)

def polarisation(pop = popu, n = parametres.nombre_pas):
    plt.plot([k.opinion for k in pop.pop], [k.charisme for k in pop.pop])
    plt.show()
    for k in range (n):
        pop.evolution()
    plt.hist([k.opinion for k in pop.pop])
    plt.show()