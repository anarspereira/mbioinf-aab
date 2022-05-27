# -*- coding: utf-8 -*-
"""
Package dos algoritmos implementados em aula
Algoritmos Avançados de Bioinformática
"""

"""
Class: DeBruijn Graph
"""

from my_graph import MyGraph

class DeBruijnGraph(MyGraph):
    """
    Classe implementada para representar os grafos de Bruijn. Estes representam os fragmentos (k-mers) como
    arcos do grafo e os nodos como sequências de tamanho k-1, correspondendo a prefixos ou sufixos dos
    fragmentos.
    Esta classe é uma subclasse do MyGraph e, desta forma, herdará todos os métodos definidos na mesma.
    """

    def __init__(self, frags : lst):
        """
        Método construtor que guarda os valores utilizados nos restantes métodos
        :param frags: um conjunto de sequências (k-mers)
        """
        MyGraph.__init__(self, {})
        self.create_deBruijn_graph(frags)

    def add_edge(self, o : str, d : str):
        """
        Método que adiciona o arco (o,d) ao grafo, verificando se este já não existe no mesmo
        :param o: vertice do arco
        :param d: vertice do arco
        """
        if o not in self.graph.keys(): #se o vertice o não existe
            self.add_vertex(o) #adiciona vertice o
        if d not in self.graph.keys(): #se o vertice d não existe
            self.add_vertex(d) #adiciona vertice d
        self.graph[o].append(d) #adiciona o valor d ao vertice o

    def in_degree(self, v : str) -> int:
        """
        Método que calcula o grau de entrada do nodo v
        :param v: nodo
        :return: retorna grau de entrada do nodo
        """
        count_nodes = 0
        for k in self.graph.keys(): #para cada nodo no grafo
            if v in self.graph[k]: #se o nodo v se encontra no grafo
                count_nodes += self.graph[k].count(v) #contagem dos nodos presentes no grafo
        return count_nodes

    def create_deBruijn_graph(self, frags : lst):
        """
        Método que implementa a criação de um grafo DeBruijn
        :param frags: um conjunto de sequências (fragmentos)
        :return:
        """
        for seq in frags: #para cada sequência em fragmentos
            suffix_seq = suffix(seq) #cria o sufixo da sequência
            self.add_vertex(suf) #adiciona o sufixo como um vertice ao grafo
            prefix_seq = prefix(seq) #cria o prefixo da sequência
            self.add_vertex(pref) #adiciona o prefixo como um vertice ao grafo
            self.add_edge(pref,suf) #adiciona o arco entre o prefixo e o sufixo

    def seq_from_path(self, path):
        seq = path[0]
        for i in range(1, len(path)):
            nxt = path[i]
            seq += nxt[-1]
        return seq


def suffix(seq):
    return seq[1:]


def prefix(seq):
    return seq[:-1]


def composition(k, seq):
    res = []
    for i in range(len(seq) - k + 1):
        res.append(seq[i:i + k])
    res.sort()
    return res


def test1():
    frags = ["ATA", "ACC", "ATG", "ATT", "CAT", "CAT", "CAT", "CCA", "GCA", "GGC", "TAA", "TCA", "TGG", "TTC", "TTT"]
    dbgr = DeBruijnGraph(frags)
    dbgr.print_graph()


def test2():
    frags = ["ATA", "ACC", "ATG", "ATT", "CAT", "CAT", "CAT", "CCA", "GCA", "GGC", "TAA", "TCA", "TGG", "TTC", "TTT"]


dbgr = DeBruijnGraph(frags)
dbgr.print_graph()
print(dbgr.check_nearly_balanced_graph())
print(dbgr.eulerian_path())


def test3():
    orig_sequence = "ATGCAATGGTCTG"
    frags = composition(3, orig_sequence)
    # ... completar


test1()
print()
# test2()
# print()
# test3()