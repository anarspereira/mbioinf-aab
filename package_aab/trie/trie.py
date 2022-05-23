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
        self.nodes = {0: {}} # dicionário de nodes
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
        :param symbol: símbolo de cada arco que sai de um node
        """
        self.num += 1 # indexa o nodo ao dicionário de nodes
        self.nodes[origin][symbol] = self.num
        self.nodes[self.num] = {} # cria novo node com um dicionário vazio

    def add_pattern(self, p):
        """
        Método que adiciona padrão à trie
        :param p: padrão, começa sempre na root
        """
        position = 0
        node = 0
        while position < len(p): # enquanto a posição do node for menor que o tamanho do padrão,
            if p[position] not in self.nodes[node].keys(): # se o caracter já estiver presente no node,
                self.add_node(node, p[position]) # é adicionado um caracter ao node
            node = self.nodes[node][p[position]] # define o node atual
            position += 1 # passa para a próxima posição

    def trie_from_patterns(self, pats):
        """
        Método que adiciona padrões à trie
        :param pats: padrões
        """
        for p in pats:
            self.add_pattern(p) # adiciona cada padrão presente na lista de padrões

    def prefix_trie_match(self, text: str) -> list:
        """
        Método de procura de padrões como prefixos da sequência text.
        Percorre a árvore (saindo do node raiz) e segue os arcos correspondentes.
        Se atingir uma folha, o padrão correspondente a esta folha é prefixo da sequência.
        :param text: sequência
        :return: match ou nada
        """
        position = 0 # posição inicial
        match = "" # match inicial (resultado)
        node = 0 # nó inicial
        while position < len(text): # enquanto a posição for menor que o tamanho do texto,
            if text[position] in self.nodes[node].keys(): # se o caracter estiver presente na árvore,
                node = self.nodes[node][text[position]] # guarda o node
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
        Método que identifica matches dos padrões em toda a sequência text.
        Processo iterativo - faz match da sequência, remove o primeiro símbolo desta, repete o processo -> o processo anterior é repetido para todos os sufixos da seq.
        :param text: sequência
        :return: lista de matches
        """
        res = []
        for i in range(len(text)): # para cada posição na sequência text,
            m = self.prefix_trie_match(text[i:]) # procura no padrão os caracteres da sequência txt e guarda o valor em m
            if m != None: # caso m seja diferente de none,
                res.append((i, m)) # é adicionado à lista do resultado um tuplo com a posição iterada e o padrão encontrado
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