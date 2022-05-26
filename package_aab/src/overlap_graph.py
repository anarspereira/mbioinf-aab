# -*- coding: utf-8 -*-
"""
Package dos algoritmos implementados em aula
Algoritmos Avançados de Bioinformática
"""

"""
Class: OverlapGraph
Será uma sub-classe da classe MyGraph para representar grafos orientados
"""

from my_graph import MyGraph


class OverlapGraph(MyGraph):
    """
    A classe OverlapGraph será uma sub-classe da classe MyGraph para representar grafos orientados
    """

    #def __init__(self, frags):
    #    MyGraph.__init__(self, {})
    #    self.create_overlap_graph(frags)

    def __init__(self, frags, reps = False):
        if reps:
            self.create_overlap_graph_with_reps(frags)
        else:
            self.create_overlap_graph(frags)
        self.reps = reps

    ## create overlap graph from list of sequences (fragments)
    def create_overlap_graph(self, frags):
        """
        Método para criar o grafo de overlap a partir das ligações do sufixos com os prefixos
        :param frags: fragmentos ou conjuntos de sequencias
        :return:
        """
        for seq in frags:
            self.add_vertex(seq) #adiciona vertices
        for seq in frags:
            suf = suffix(seq)
            for seq2 in frags:
                if prefix(seq2) == suf: #serve para definir os arcos
                    self.add_edge(seq, seq2) #adiciona arcos


    def create_overlap_graph_with_reps(self, frags):
        """
        Método para criar grafo de overlap com repetições de elementos
        :param frags: fragmentos ou conjuntos de sequencias
        :return:
        """
    #repetição caso exista repetição de elementos
        idnum = 1
        for seq in frags:
            self.add_vertex(seq + "-" + str(idnum))
            idnum = idnum + 1
        idnum = 1
        for seq in frags:
            suf = suffix(seq)
            for seq2 in frags:
                if prefix(seq2) == suf:
                    for x in self.get_instances(seq2):
                        self.add_edge(seq + "-" + str(idnum), x)
            idnum = idnum + 1

    def get_instances(self, seq):
        """

        :param seq: sequencia
        :return: a lista da sequencia
        """
        res = []
        for k in self.graph.keys():
            if seq in k: res.append(k)
        return res

    def get_seq(self, node):
        """
        Método que retorna o nodo
        :param node: nodo
        :return:
        """
        if node not in self.graph.keys():
            return None
        if self.reps:
            return node.split("-")[0]
        else:
            return node

    def seq_from_path(self, path):
        """
        Método para dar a sequencia contruida dado um caminho no grafo
        :param path: caminho
        :return:
        """
        if not self.check_if_hamiltonian_path(path):
            return None
        seq = self.get_seq(path[0])
        for i in range(1, len(path)):
            nxt = self.get_seq(path[i])
            seq += nxt[-1]
        return seq

#funções auxiliares
def composition(k, seq):
    """
    Método da composição
    :param k: valor de k, numero de nucléotidos
    :param seq: sequencia
    :return:
    """
    res = []
    for i in range(len(seq) - k + 1):
        res.append(seq[i:i + k])
    res.sort()
    return res


def suffix(seq):
    """
    Método do sufixo
    :param seq: sequencia
    :return: a sequencia sem o primeiro elemento
    """
    return seq[1:]


def prefix(seq):
    """
    Método do prefixo
    :param seq: sequencia
    :return: a sequencia sem o ultimo nucleotido
    """
    return seq[:-1]


# testing / mains
def test1():
    seq = "CAATCATGATG"
    k = 3
    print(composition(k, seq))


def test2():
    frags = ["ACC", "ATA", "CAT", "CCA", "TAA"]
    ovgr = OverlapGraph(frags, False)
    ovgr.print_graph()


def test3():
    frags = ["ATA", "ACC", "ATG", "ATT", "CAT", "CAT", "CAT", "CCA", "GCA", "GGC", "TAA", "TCA", "TGG", "TTC", "TTT"]
    ovgr = OverlapGraph(frags, True)
    ovgr.print_graph()


##def test4():
##    frags = ["ATA", "ACC", "ATG", "ATT", "CAT", "CAT", "CAT", "CCA", "GCA", "GGC", "TAA", "TCA", "TGG", "TTC", "TTT"]
##    ovgr = OverlapGraph(frags, True)
##    path = ['ACC−2', 'CCA−8', 'CAT−5', 'ATG−3']
##    print(ovgr.check_if_valid_path(path))
##    print(ovgr.check_if_hamiltonian_path(path))
##    path2 = ['ACC−2', 'CCA−8', 'CAT−5', 'ATG−3', 'TGG−13', 'GGC−10', 'GCA−9', 'CAT−6', 'ATT−4','TTT−15', 'TTC−14', 'TCA−12', 'CAT−7', 'ATA−1', 'TAA−11']
##    print(ovgr.check_if_valid_path(path2))
##    print(ovgr.check_if_hamiltonian_path(path2))
##    print(ovgr.seq_from_path(path2))


def test5():
    frags = ["ATA", "ACC", "ATG", "ATT", "CAT", "CAT", "CAT", "CCA", "GCA", "GGC", "TAA", "TCA", "TGG", "TTC", "TTT"]
    ovgr = OverlapGraph(frags, True)

    path = ovgr.search_hamiltonian_path()
    print(path)
    print(ovgr.check_if_hamiltonian_path(path))
    print(ovgr.seq_from_path(path))


def test6():
    orig_sequence = "CAATCATGATGATGATC"
    frags = composition(3, orig_sequence)
    print(frags)
    ovgr = OverlapGraph(frags, True)
    ovgr.print_graph()
    path = ovgr.search_hamiltonian_path()
    print(path)
    print(ovgr.seq_from_path(path))


test1()
print()
test2()
print()
# test3()
# print()
# test4()
# print()
# test5()
# print()
# test6()