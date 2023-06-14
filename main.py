import random
from operator import indexOf
from pysat.formula import CNF
from pysat.solvers import Solver
import matplotlib.pyplot as plt

# two cnf files, one is satisfiable and the other is unsatisfiable
formula = CNF(from_file="Input.cnf")

# Create a solver instance for satisfiable formula
solver = Solver()
#print(formula.clauses)
maxFitness = len(formula.clauses)


# solver.append_formula(formula.clauses)

# actually solves it and can find out if it's satisfiable
# print(solver.solve())

# if it's satisfiable we can get an answer
# print(solver.get_model())


def random_chromosome(size):
    return [random.randint(0, 1) for _ in range(size)]


def fitness(chromosome):
    n = len(chromosome)
    result = 0
    for clauses in formula.clauses:
        found = False
        for clause in clauses:
            if clause < 0 and chromosome[abs(clause) - 1] == 0:
                found = True
            elif clause > 0 and chromosome[clause - 1] == 1:
                found = True
        if found:
            result += 1
    return result


def crossover(x, y):
    n = len(x)
    child = [0] * n
#    index_break = random.randint(0, n)
    index_break = n // 2
    for i in range(n):
        child = x[:index_break] + y[index_break:]
    return child


def mutate(x):
    n = len(x)
    c = random.randint(0, n - 1)
    m = random.randint(0, 1)
    x[c] ^= 1
    return x


def probability(chromosome):
    return fitness(chromosome) / maxFitness


def random_pick(cur_population, probabilities):
    population_with_probability = zip(population, probabilities)
    total = sum(w for c, w in population_with_probability)
    r = random.uniform(0, total)
    upto = 0
    for c, w in zip(cur_population, probabilities):
        if upto + w >= r:
            return c
        upto += w
    assert False, "Shouldn't get here"


def genetic_sat(cur_population):
    mutation_probability = 0.1
    new_population = []
    sorted_population = []
    probabilities = []
    for n in cur_population:
        f = fitness(n)
        probabilities.append(f / maxFitness)
        sorted_population.append([f, n])

    sorted_population.sort(reverse=True)

    # Elitism
    new_population.append(sorted_population[0][1])  # the best gen
    new_population.append(sorted_population[-1][1])  # the worst gen

    for i in range(len(population) - 2):

        chromosome_1 = random_pick(population, probabilities)
        chromosome_2 = random_pick(population, probabilities)

        # Creating two new chromosomes from 2 chromosomes
        child = crossover(chromosome_1, chromosome_2)

        # Mutation
        if random.random() < mutation_probability:
            child = mutate(child)

        new_population.append(child)
        if fitness(child) == maxFitness:
            break
    return new_population


def print_chromosome(chrom):
    print(
        "Chromosome = {},  Fitness = {}".format(str(chrom), fitness(chrom))
    )


if __name__ == "__main__":
    while True:
        generations = []
        generations_max_fit = []
        POPULATION_SIZE = 200

        nc = formula.nv
        population = [random_chromosome(nc) for _ in range(POPULATION_SIZE)]

        generation = 1
        while (
            not maxFitness in [fitness(chrom) for chrom in population]
            and generation < 200
        ):

            population = genetic_sat(population)
            if generation % 10 == 0:
                print("=== Generation {} ===".format(generation))
                print(
                    "Maximum Fitness = {}".format(
                        max([fitness(n) for n in population])
                    )
                )
            generations.append(generation)
            generations_max_fit.append(max([fitness(n) for n in population]))

            generation += 1

        fitnessOfChromosomes = [fitness(chrom) for chrom in population]

        bestChromosomes = population[
            indexOf(fitnessOfChromosomes, max(fitnessOfChromosomes))
        ]

        if maxFitness in fitnessOfChromosomes:
            print("\nSolved in Generation {}!".format(generation - 1))

            print_chromosome(bestChromosomes)
            exit(0)

        else:
            print(
                "\nUnfortunately, we could't find the answer until generation {}. The best answer that the algorithm found was:".format(
                    generation - 1
                )
            )
        if generations_max_fit[-1] > 426:
            plt.ylabel("Clauses satisfied")
            plt.xlabel("Generation Number")
            plt.plot(generations, generations_max_fit)
            plt.show()
            break


"""
# we can make a test list and feed it to the model as an assumption
variables = []
# test for satisfiable formula:
for i in range(1, formula.nv + 1):
    var = (random.randint(0, 1))
    if var == 1:
        variables.append(i)
    else:
        variables.append(-i)

print(solver.solve(assumptions=variables))
"""
