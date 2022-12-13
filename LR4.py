import random
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.ticker import LinearLocator
import matplotlib.animation as animation

random.seed(42)
np.random.seed(42)
POPULATION_SIZE = 200  # количество индивидуумов в популяции
P_CROSSOVER = 0.9  # вероятность скрещивания
P_MUTATION = 0.1  # вероятность мутации индивидуума
MAX_GENERATIONS = 100  # максимальное количество поколений


class Individual:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.fitness = fitness_func(x, y)

    def set_fitness(self):
        self.fitness = fitness_func(self.x, self.y)


def fitness_func(x, y):
    return x*x + y*y


def clone(value):
    ind = Individual(value.x, value.y)
    return ind


def selTournament(population, p_len):
    offspring = []
    for n in range(p_len):
        i1 = i2 = i3 = 0
        while i1 == i2 or i1 == i3 or i2 == i3:
            i1, i2, i3 = random.randint(0, p_len - 1), random.randint(0, p_len - 1), random.randint(0, p_len - 1)

        offspring.append(min([population[i1], population[i2], population[i3]], key=lambda ind: ind.fitness))

    return offspring


def crossover(p1, p2, a=0.3):
    x = a * p1.x + (1 - a) * p2.x
    y = a * p1.y + (1 - a) * p2.y
    child1 = Individual(x, y) 
    child2 = Individual(x, y)
    return child1, child2


def mutate(mutant, indpb=0.5):
    if random.random() < indpb:
        mutant.x += pow(-1, random.randint(1, 2)) * mutant.x * 0.1
    else:
        mutant.y += pow(-1, random.randint(1, 2)) * mutant.y * 0.1


N = 50
X = np.random.randint(-5, 5, N) * np.random.random(N)
Y = np.random.randint(-5, 5, N) * np.random.random(N)

population = []
for i in range(N):
    population.append(Individual(X[0], Y[0]))

generationCounter = 0
maxFitnessValues = []
meanFitnessValues = []

fig, ax = plt.subplots(subplot_kw={"projection": "3d"})

# Make data.
A = np.arange(-5, 5, 0.25)
B = np.arange(-5, 5, 0.25)
A, B = np.meshgrid(A, B)
Z = fitness_func(A, B)
z = fitness_func(X, Y)
# Plot the surface.
surf = ax.plot_surface(A, B, Z, cmap=cm.coolwarm,
                       linewidth=0, antialiased=False)

# Customize the z axis.
ax.set_zlim(0, 10)
ax.zaxis.set_major_locator(LinearLocator(10))
# A StrMethodFormatter is used automatically
ax.zaxis.set_major_formatter('{x:.02f}')

# Add a color bar which maps values to colors.
fig.colorbar(surf, shrink=0.5, aspect=5)
#ax.scatter(X, Y, z, marker='o', color="#00FF00")
while generationCounter < MAX_GENERATIONS:
    generationCounter += 1
    offspring = selTournament(population, len(population))
    offspring = list(map(clone, offspring))

    for parent1, parent2 in zip(offspring[::2], offspring[1::2]):
        if random.random() < P_CROSSOVER:
            crossover(parent1, parent2)

    for mutant in offspring:
        if random.random() < P_MUTATION:
            mutate(mutant)

    for ind in population:
        ind.set_fitness()

    population[:] = offspring

    fitnessValues = [ind.fitness for ind in population]

    maxFitness = min(fitnessValues)
    meanFitness = sum(fitnessValues) / len(population)
    maxFitnessValues.append(maxFitness)
    meanFitnessValues.append(meanFitness)
    print(f"Поколение {generationCounter}: Макс приспособ. = {maxFitness}, Средняя приспособ.= {meanFitness}")


X = np.zeros(len(population))
Y = np.zeros(len(population))
for i in range(len(population)):
    X[i] = population[i].x
    Y[i] = population[i].y

zs = fitness_func(X, Y)
ax.scatter(X, Y, zs, marker='^', color="#000000")
plt.show()