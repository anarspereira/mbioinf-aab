# -*- coding: utf-8 -*-
"""
Package dos algoritmos implementados em aula
Algoritmos Avançados de Bioinformática
"""

"""
Class: MyGraph
"""

class MyGraph:
    """
    Classe para a implementação de grafos
    """
    def __init__(self, g: dict = {}):
        """
        Método que guarda os valores utilizados nos restantes métodos
        :param g: é um dicionário em que guarda o grafo
        """
        self.graph = g

    def print_graph(self):
        """
        Método que imprime o conteúdo do grafo como lista de adjacência
        """
        for v in self.graph.keys():
            print(v, " -> ", self.graph[v])

    def get_nodes(self) -> list:
        """
        Método que retorna a lista de nodos
        """
        return list(self.graph.keys())

    def get_edges(self) -> list:
        """
        Método que retorna a lista de arcos
        v será a origem
        d será o destino
        """
        edges = []
        for v in self.graph.keys():
            for d in self.graph[v]:
                edges.append((v, d)) #os arcos são o par de nodos anterior e seguinte
        return edges

    def size(self):
        """
        Método que retorna o tamanho do grafo, nomeadamente número de nodos e o número de arcos
        """

        return len(self.get_nodes()), len(self.get_edges())

    def add_vertex(self, v:str):
        """
        Método que adiciona o nodo v ao grafo
        :param v: nodo
        """
        if v not in self.graph.keys(): #caso v não exista, é adicionado
            self.graph[v] = []

    def add_edge(self, o:str, d:str):
        """
        Método que adiciona o arco (o,d) ao grafo
        :param o: vertice do arco
        :param d: vertice do arco
        :return:
        """
        ''' Add edge to the graph; if vertices do not exist, they are added to the graph '''
        if o not in self.graph.keys(): #se o não exista, é adicionado vertice o
            self.add_vertex(o)
        if d not in self.graph.keys(): #verifica se o vertice d está no dicionário, caso não esteja é adicionado
            self.add_vertex(d)
        if d not in self.graph[o]: #verifica se o vertice d é um valor de vertice o
            self.graph[o].append(d) #adiciona o valor d ao o

    def get_successors(self, v:str):
        """
        :param v: nodo
        :return: retorna lista de nodos sucessores do nodo v
        """
        return list(
            self.graph[v])

    def get_predecessors(self, v:str) -> list:
        """
        :param v: nodo
        :return: retorna lista de nodos antecessores do nodo v
        """
        res = []
        for k in self.graph.keys():
            if v in self.graph[k]:
                res.append(k)
        return res

    def get_adjacents(self, v:str) -> list:
        """
        :param v: nodo
        :return: retorna a lista de nodos adjacentes do nodo v
        """
        suc = self.get_successors(v)
        pred = self.get_predecessors(v)
        res = pred
        for p in suc:
            if p not in res: res.append(p)
        return res


    def out_degree(self, v:str) -> int:
        """
        Método que calcula grau de saída do nodo v
        :param v: nodo
        :return: retorna grau de saída do nodo
        """
        return len(self.graph[v])

    def in_degree(self, v:str) -> int:
        """
        Método que calcula grau de entrada do nodo v
        :param v: nodo
        :return: retorna grau de entrada do nodo
        """
        return len(self.get_predecessors(v))

    def degree(self, v:str) -> int:
        """
        Método que calcula grau do nodo v (todos os nodos adjacentes quer percursores quer sucessores
        :param v: nodo
        :return: retorna grau do nodo v
        """
        return len(self.get_adjacents(v))

    def all_degrees(self, deg_type="inout") -> dict:
        """
        Método do cálculo de graus de entrada e saída, ou ambos para todos os nodos do grafo
        :param deg_type: tipo de grau (entrada, saída ou ambos)
        :return: retorna os graus
        """
        degs = {}
        for v in self.graph.keys():
            if deg_type == "out" or deg_type == "inout": #Se for graus de saida ou de entrada e saída
                degs[v] = len(self.graph[v]) #
            else:
                degs[v] = 0
        if deg_type == "in" or deg_type == "inout": #Se for graus de entrada ou de entrada e saída
            for v in self.graph.keys(): #para cada key no grafo
                for d in self.graph[v]: #para cada valor de v
                    if deg_type == "in" or v not in self.graph[d]: #Se for graus de entrada ou v não for um valor de d no grafo
                        degs[d] = degs[d] + 1   #adiciona +1 ao valor de d
        return degs

    def highest_degrees(self, all_deg=None, deg_type="inout", top=10) ->list:
        """
        Método que calcula graus mais elevados
        :param all_deg: graus de entrada e saída, ou ambos
        :param deg_type:tipo de grau (entrada, saída ou ambos)
        :return: lista de graus mais elevados
        """
        if all_deg is None:
            all_deg = self.all_degrees(deg_type)
        ord_deg = sorted(list(all_deg.items()), key=lambda x: x[1], reverse=True)
        return list(map(lambda x: x[0], ord_deg[:top]))


    def mean_degree(self, deg_type="inout") -> dict:
        """
        Método para calcular a media de graus
        :param deg_type: tipo de grau (entrada, saída ou ambos)
        :return: retorna a média de graus
        """
        degs = self.all_degrees(deg_type)
        return sum(degs.values()) / float(len(degs))

    def prob_degree(self, deg_type="inout") -> dict:
        """
        Método para calcular a probabilidade de graus
        :param deg_type: tipo de grau (entrada, saída ou ambos)
        :return: retorna a probabilidade de graus
        """
        degs = self.all_degrees(deg_type)
        res = {}
        for k in degs.keys():
            if degs[k] in res.keys():
                res[degs[k]] += 1
            else:
                res[degs[k]] = 1
        for k in res.keys():
            res[k] /= float(len(degs))
        return res

        ## BFS and DFS searches

    def reachable_bfs(self, v):
        """
        Método de nodos atingíveis a partir de v
        começa pelo nó de origem, depois visita todos os seus sucessores, seguindo-se pelos seus sucessores,
        até que todos os nós possíveis sejam visitados
        :param v: nodo
        :return: retorna lista de nodos atingíveis a partir de v
        """
        l = [v]
        res = []
        while len(l) > 0: #enquanto há elementos na lista l
            node = l.pop(0) #isolar o primeiro elemento da lista l, queue de nodos
            if node != v: res.append(node) #se o nodo for diferente de v, adicionar o nodo a res
            for elem in self.graph[node]: #para todos os sucessores do nodo
                if elem not in res and elem not in l and elem != node: #se não existe em res e em l e se o sucessor é diferente do nodo
                    l.append(elem) #adicionar na queue para verificar
        return res

    def reachable_dfs(self, v):
        """
        Método de nodos atingíveis a partir de v, da esquerda para a direita (em profundidade)
        começa pelo nó de origem, explora o seu primeiro sucessor, depois o seu primeiro sucessor,
        até que não seja possível qualquer outra exploração, e depois volta para explorar mais alternativas.
        :param v: nodo
        :return: retorna lista de nodos atingíveis a partir de v
        """
        l = [v]
        res = []
        while len(l) > 0: #enquanto há elementos na lista l, queue de nodos
            node = l.pop(0) #isolar o primeiro elemento da lista l
            if node != v: res.append(node) #se o nodo for diferente de v, adicionar o nodo a res
            s = 0 #ira ser usado para criar o stack//é reposto a 0 antes do loop for abaixo
            for elem in self.graph[node]: #para todos os sucessores do nodo
                if elem not in res and elem not in l: #se não existe em res e em l e se o sucessor é diferente do nodo
                    l.insert(s, elem) #cria um stack/vai voltar a verificar o mais recente/insere no inicio da lista
                    s += 1 #caso haja multiplos sucessores, o s vai aumentar de forma a colocar as proximas iteraçoes na posicao depois da iteraçao anterior (stack)
        return res

    def distance(self, s, d):
        """
        Método da distância entre nodos s e d
        :param s: nodo s
        :param d: nodo d
        :return: retorna a distancia entre nodos s e d
        """
        if s == d:
            return 0
        l = [(s, 0)] #lista com os tuplos do nodo e a distância
        visited = [s] #nodos visitados
        while len(l) > 0: #enquanto há elementos na lista l, queue de nodos
            node, dist = l.pop(0) #isolar o primeiro elemento da lista l
            for elem in self.graph[node]: #para todos os sucessores do nodo
                if elem == d: #
                    return dist + 1 #
                elif elem not in visited:
                    l.append((elem, dist + 1))
                    visited.append(elem)
        return None

    def shortest_path(self, s, d):
        """
        Método do caminho mais curto entre s e d (lista de nodos por onde passa)
        :param s: nodo s
        :param d: nodo d
        :return: retorna caminho mais curto, lista de nodos por onde passa
        """
        if s == d:
            return []
        l = [(s, [])] #lista com um tuplo com o nodo e o caminho
        visited = [s] #nodos visitados
        while len(l) > 0:
            node, preds = l.pop(0)
            for elem in self.graph[node]:
                if elem == d:
                    return preds + [node, elem]
                elif elem not in visited:
                    l.append((elem, preds + [node]))
                    visited.append(elem)
        return None

    def reachable_with_dist(self, s: str):
        """
        Método de nodos atingíveis a partir de v com respetiva distância
        :param s: nodo
        :return: retorna lista de pares nodos, distância
        """
        res = []
        l = [(s, 0)] #lista com tuplo com s e distância de s a s(0)
        while len(l) > 0: #enquanto há elementos na lista l, queue de nodos
            node, dist = l.pop(0)
            if node != s: #se nodo for diferente de s
                res.append((node, dist)) #não conta o s
            for elem in self.graph[node]: #para
                if not is_in_tuple_list(l, elem) and not is_in_tuple_list(res, elem): # vai ver se o p se encontra dentro de l ou em res
                    l.append((elem, dist + 1)) # adiciona o vertice a que se liga
        return res

    def mean_distances(self):
        """
        Método da média das distâncias de cada nodo
        :return: retorna a distância média e a proporção de nodos atingíveis
        """
        total = 0
        num_reachable = 0 #números de nodos no grafo ligados entre si
        for k in self.graph.keys(): #para cada key no grafo
            distsk = self.reachable_with_dist(k) #a lista correspondente aos nodos atingidos e a respetiva distância
            for _, dist in distsk: #para cada carater correspondente à distancia na lista
                total += dist #vamos adicionar o valor da distância ao total
            num_reachable += len(distsk) #número de nodos atingidos vai corresponder ao comprimento da lista (distsk) obtida, todas as ligações entre todos os nodos
        meandist = float(total) / num_reachable #média da distancia total dos nodos atingidos
        n = len(self.get_nodes()) #número total de nodos
        return meandist, float(num_reachable) / ((n - 1) * n)

    def closeness_centrality(self, node: str) ->:
        """
        Método de aproximação média das distâncias percorridas entre os nodos atingidos
        :param nodo: nodo
        :return: retorna a média das distâncias entre os nodos atingidos
        """
        dist = self.reachable_with_dist(node) #a lista correspondente aos nodos atingidos e a respetiva distância
        if len(dist) == 0: #se o número de nodos atingidos for igual a 0
            return 0.0 #retorna 0
        s = 0.0
        for d in dist: s += d[1] #para cada nodo é adicionada a distância à variavel s
        return len(dist) / s

    def highest_closeness(self, top=10) -> list:
        cc = {} #dicionário
        for k in self.graph.keys(): #para cada key no grafo
            cc[k] = self.closeness_centrality(k) #nodo corresponde
        ord_cl = sorted(list(cc.items()), key=lambda x: x[1], reverse=True)
        return list(map(lambda x: x[0], ord_cl[:top]))

    def betweenness_centrality(self, node) -> float:
        total_sp = 0
        sps_with_node = 0
        for s in self.graph.keys():
            for t in self.graph.keys():
                if s != t and s != node and t != node:
                    sp = self.shortest_path(s, t)
                    if sp is not None:
                        total_sp += 1
                        if node in sp: sps_with_node += 1
        return sps_with_node / total_sp

    ## cycles
    def node_has_cycle(self, v):
        """
        Método para verificar de o nodo tem ciclo, ou seja se começa e termina no mesmo nó
        :param v: nodo
        :return: valor de "False" ou "True" se o nodo não tem ou tem ciclo, respetivamente
        """
        l = [v] #vai buscar o nodo v e cria uma lista
        res = False
        visited = [v] #lista de nodos visitados
        while len(l) > 0: #enquanto há elementos na lista l, queue de nodos
            node = l.pop(0) #isolar o primeiro elemento da lista l
            for elem in self.graph[node]: #para cada elemento vai buscar ao grafo (dicionário) o nodo adjacente
                if elem == v:   #se o elemento da lista corresponder ao nodo
                    return True
                elif elem not in visited: #caso o elemento da lista não corresponder ao nodo visitado
                    l.append(elem) #adiciona o elemento à lista l
                    visited.append(elem) #adiciona o elemento à lista de nodos visitados
        return res #retorna False

    def has_cycle(self) -> bool:
        """
        Método que verifica se o grafo tem ciclo, ou seja se o caminho é fechado
        :return: valor de "False" ou "True" se o caminho é não fechado ou fechado, respetivamente.
        """
        res = False
        for v in self.graph.keys():  #para cada nodo vai buscar ao grafo (dicionário) o nodo adjacente
            if self.node_has_cycle(v): #se o nodo tiver ciclo
                return True
        return res #retorna False

    ## clustering

    def clustering_coef(self, v) -> float:
        """
        Método de cálculo do coeficiente de clustering, para medir até que ponto cada nó está inserido num grupo coeso
        :param v: nodo
        :return: coeficente de clustering
        """
        adjs = self.get_adjacents(v) #lista de nodos adjacentes
        if len(adjs) <= 1: #se o número de nodos adjacentes for inferior ou igual a 1, só terá 1 ou 0 nodos adjacentes
            return 0.0 #logo, não tem nodos suficientes para formar pares
        ligs = 0
        for i in adjs: #para cada nodo i (anterior) adjacente
            for j in adjs: #para cada nodo j (seguinte) adjacente
                if i != j: #se nodo i diferente de nodo j
                    if j in self.graph[i] or i in self.graph[j]: #se nodo j estiver no grafo adjacente a i ou i estiver no grafo adjacente a j
                        ligs = ligs + 1
        return float(ligs) / (len(adjs) * (len(adjs) - 1))
        #o número de pares de nodos adjacentes a dividir pelo número de pares que é possivel serem formados

    def all_clustering_coefs(self) -> dict:
        """
        Método que calcula todos os coeficientes
        :return: dicionário de coeficientes de cada nodo em que a key corresponde a cada nodo e a cada coeficiente
        """
        ccs = {} #dicionário de coeficientes
        for k in self.graph.keys(): #para cada key no grafo
            ccs[k] = self.clustering_coef(k)
            #cálculo do coeficiente de cada nodo, valor adicionado no dicionário ccs
        return ccs

    def mean_clustering_coef(self) -> float:
        """
        Método da média global dos coeficientes
        :return: o valor da média de todos os coeficientes
        """
        ccs = self.all_clustering_coefs() #cálculo de todos os coeficientes
        return sum(ccs.values()) / float(len(ccs)) #cálculo da média

    def mean_clustering_perdegree(self, deg_type="inout") -> dict:
        """
        Método que calcula valores para a média dos coeficientes para todos os nodos
        :param deg_type: tipo de grau (entrada, saída ou ambos)
        :return: retorna o dicionário de nodos e o respetivo coeficiente
        """
        degs = self.all_degrees(deg_type) #graus de entrada e saída, ou ambos para todos os nodos do grafo
        ccs = self.all_clustering_coefs() #coeficiente de todos os nodos em dicionário
        degs_k = {} #dicionário de grau k
        for k in degs.keys(): #para cada k grau
            if degs[k] in degs_k.keys(): #se cada grau k de entrada e saída, ou ambos está dentro
                degs_k[degs[k]].append(k) #o que estava no dicionário passa para uma lista
            else: #senão
                degs_k[degs[k]] = [k] #grau k permanece no dicionário
        ck = {} #dicionário da média dos coeficientes considerando nodos de grau k.
        for k in degs_k.keys():#para cada k grau
            tot = 0
            for v in degs_k[k]: tot += ccs[v]
            #para grau v calcular o total, o coeficiente de todos os nodos (dicionário)
            ck[k] = float(tot) / len(degs_k[k])
            #calcula o coeficiente a dividir pelo comprimento do grau k
        return ck

    ## Hamiltonian

    def check_if_valid_path(self, p:list) -> bool:
        """
        método de verificação se caminho é correto
        :param p:caminho
        :return: valor de "False" ou "True" se o caminho for inválido ou válido, respetivamente.
        """
        if p[0] not in self.graph.keys(): #se o primeiro nodo do caminho não pertencer ao grafo
            return False #caminho inválido
        for i in range(1, len(p)): #para cada nodo no caminho
            if p[i] not in self.graph.keys() or p[i] not in self.graph[p[i - 1]]:
                #se o nodo não pertencer ao grafo ou não for o primeiro no caminho
                return False #caminho inválido
        return True #caminho válido

    def check_if_hamiltonian_path(self, p:list) -> bool:
        """
        Método verificação se caminho é Hamiltonian
        :param p: caminho
        :return: valor de "False" ou "True" se o caminho hamiltoniano for inválido ou válido, respetivamente.
        """
        if not self.check_if_valid_path(p): #se não for um caminho válido
            return False
        to_visit = list(self.get_nodes()) #lista dos nodos a visitar
        if len(p) != len(to_visit): #verifica se o número de nodos do caminho for diferente do número de nodos a visitar
            return False
        for i in range(len(p)): #para cada nodo no caminho
        #verifica se os nodos no caminho e na lista a visitar são iguais
            if p[i] in to_visit: #se o nodo tiver na lista a visitar
                to_visit.remove(p[i]) #remove da lista dos nodos a visitar
                return False
        if not to_visit: #caso contrário,se os nodos na lista de nodos não tiverem presentes na lista a visitar
            return True # é um caminho hamiltonian pois passou por todos os nodos e não existem mais nodos a visitar
        else: #se houver nodos na lista a visitar
            return False #não é um caminho hamiltonian

    def search_hamiltonian_path(self) -> Union[dict, None]:
        """
        Método de procura de caminhos Hamiltonianos
        :return: se p for diferente de None retorna p senão retorna None
        """
        for ke in self.graph.keys(): #para cada key no grafo
            p = self.search_hamiltonian_path_from_node(ke)
            if p != None:
                return p
        return None

    def search_hamiltonian_path_from_node(self, start : int) -> list:
        """
        Método de procura de caminhos Hamiltonianos no grafo
        :param start: nodo inicial
        :return: caminho Hamiltonianos em lista
        """
        current = start #para iniciar o nodo atual tem de ser o nodo inicial
        visited = {start: 0}
        #dicionário em que as key é o nodo atual e os values o index
        path = [start] #caminho em lista dos nodos
        while len(path) < len(self.get_nodes()):
        #enquanto o caminho for menor que o número de nodos do grafo
            nxt_index = visited[current] #o proximo index corresponde ao index atual
            if len(self.graph[current]) > nxt_index:
            #se o comprimento do grafo até ao nodo atual for superior ao próximo index
                nxtnode = self.graph[current][nxt_index]
                #o próximo nodo é o nodo adjacente ao nodo atual
                visited[current] += 1
                #para percorrer todos os nodos adjacente ao nodo atual
                if nxtnode not in path:
                #se o próximo nodo não tiver no caminho (lista)
                    path.append(nxtnode)
                    #adicionar à lista path o próximo nodo
                    visited[nxtnode] = 0
                    #adicionar o nodo adjacente que visitamos ao dicionário de nodos visitados
                    #e guarda o valor como zero para ler os nodos adjacentes a partir da primeira posição
                    current = nxtnode
                    #o nodo atual passa a ser o próximo nodo
            else: #se não
                if len(path) > 1:
                #se houver um caminho,ou seja, o comprimento da lista for maior que um
                    rmvnode = path.pop() #remove o nodo da lista path e retorna o nodo removido
                    del visited[rmvnode] #elimina o nodo removido do diciónario de nodos visitados
                    current = path[-1] #inicia a nova procura de um caminho a partir do ultimo nodo da lista
                else: #senão
                    return None
        return path #caminho hamiltonianos em lista

    # Eulerian
        #Caminho que passa por todos os arcos do grafo exatamente uma vez

    def check_balanced_node(self, node) -> bool:
        """
        Método de verificação se um nó é balanceado
        :param node: nodo
        :return: valor de "False" ou "True", se o grau de entrada do nodo não for igual/ou for igual ao grau de saída do nodo, respetivamente
        """
        return self.in_degree(node) == self.out_degree(node)

    def check_balanced_graph(self) -> bool:
        """
        Método de verificação se o grafo é balanceado
        :return:valor de "False" ou "True", se o grafo for não balanceado ou balanceado, respetivamente
        """
        for n in self.graph.keys(): #para cada key do grafo
            if not self.check_balanced_node(n): #se não for um nó balanceado
                return False
        return True

    def check_nearly_balanced_graph(self):
        """
        Método de verificação se o grafo é semi-balanceado
        :return: retorna none (caso não se verifique que o grafo é semi-balanceado) ou o tuplo
        """
        res = None, None #forma um tuplo
        for n in self.graph.keys(): #para cada key do grafo
            indeg = self.in_degree(n) #indeg vai corresponder ao indice do grau de entrada
            outdeg = self.out_degree(n) #outdeg vai corresponder ao indice do grau de saída
            if indeg - outdeg == 1 and res[1] is None:
            #se o grau de entrada a subtrair pelo de saída corresponder a 1 e o tuplo de indice 1 for none
                res = res[0], n #o tuplo vai passar o ter o valor de n
            elif indeg - outdeg == -1 and res[0] is None:
            #se o grau de entrada a subtrair pelo de saída corresponder a -1  e o tuplo de indice 0 for none
                res = n, res[1] #vai subtituir o valor de n no tuplo de indice 0
            elif indeg == outdeg:
            #se o grau de entrada e saída forem iguais
                pass #passa
            else:
                return None, None
        return res

    def is_connected(self) -> bool:
        """
        Método para verificar se está conectado ou não
        :return: valor de "False" ou "True", se não tiver ligado ou tiver ligado, respetivamente
        """
        total = len(self.graph.keys()) - 1
        for v in self.graph.keys(): #para cada key do grafo
            reachable_v = self.reachable_bfs(v) #lista de nodos atingíveis a partir de v
            if (len(reachable_v) < total):
                return False
        return True

    def eulerian_cycle(self) -> list:
        """
        ciclo Euleriano passa por todos os arcos do grafo examante uma vez, regressando ao nó de partida
        :return: valor de "None" (se não for um ciclo Euleriano) ou a lista res (lista do ciclo)
        """
        if not self.is_connected() or not self.check_balanced_graph():
        #se não estiver conetado ou não o grafo não tiver balanceado, ou seja verifica se é Euleriano
            return None
        edges_visit = list(self.get_edges()) #arcos a visitar vai ser a lista de arcos
        res = [] #lista vazia
        while edges_visit: #enquanto os arcos a visitar
            pair = edges_visit[0]
            #par dos nodos correspondentes a arcos a visitar do grafo
            # vai buscar no tuplo da primeira posição da lista de arcos
            i = 1 #define o index como 1, para mudar a posição
            if res != []: #se a lista não for vazia
                while pair[0] not in res: #enquanto o primeiro par de nodos não tiver na lista correspondente ao ciclo
                    pair = edges_visit[i] #guarda o par de nodos da posição i
                    i = i + 1 #incrementa o index da lista de par de nodos para ir lendo a lista
            edges_visit.remove(pair) #remove o par da lista de arcos a visitar porque vai visitar
            start, nxt = pair #pega no par de nodos e define o primeiro nodo como o start e o segundo nodo como o nxt
            cycle = [start, nxt] #lista do ciclo em que o star é o nodo inicial e o nxt é o último nodo
            while nxt != start: #enquanto o próximo for diferente do inicial, para andar para a frente no grafo
                for adj in self.graph[nxt]: #itera cada nodo adjacente ao próximo nodo
                    if (nxt, adj) in edges_visit: #verifica se o próximo nodo e o nodo adjacente têm um arco
                        pair = (nxt, adj) #se sim, define como arco
                        nxt = adj #define o adjacente como próximo.
                        cycle.append(nxt) #adiciona o próximo nodo ao ciclo.
                        edges_visit.remove(pair) #remove o par acabado de visitar
            if not res: #se a lista for vazia
                res = cycle #a lista de nodos do ciclo passa a ser a lista de resolução
            else: #caso já tenha conteúdo
                pos = res.index(cycle[0]) #cria a variavel pos, indice do ciclo na primeira posição
                for i in range(len(cycle) - 1): #itera as posições dos nodos na lista cycle
                    res.insert(pos + i + 1, cycle[i + 1])
                    #insere na lista res na dada posição (pos+i+1) o nodo da lista cycle(da posição i+1)
        return res


    def eulerian_path(self):
        """
        Método do caminho Euleriano, caso exista
        :return: retorna o caminho
        """
        unb = self.check_nearly_balanced_graph()
        if unb[0] is None or unb[1] is None:
            return None #se não houver pontos semibalanciados não há caminho
        self.graph[unb[1]].append(unb[0])
        cycle = self.eulerian_cycle() #função do ciclo euleriano
        for i in range(len(cycle) - 1): #itera as posições dos nós
            if cycle[i] == unb[1] and cycle[i + 1] == unb[0]: 
            #quando o nó da lista cycle na posição i for igual ao segundo nodo semibalanceado e 
            # o nó seguinte for igual ao primeiro nodo semibalanceado
                break #quebra o loop
        path = cycle[i + 1:] + cycle[1:i + 1] 
        #o path fica os nodos do ciclo começando na posição i+1 e 
        # os nodos desde a segunda posição até i+1 
        return path


def is_in_tuple_list(tl, val) -> bool:
    res = False
    for (x, y) in tl:
        if val == x:
            return True
    return res