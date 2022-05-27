from random import randint, random, shuffle, uniform


class Indiv:

    def __init__(self, size=int, genes, lb=0, ub=1):
        """
        :param size: tamanho da população
        :param genes: lista do conjunto de genes
        :param lb: limite inferior para o gene. Default = 0.
        :param ub: limite superior para o gene. Default = 1
        """
        self.lb = lb  # limite inferior do gene
        self.ub = ub  # limite superior do gene
        self.genes = genes  # genoma
        self.fitness = None  # valor de aptidão
        if not self.genes:  # se não exist lista de genes:
            self.init_random(size)  # criar indivíduo aleatório

    def __eq__(self, solution):
        if isinstance(solution, self.__class__):
            return self.genes.sort() == solution.genes.sort()
        return False

    def __gt__(self, solution):
        if isinstance(solution, self.__class__):
            return self.fitness > solution.fitness
        return False

    def __ge__(self, solution):
        if isinstance(solution, self.__class__):
            return self.fitness >= solution.fitness
        return False

    def __lt__(self, solution):
        if isinstance(solution, self.__class__):
            return self.fitness < solution.fitness
        return False

    def __le__(self, solution):
        if isinstance(solution, self.__class__):
            return self.fitness <= solution.fitness
        return False

    def __str__(self):
        return f"{str(self.genes)} {self.getFitness()}"

    def __repr__(self):
        return self.__str__()

    def setFitness(self, fit):
        self.fitness = fit

    def getFitness(self):
        return self.fitness

    def getGenes(self):
        return self.genes

    def init_random(self, size=int):
        """
        método para gerar indivíduos aleatoriamente
        :param size:
        """
        self.genes = []
        for x in range(size):  # a cada x para a quantidade de populaçao
            self.genes.append(randint(self.lb, self.ub))  # gerar individuos aleatoriamente entre os limites

    def mutation(self):
        s = len(self.genes)
        pos = randint(0, s - 1)  # gera posição; s-1 pois o len começa a contar do 1 e no randint inclusive
        if self.genes[pos] == 0:  # se na posiçao tiver 0:
            self.genes[pos] = 1  # passa a 1
        else:
            self.genes[pos] = 0  # ao contrário, passa a 0

    def crossover(self, indiv2):  # cruzamento de um ponto
        return self.one_pt_crossover(indiv2)

    def one_pt_crossover(self, indiv2):  # cruzar com individuo 2

        offsp1 = []  # descendente 1
        offsp2 = []  # descendente 2
        s = len(self.genes)  # contar elem
        pos = randint(0, s - 1)  # atribuir posiçao
        for i in range(pos):
            offsp1.append(self.genes[i])  # fica igual até à pos -1
            offsp2.append(indiv2.genes[i])  # igual até à pos -1
        for i in range(pos, s):
            offsp2.append(self.genes[i])  # troca de pos ate ao fim (progenitor 2 troca com 1)
            offsp1.append(indiv2.genes[i])  # troca de pos ate ao fim (progenitor 1 troca com 2)
        res1 = self.__class__(s, offsp1, self.lb, self.ub)  # para usar o mesmo metodo numa representaçao inteira
        res2 = self.__class__(s, offsp2, self.lb, self.ub)
        return res1, res2


class IndivInt(Indiv):
    """
    método de representação inteira do algoritmo
    """

    def __init__(self, size=int, genes, lb=0, ub=1):
        self.lb = lb
        self.ub = ub
        self.genes = genes
        self.fitness = None
        if not self.genes:
            self.initRandom(size)

    def initRandom(self, size=int):  # criar indiviudos aleatoriamente
        self.genes = []
        for _ in range(size):
            self.genes.append(randint(0, self.ub))

    def mutation(self):
        s = len(self.genes)  # tamanho dos genes
        pos = randint(0, s - 1)  # random posicao
        self.genes[pos] = randint(0, self.ub)  # replace da posição por um valor aleatorio (0,1)




