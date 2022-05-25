# -*- coding: utf-8 -*-
"""
Package dos algoritmos implementados em aula
Algoritmos Avançados de Bioinformática
"""
"""
Class: SuffixTree - Árvore de sufixos

É construída uma árvore de sufixos para procurar padrões.
A árvore contém os ramos dos sufixos do padrão TACTA$ (TACTA$, ACTA$, CTA$, TA$, A$, $).
Começando do primeiro caracter do padrão (string) e da raiz da ST:
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
        self.nodes = {0: (-1, {})} # dicionário com tuplo de cada nodo
        # 1º elemento é o nº do sufixo (para folhas) ou -1 (se não for folha)
        # 2º elemento corresponde a um dicionário
        self.num = 0

    def print_tree(self) -> None:
        """
        Método que imprime a árvore de sufixos.
        """
        for k in self.nodes.keys():
            if self.nodes[k][0] < 0:
                print(k, "->", self.nodes[k][1])
            else:
                print(k, ":", self.nodes[k][0])

    def add_node(self, origin: str, symbol: str, leafnum = -1) -> None:
        """
        Método que adiciona os nós à árvore.
        :param origin: node atual
        :param symbol: caracter referente ao node que vai ser adicionado
        :param leafnum: número da folha
        """
        print("Símbolo: ", symbol)
        print("Nº da folha: ", leafnum)
        self.num += 1 # indexa o nodo ao dicionário de nodes
        self.nodes[origin][1][symbol] = self.num
        self.nodes[self.num] = (leafnum, {}) # cria novo node com o número da folha e um dicionário vazio

    def add_suffix(self, p: list, sufnum: int) -> None:
        """
        Método que adiciona sufixo
        :param p: padrão
        :param sufnum: número do sufixo para as folhas ou -1 para não folhas
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

    def suffix_tree_from_seq(self, text: str) -> None:
        """
        Método que cria a árvore de sufixos, adicionando um sufixo em cada iteração
        :param text: sequência que será adicionada à árvore
        """
        t = text + "$" # adiciona $ no fim do texto
        for i in range(len(t)): # para cada índice no range do tamanho do texto (com o $),
            self.add_suffix(t[i:], i) # adicionar sufixo em cada iteração

    def find_pattern(self, pattern: str):
        """
        Método que procura padrões (trie)
        :param pattern: padrão a procurar
        :return: #TODO: ver o que retorna
        """
        pos = 0 # posição
        node = 0 # node
        for pos in range(len(pattern)): # para cada posição no range do tamanho do padrão a procurar,
            if pattern[pos] in self.nodes[node][1].keys(): # se o padrão, na posição em questão, estiver presente no dicionário de nodes,
                node = self.nodes[node][1][pattern[pos]] # adicionar o padrão ao node
            else: # se o padrão não estiver presente no dicionário de nodes,
                return None # retorna none
        return self.get_leafes_below(node) # no fim do ciclo for, retorna o conjunto de folhas abaixo de um dado nó

    def get_leafes_below(self, node) -> list: #TODO: type hinting
        """
        Método auxiliar para colecionar todas as folhas abaixo de um dado nó
        :param node: node a partir do qual se procuram as informações das folhas abaixo deste
        :return: lista de folhas abaixo de um dado nó
        """
        res = [] # lista vazia que irá conter as folhas abaixo de um dado nó e que será retornada
        if self.nodes[node][0] >= 0: # se a folha com o padrão em questão for encontrada,
            res.append(self.nodes[node][0]) # a folha é adicionada à lista final
        else: # caso contrário,
            for k in self.nodes[node][1].keys(): # para cada caracter do node,
                newnode = self.nodes[node][1][k] # é criado um novo node com esse caracter
                leafes = self.get_leafes_below(newnode) # é criada uma folha com o novo node
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
    #print(st.repeats(2, 2))


test()
print()
test2()