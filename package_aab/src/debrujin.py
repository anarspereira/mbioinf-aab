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
    Esta classe é uma subclasse da MyGraph e, desta forma, herdará todos os métodos definidos na mesma.
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
        :param frags: um conjunto de sequências
        """
        for seq in frags: #para cada sequência em fragmentos
            suffix_seq = suffix(seq) #cria o sufixo da sequência
            self.add_vertex(suffix_seq) #adiciona o sufixo como um vertice ao grafo
            prefix_seq = prefix(seq) #cria o prefixo da sequência
            self.add_vertex(prefix_seq) #adiciona o prefixo como um vertice ao grafo
            self.add_edge(prefix_seq,suffix_seq) #adiciona o arco entre o prefixo e o sufixo

    def seq_from_path(self, path : lst) -> str:
        """
        Método que obtém a sequência a partir do caminho construído.
        :param path: caminho do grafo em lista
        :return: retorna a sequência representada pelo caminho construído
        """
        seq = path[0]
        #define o início da sequência como o primeiro nodo no caminho (nodo correspondente ao index 0 da lista path)
        for i in range(1, len(path)):
            #para cada nodo presente no caminho desde o nodo correspondente ao index 1 da lista do caminho (path)
            next = path[i] #define o próximo nodo como sendo o nodo no index seguinte da lista do caminho
            seq += next[-1] #adiciona o nodo à sequêcia
        return seq


def suffix(seq : str) -> str:
    """
    Método que obtém o sufixo da sequência obtido na método "seq_from_path".
    :param seq: sequência representada pelo caminho construído
    :return: retorna o sufixo da sequência seq, o que corresponde à sequência exceto o primeiro caracter
    """
    return seq[1:]


def prefix(seq : str) -> str:
    """
    Método que obtém o prefixo da sequência obtido na método "seq_from_path".
    :param seq: sequência representada pelo caminho construído
    :return: retorna o prefixo da sequência seq, o que corresponde à sequência exceto o último caracter
    """
    return seq[:-1]


def composition(k : int, seq : str) -> lst:
    """
    Método que recupera a sequência original, dando como valores de entrada a sequência obtida e o valor de k
    :param k: tamanho dos fragmentos
    :param seq: sequência obtida
    :return: retorna a sequência original em lista
    """
    seq_original = [] #criar lista vazia da sequência original
    for i in range(len(seq) - k + 1): #percorre a sequência, subtraindo o tamanho do fragmento e incrementando + 1
        seq_original.append(seq[i:i + k]) #adiciona à lista o fragmento de tamanho k
    seq_original.sort() #ordenar a lista
    return seq_original


#testes

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