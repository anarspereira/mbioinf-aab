# -*- coding: utf-8 -*-
"""
Package dos Algoritmos implementados em aula
Algoritmos Avançados de Bioinformática
"""
"""
Class: SuffixTree

É construída uma árvore de sufixos para procurar padrões.
Começando do primeiro caracter (duvidoso, não deveria ser último?) do padrão e raiz da ST:
- Para o caracter atual do padrão, se houver uma aresta do nó atual da ST, percorrer a aresta. Se não houver, volta à raiz;
- Se não houver aresta, o padrão não existe e não retorna nada;
Se todos os caracteres do padrão foram lidos, ou seja, se existe um caminho desde a raiz para os caracteres de um dado padrão, esse padrão foi encontrado.

Aplicações:
- Procura de padrões;
- Encontrar a maior substring repetida;
- Encontrar o maior palindromo numa string;
- Encontrar os lowest common ancestors;
- Encontrar a maior substring comum;
- Match exato de uma string
"""

class SuffixTree:
    """
    Classe que cria árvore de sufixos de um padrão que vai ser procurado numa sequência
    """

    def __init__(self):
        """
        Método que guarda os valores nos restantes métodos.
        """
        self.nodes = {0: (-1, {})} # tuplo de cada nó
        # 1º elemento é o nº do sufixo (para folhas) ou -1 (se não for folha)
        # 2º elemento corresponde a um dicionário
        self.num = 0

    def print_tree(self):
        """
        Método para imprimir a raiz
        """
        for k in self.nodes.keys():
            if self.nodes[k][0] < 0:
                print(k, "->", self.nodes[k][1])
            else:
                print(k, ":", self.nodes[k][0])

    def add_node(self, origin, symbol, leafnum = -1):
        """
        Método que adiciona os nós à árvore
        :param origin:
        :param symbol:
        :param leafnum:
        """
        self.num += 1
        self.nodes[origin][1][symbol] = self.num
        self.nodes[self.num] = (leafnum, {})

    def add_suffix(self, p, sufnum):
        """
        Método que adiciona sufixo
        :param p:
        :param sufnum:
        :return:
        """
        pos = 0
        node = 0
        while pos < len(p):
            if p[pos] not in self.nodes[node][1].keys():
                if pos == len(p) - 1:
                    self.add_node(node, p[pos], sufnum)
                else:
                    self.add_node(node, p[pos])
            node = self.nodes[node][1][p[pos]]
            pos += 1

    def suffix_tree_from_seq(self, text):
        """
        Método que cria a árvore de sufixos, adicionando um sufixo em cada iteração
        :param text:
        :return:
        """
        t = text + "$"
        for i in range(len(t)):
            self.add_suffix(t[i:], i)

    def find_pattern(self, pattern):
        """
        Método que procura padrões (trie)
        :param pattern:
        :return:
        """
        pos = 0
        node = 0
        for pos in range(len(pattern)):
            if pattern[pos] in self.nodes[node][1].keys():
                node = self.nodes[node][1][pattern[pos]]
            else:
                return None
        return self.get_leafes_below(node)

    def get_leafes_below(self, node):
        """
        Método auxiliar para colecionar todas as folhas abaixo de um dado nó
        :param node:
        :return:
        """
        res = []
        if self.nodes[node][0] >= 0:
            res.append(self.nodes[node][0])
        else:
            for k in self.nodes[node][1].keys():
                newnode = self.nodes[node][1][k]
                leafes = self.get_leafes_below(newnode)
                res.extend(leafes)
        return res


def test():
    seq = "TACTA"
    st = SuffixTree()
    st.suffix_tree_from_seq(seq)
    st.print_tree()
    print(st.find_pattern("TA"))
    print(st.find_pattern("ACG"))


def test2():
    seq = "TACTA"
    st = SuffixTree()
    st.suffix_tree_from_seq(seq)
    print(st.find_pattern("TA"))
    print(st.repeats(2, 2))


test()
print()
test2()