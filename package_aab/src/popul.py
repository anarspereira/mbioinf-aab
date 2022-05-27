# -*- coding: utf-8 -*-
"""
Package dos algoritmos implementados em aula
Algoritmos Avançados de Bioinformática
"""

"""
Class: Implementação de Algoritmos Evolucionários - População
"""

from indiv import Indiv, IndivInt, IndivReal
from random import random


class Popul:
    """
    Classe para implementar populações de indivíduos com representações binárias
    """

    def __init__(self, popsize: int, indsize: int, indivs=[]):
        """
        :param popsize: Número de indivíduos da população
        :param indsize: Tamanho dos indivíduos
        :param indivs: Indivíduos
        """
        self.popsize = popsize
        self.indsize = indsize
        if indivs:
            self.indivs = indivs
        else:
            self.initRandomPop()

    def getIndiv(self, index):
        """

        :param index:
        :return:
        """
        return self.indivs[index]

    def initRandomPop(self):
        """

        :return:
        """
        self.indivs = []
        for _ in range(self.popsize):
            indiv_i = Indiv(self.indsize, [])
            self.indivs.append(indiv_i)

    def getFitnesses(self, indivs=None):
        """

        :param indivs:
        :return:
        """
        fitnesses = []
        if not indivs:
            indivs = self.indivs
        for ind in indivs:
            fitnesses.append(ind.getFitness())
        return fitnesses

    def bestSolution(self):
        """

        :return:
        """
        return max(self.indivs)

    def bestFitness(self):
        """

        :return:
        """
        indv = self.bestSolution()
        return indv.getFitness()


    def selection(self, n, indivs=None):
        """

        :param n:
        :param indivs:
        :return:
        """
        res = []
        fitnesses = list(self.linscaling(self.getFitnesses(indivs)))
        for _ in range(n):
            sel = self.roulette(fitnesses)
            fitnesses[sel] = 0.0
            res.append(sel)
        return res

    def roulette(self, f):
        """

        :param f:
        :return:
        """
        tot = sum(f)
        val = random()
        acum = 0.0
        ind = 0
        while acum < val:
            acum += (f[ind] / tot)
            ind += 1
        return ind-1

    def linscaling(self, fitnesses):
        """

        :param fitnesses:
        :return:
        """
        mx = max(fitnesses)
        mn = min(fitnesses)
        res = []
        for f in fitnesses:
            val = (f-mn)/(mx-mn)
            res.append(val)
        return res

    def recombination(self, parents, noffspring):
        """
        Método de recombinação que usa cruzamento para criar novas soluções e aplica mutação a cada nova solução.
        :param parents:
        :param noffspring:
        :return:
        """
        offspring = []
        new_inds = 0
        while new_inds < noffspring:
            parent1 = self.indivs[parents[new_inds]]
            parent2 = self.indivs[parents[new_inds+1]]
            offsp1, offsp2 = parent1.crossover(parent2)
            offsp1.mutation()
            offsp2.mutation()
            offspring.append(offsp1)
            offspring.append(offsp2)
            new_inds += 2
        return offspring

    def reinsertion(self, offspring):
        """
        Método de reinserção.
        :param offspring:
        :return:
        """
        tokeep = self.selection(self.popsize-len(offspring))
        ind_offsp = 0
        for i in range(self.popsize):
            if i not in tokeep:
                self.indivs[i] = offspring[ind_offsp]
                ind_offsp += 1


class PopulInt(Popul):
    """
    Extensão da classe Popul com implementação do método initRandomPop (override) para representações inteiras.
    """

    def __init__(self, popsize, indsize, ub, indivs=[]):
        """

        :param popsize:
        :param indsize:
        :param ub:
        :param indivs:
        """
        self.ub = ub
        Popul.__init__(self, popsize, indsize, indivs)

    def initRandomPop(self):
        """
        Método para usar representações inteiras.
        :return:
        """
        self.indivs = []
        for _ in range(self.popsize):
            indiv_i = IndivInt(self.indsize, [], 0, self.ub)
            self.indivs.append(indiv_i)


class PopulReal(Popul):
    """
    Extensão da classe Popul com implementação do método initRandomPop
    """

    def __init__(self, popsize, indsize, lb=0.0, ub=1.0, indivs=[]):
        self.lb = lb
        self.ub = ub
        Popul.__init__(self, popsize, indsize, indivs)

    def initRandomPop(self):
        self.indivs = []
        for _ in range(self.popsize):
            indiv_i = IndivReal(self.indsize, [], lb=self.lb, ub=self.ub)
            self.indivs.append(indiv_i)
