import random

class GeneticAlgorithm:

    def __init__(self, population):
         self.population = population

    def rand():
        return random.random()
        
    def crossover(self, chromosome0, chromosome1):
        for i in range(len(chromosome0)):
            if random.random() > 0.5:
                tmp = chromosome0[i]
                chromosome0[i] = chromosome1[i]
                chromosome1[i] = tmp

    def crossoverProbability(self, meanFitness, maxFitness, fitness0, fitness1):
        fitness = max(fitness0, fitness1)
        if fitness < meanFitness:
            # always cross chromosomes of those cells with less than average fitness
            return 1.0
        return (maxFitness - fitness) / (maxFitness - meanFitness)

