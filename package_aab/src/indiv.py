import random
class Indiv:

    def __init__(self, size, genes=[], lb=0, ub=1):
        """
        :param size: tamanho da população
        :param genes: lista do conjunto de genes
        :param lb: limite inferior para o gene. Default = 0.
        :param ub: limite superior para o gene. Default = 1
        """
        self.lb = lb
        self.ub = ub
        self.genes = genes
        self.fitness = None
        if not self.genes:
            self.init_random(size)

    def init_random(self, size):
        for x in range(size):
            self.genes.append(randint(self.lb, self.ub))

