# -*- coding: utf-8 -*-
"""
Package dos algoritmos implementados em aula
Algoritmos Avançados de Bioinformática
"""

"""
Class: SuffixTree - Árvore de sufixos
"""

class SuffixTree:
    """
    Classe que cria árvore de sufixos de um padrão que vai ser procurado numa sequência.
    Permite fazer o pré-processamento de uma sequência-alvo, tornando a sua procura mais eficiente.
    É a solução para fazer o pré-processamento de sequências muito grandes, descobrir quais árvores contêm um dado padrão,
    descobrir a substring comum mais longa num conjunto de sequências e calcular o máximo de overlap de um conjunto de
    sequências.
    """

    def __init__(self):
        """
        Método que guarda os valores utilizados nos restantes métodos.
        """
        self.nodes = {0: (-1, {})} # dicionário com tuplo de cada nodo
        # 1º elemento é a posição do sufixo (para folhas) ou -1 (se não for folha -> nodes internos)
        # 2º elemento corresponde a um dicionário
        # keys: símbolos do arco; values: indíce dos destination nodes <- representa as folhas da árvore
        self.num = 0

    def printTree(self) -> None:
        """
        Método que imprime a árvore de sufixos.
        """
        for k in self.nodes.keys():
            if self.nodes[k][0] < 0:
                print(k, "->", self.nodes[k][1])
            else:
                print(k, ":", self.nodes[k][0])

    def addNode(self, origin: int, symbol: str, leafnum = -1) -> None:
        """
        Método que adiciona os nós à árvore.
        :param origin: node atual
        :param symbol: caracter referente ao node que vai ser adicionado
        :param leafnum: número da folha (-1 é o default)
        """
        #print("Símbolo: ", symbol)
        #print("Nº da folha: ", leafnum)
        self.num += 1 # adiciona um nó à árvore, aumentando o seu tamanho
        self.nodes[origin][1][symbol] = self.num # cria um novo node e liga-o a um já existente (através do parâmetro origin)
        self.nodes[self.num] = (leafnum, {}) # cria novo node com o número da folha e um dicionário vazio

    def addSuffix(self, p: list, sufnum: int) -> None:
        """
        Método que adiciona sufixo à árvore.
        :param p: padrão
        :param sufnum: número do sufixo para as folhas ou -1 para não folhas
        """
        pos = 0 # posição inicial do padrão. Itera os símbolos do padrão p, enquanto o node se mantém o node atual da árvore, começando pela raiz (node 0)
        node = 0
        while pos < len(p): # enquanto a primeira posição do padrão for menor que o tamanho do padrão,
            if p[pos] not in self.nodes[node][1].keys(): # se a posição inicial do padrão não estiver presente nas keys do dicionário de nodes (se ainda não existir um arco),
                if pos == len(p) - 1: # se a posição inicial for a última do padrão,
                    self.addNode(node, p[pos], sufnum) # adiciona um node com o sufixo
                else: # caso contrário,
                    self.addNode(node, p[pos]) # não adiciona um sufixo
            node = self.nodes[node][1][p[pos]] # se existir um arco na posição inicial do padrão, esse passará a ser o current node e a iteração começará deste node
            pos += 1 # incrementar i em 1 para seguir para a próxima iteração, repetindo o processo até chegar ao fim do padrão (len(p)).

    def suffixTreeFromSeq(self, text: str) -> None:
        """
        Método que cria a árvore de sufixos, adicionando um símbolo ("$") no fim da sequência e chama o método anterior
        para cada sufixo da sequência -> nenhum sufixo será o prefixo de outro sufixo.
        :param text: sequência que será adicionada à árvore
        """
        t = text + "$" # adiciona "$" no fim do texto
        for i in range(len(t)): # para cada índice no range do tamanho do texto (com o $),
            self.addSuffix(t[i:], i) # adicionar sufixo em cada iteração

    def findPattern(self, pattern: str):
        """
        Método que procura padrões (trie) começando da raiz até chegar ao node final ou falhar a pesquisa.
        :param pattern: padrão a procurar
        :return: lista de folhas abaixo de um dado nó
        """
        pos = 0 # posição inicial
        node = 0 # node
        for pos in range(len(pattern)): # para cada posição ao longo do tamanho do padrão a procurar, começando pela raiz,
            if pattern[pos] in self.nodes[node][1].keys(): # se os arcos estão presentes no conjunto de símbolos do padrão,
                node = self.nodes[node][1][pattern[pos]] # adicionar o padrão ao node da árvore
            else: # se os arcos não estão presentes no conjunto de símbolos do padrão,
                return None # retorna none -> o padrão não ocorre
        return self.getLeavesBelow(node) # no fim do ciclo for, retorna o conjunto de folhas abaixo de um dado nó usando o método auxiliar get_leaves_below implementado recursivamente

    def getLeavesBelow(self, node: int) -> list:
        """
        Método auxiliar para colecionar todas as folhas abaixo de um dado nó.
        :param node: node a partir do qual se procuram as informações das folhas abaixo deste
        :return: lista de folhas abaixo de um dado nó
        """
        res = [] # lista vazia que irá conter as folhas abaixo de um dado nó e que será retornada
        if self.nodes[node][0] >= 0: # se a folha com o padrão em questão for encontrada,
            res.append(self.nodes[node][0]) # a folha é adicionada à lista final
        else: # caso contrário,
            for k in self.nodes[node][1].keys(): # para cada caracter do node,
                newnode = self.nodes[node][1][k] # é criado um novo node com esse caracter
                leaves = self.getLeavesBelow(newnode) # é criada uma folha com o novo node
                res.extend(leaves)
        return res