# -*- coding: utf-8 -*-
"""
Package dos algoritmos implementados em aula
Algoritmos Avançados de Bioinformática
"""

"""
Class: Trie
"""

class Trie:
    """
    Classe responsável pela implementação da árvore de prefixos que permite fazer o pré-processamento
    de um conjunto de padrões. Os símbolos de um dado alfabeto estão associados aos arcos de uma árvore.
    A trie é construída a partir de um conjunto de padrões, começando pelo node da raiz e iterando
    cada padrão, adicionando os nós necessários para que a árvore contenha o caminho desde a raiz até à folha,
    representando o padrão.
    """
    #TODO -> pôr os métodos em camelcase
    def __init__(self):
        """
        Método que guarda os valores utilizados nos restantes métodos
        """
        self.nodes = {0: {}} # guarda um dicionário de nodes com a estrutura anterior.
        # keys: valores inteiros sequenciais;
        # values: arcos que saem desse nó (em dicionário vazio. keys: símbolos do arco; values: indíce dos destination
        # nodes) <- representa as folhas da árvore.
        self.num = 0 # guarda nº do último nó criado (nº de nodes de uma árvore).

    def print_trie(self) -> None:
        """
        Método que imprime a trie
        """
        for k in self.nodes.keys():
            print(k, "->", self.nodes[k])

    def add_node(self, origin: int, symbol: str) -> None:
        """
        Método que adiciona o nodo à trie
        Este método é usado pelo método add_pattern.

        :param origin: node existente
        :param symbol: caracter referente ao node que vai ser adicionado (identificação do arco)
        """
        self.num += 1 # adiciona um nó à árvore, aumentando o seu tamanho
        self.nodes[origin][symbol] = self.num # cria um novo node e liga-o a um já existente (através do parâmetro origin)
        self.nodes[self.num] = {} # cria novo node com um dicionário vazio

    def add_pattern(self, p: list) -> None:
        """
        Método que adiciona padrão à trie

        :param p: padrão do input
        """
        position = 0 # posição inicial do padrão. Itera os símbolos do padrão p, enquanto o node se mantém o node atual da árvore, começando pela raiz (node 0).
        node = 0
        while position < len(p): # enquanto a primeira posição do padrão for menor que o tamanho do padrão,
            if p[position] not in self.nodes[node].keys(): # se a posição inicial do padrão não estiver presente nas keys do dicionário de nodes (se ainda não existir um arco),
                self.add_node(node, p[position]) # é criado um novo nó (que irá ser considerado o current node e a iteração começará deste nó e não do anterior)
            node = self.nodes[node][p[position]] # se existir um arco na posição inicial do padrão, esse passará a ser o current node e a iteração começará deste node
            position += 1 # incrementar i em 1 para seguir para a próxima iteração, repetindo o processo até chegar ao fim do padrão (len(p)).

    def trie_from_patterns(self, pats: list) -> None:
        """
        Método que adiciona cada padrão do input à trie.

        :param pats: padrões do input
        """
        for p in pats:
            self.add_pattern(p) # adiciona cada padrão presente na lista de padrões

    def prefix_trie_match(self, text: str):
        """
        Método para procurar se um padrão da trie é um prefixo da sequência.
        Percorre a sequência de caracteres e a árvore, começando pela raiz, seguindo os arcos correspondentes aos
        caracteres da sequência até que ocorra uma das seguintes situações:
        - Se atingir uma folha da trie, o padrão foi identificado;
        - O caracter da sequência não existe -> não foi identificado nenhum padrão na trie.

        :param text: sequência de caracteres
        :return: match do prefixo ou None
        """
        position = 0 # posição inicial
        match = "" # match inicial (resultado)
        node = 0 # nó inicial
        while position < len(text): # enquanto a posição inicial for menor que o tamanho da sequência,
            if text[position] in self.nodes[node].keys(): # se a posição inicial da sequência estiver presente nas keys do dicionário de nodes,
                node = self.nodes[node][text[position]] # guarda o node atual
                match += text[position] # e dá match, adicionando o caracter ao padrão
                if self.nodes[node] == {}: # se atingir uma folha (dicionário vazio),
                    return match # retorna o padrão existente na árvore
                else: # se não atingir uma folha,
                    position += 1 # avança para a próxima posição
            else:
                return None # se o caracter não for encontrado, para o ciclo while
        return None

    def trie_matches(self, text: str) -> list:
        """
        Método para, usando o método prefix_trie_match, procurar por ocorrências (matches) do padrão na sequência.
        Processo iterativo - faz match da sequência, remove o primeiro símbolo desta, repete o processo -> o processo
        anterior é repetido para todos os sufixos da seq.

        :param text: sequência
        :return: lista de matches
        """
        res = []
        for i in range(len(text)): # para cada posição na sequência,
            m = self.prefix_trie_match(text[i:]) # procura no padrão os caracteres da sequência e guarda o valor em m
            if m != None: # caso m seja diferente de none,
                res.append((i, m)) # é adicionado à lista do resultado um tuplo com a posição iterada e o padrão encontrado
        return res


def test():
    patterns = ["GAT", "CCT", "GAG"]
    t = Trie()
    # t.trie_from_patterns(patterns)
    t.print_trie()
#
#
# def test2():
#     print("Test 2")
#     patterns = ["AGAGAT", "AGC", "AGTCC", "CAGAT", "CCTA", "GAGAT", "GAT", "TC"]
#     t = Trie()
#     t.trie_from_patterns(patterns)
#     #t.print_trie()
#     print("prefix trie match")
#     print(t.prefix_trie_match("GAGATCCTA"))
#     print("trie match")
#     print(t.trie_matches("GAGATCCTA"))


test()
# print()
# test2()