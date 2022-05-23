# -*- coding: utf-8 -*-

"""
Class: Trie
"""
class Trie:

    def __init__(self):
        """
        Método que guarda os valores utilizados nos restantes métodos

        :param nodes: guarda um dicionário de nodes
        :param num: guarda nº do último nó criado
        """
        self.nodes = {0: {}}
        self.num = 0

    def print_trie(self):
        """
        Método que imprime a trie
        """
        for k in self.nodes.keys():
            print(k, "->", self.nodes[k])

    def add_node(self, origin, symbol):
        """
        Método que adiciona o nodo à trie
        :param origin:
        :param symbol: símbolo de cada arco que sai de um nodo
        """
        self.num += 1
        self.nodes[origin][symbol] = self.num
        self.nodes[self.num] = {}

    def add_pattern(self, p):
        """
        Método que adiciona padrão à trie
        :param p: padrão a adicionar
        """
        position = 0
        node = 0
        while position < len(p):
            if p[position] not in self.nodes[node].keys():
                self.add_node(node, p[position])
            node = self.nodes[node][p[position]]
            position += 1

    def trie_from_patterns(self, pats):
        """
        Método que adiciona padrões à trie
        :param pats: padrões
        """
        for p in pats:
            self.add_pattern()

    def prefix_trie_match(self, text: str) -> list:
        """
        Método de procura de padrões como prefixos da sequência text.
        Percorre a árvore (saindo do node raiz) e segue os arcos correspondentes.
        Se atingir uma folha, o padrão correspondente a esta folha é prefixo da sequência.
        :param text: sequência
        :return:
        """
        position = 0 # posição inicial
        match = "" # match inicial (vazio)
        node = 0 # nó inicial
        while position < len(text): # enquanto a posição for menor que o tamanho do texto,
            if text[position] in self.nodes[node].keys():
                node = self.nodes[node][text[position]]
                match += text[position]
                if self.nodes[node] == {}:
                    return match
                else:
                    position += 1
            return None

        return None

    def trie_matches(self, text: str) -> list:
        """
        Método que identifica matches dos padrões em toda a sequência text.
        Processo iterativo - faz match da sequência, remove o primeiro símbolo desta, repete o processo -> o processo anterior é repetido para todos os sufixos da seq.
        :param text:
        :return:
        """
        res = []
        for i in range(len(text)):
            m = self.prefix_trie_match(text[i:])
            if m != None:
                res.append((i, m))
        return res


def test():
    patterns = ["GAT", "CCT", "GAG"]
    t = Trie()
    t.trie_from_patterns(patterns)
    t.print_trie()


def test2():
    patterns = ["AGAGAT", "AGC", "AGTCC", "CAGAT", "CCTA", "GAGAT", "GAT", "TC"]
    t = Trie()
    t.trie_from_patterns(patterns)
    print(t.prefix_trie_match("GAGATCCTA"))
    print(t.trie_matches("GAGATCCTA"))


test()
print()
test2()