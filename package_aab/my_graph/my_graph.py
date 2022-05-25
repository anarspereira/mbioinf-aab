# -*- coding: utf-8 -*-
"""
Package dos algoritmos implementados em aula
Algoritmos Avançados de Bioinformática
"""

"""
Class: MyGraph
"""

## keys are vertices
## values of the dictionary represent the list of adjacent vertices of the key node

class MyGraph:

    def __init__(self, g ={}):
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

    def get_nodes(self):
        """
        Método que returna a lista de nodes
        """
        return list(self.graph.keys())

    def get_edges(self):
        """
        Método que returna a lista de arcos
        v será a origem
        d será o destino
        """
        edges = []
        for v in self.graph.keys():
            for d in self.graph[v]:
                edges.append((v, d))
        return edges

    def size(self):
        """
        Método que returna o tamanho do grafo, nomeadamente número de nodos e o número de arcos
        """

        return len(self.get_nodes()), len(self.get_edges())

    def add_vertex(self, v:str):
        """
        Método que adiciona o node v ao grafo
        :param v: node
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
        :param v: node
        :return: returna lista de nodes sucessores do node v
        """
        return list(
            self.graph[v])  # needed to avoid list being overwritten of result of the function is used

    def get_predecessors(self, v:str):
        """
        :param v: node
        :return: returna lista de nodes antecessores do node v
        """
        res = []
        for k in self.graph.keys():
            if v in self.graph[k]:
                res.append(k)
        return res

    def get_adjacents(self, v:str):
        """
        :param v: node
        :return: returna a lista de nodes adjacentes do node v
        """
        suc = self.get_successors(v)
        pred = self.get_predecessors(v)
        res = pred
        for p in suc:
            if p not in res: res.append(p)
        return res


    def out_degree(self, v:str):
        """
        Método que calcula grau de saída do node v
        :param v: node
        :return: returna grau de saída do node
        """
        return len(self.graph[v])

    def in_degree(self, v:str):
        """
        Método que calcula grau de entrada do node v
        :param v: node
        :return: returna grau de entrada do node
        """
        return len(self.get_predecessors(v))

    def degree(self, v:str):
        """
        Método que calcula grau do node v (todos os nodes adjacentes quer percursores quer sucessores
        :param v: node
        :return: returna grau do node v
        """
        return len(self.get_adjacents(v))

    def all_degrees(self, deg_type="inout"):
        """
        Método do cálculo de graus de entrada e saída, ou ambos para todos os nodes do grafo
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

    def highest_degrees(self, all_deg=None, deg_type="inout", top=10):
        """
        Método que calcula graus mais elevados
        :param all_deg: graus de entrada e saída, ou ambos
        :param deg_type:tipo de grau (entrada, saída ou ambos)
        :param top:
        :return:
        """
        if all_deg is None:
            all_deg = self.all_degrees(deg_type)
        ord_deg = sorted(list(all_deg.items()), key=lambda x: x[1], reverse=True)
        return list(map(lambda x: x[0], ord_deg[:top]))

    ## topological metrics over degrees

    def mean_degree(self, deg_type="inout"):
        """
        Método para calcular a media de graus
        :param deg_type: tipo de grau (entrada, saída ou ambos)
        :return: returna a média de graus
        """
        degs = self.all_degrees(deg_type)
        return sum(degs.values()) / float(len(degs))

    def prob_degree(self, deg_type="inout"):
        """
        Método para calcular a probabilidade de graus
        :param deg_type: tipo de grau (entrada, saída ou ambos)
        :return: returna a probabilidade de graus
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
        Método de nodes atingíveis a partir de v, de cima para baixo (largura)
        :param v: node
        :return: retorna lista de nodes atingíveis a partir de v
        """
        l = [v]
        res = []
        while len(l) > 0: #enquanto há elementos na lista l
            node = l.pop(0) #isolar o primeiro elemento da lista l, queue de nodes
            if node != v: res.append(node) #se o node for diferente de v, adicionar o node a res
            for elem in self.graph[node]: #para todos os sucessores do node
                if elem not in res and elem not in l and elem != node: #se não existe em res e em l e se o sucessor é diferente do node
                    l.append(elem) #adicionar na queue para verificar
        return res

    def reachable_dfs(self, v):
        """
        Método de nodes atingíveis a partir de v, da esquerda para a direita (em profundidade)
        :param v: node
        :return: retorna lista de nodes atingíveis a partir de v
        """
        l = [v]
        res = []
        while len(l) > 0: #enquanto há elementos na lista l, queue de nodes
            node = l.pop(0) #isolar o primeiro elemento da lista l
            if node != v: res.append(node) #se o node for diferente de v, adicionar o node a res
            s = 0 #ira ser usado para criar o stack//é reposto a 0 antes do loop for abaixo
            for elem in self.graph[node]: #para todos os sucessores do node
                if elem not in res and elem not in l: #se não existe em res e em l e se o sucessor é diferente do node
                    l.insert(s, elem) #cria um stack/vai voltar a verificar o mais recente/insere no inicio da lista
                    s += 1 #caso haja multiplos sucessores, o s vai aumentar de forma a colocar as proximas iteraçoes na posicao depois da iteraçao anterior (stack)
        return res

    def distance(self, s, d):
        """
        Método da distância entre nodes s e d
        :param s: node s
        :param d: node d
        :return: retorna a distancia entre nodes s e d
        """
        if s == d:
            return 0
        l = [(s, 0)] #lista com os tuplos do node e a distância
        visited = [s] #nodes visitados
        while len(l) > 0: #enquanto há elementos na lista l, queue de nodes
            node, dist = l.pop(0) #isolar o primeiro elemento da lista l
            for elem in self.graph[node]: #para todos os sucessores do node
                if elem == d: #
                    return dist + 1 #
                elif elem not in visited:
                    l.append((elem, dist + 1))
                    visited.append(elem)
        return None

    def shortest_path(self, s, d):
        """
        Método do caminho mais curto entre s e d (lista de nodes por onde passa)
        :param s: node s
        :param d: node d
        :return: retorna caminho mais curto, lista de nodes por onde passa
        """
        if s == d:
            return []
        l = [(s, [])] #lista com um tuplo com o node e o caminho
        visited = [s] #nodes visitados
        while len(l) > 0:
            node, preds = l.pop(0)
            for elem in self.graph[node]:
                if elem == d:
                    return preds + [node, elem]
                elif elem not in visited:
                    l.append((elem, preds + [node]))
                    visited.append(elem)
        return None

    def reachable_with_dist(self, s):
        """
        Método de nodes atingíveis a partir de v com respetiva distância
        :param s: node
        :return: retorna lista de pares nodes, distância
        """
        res = []
        l = [(s, 0)] #lista com tuplo com s e distância de s a s(0)
        while len(l) > 0: #enquanto há elementos na lista l, queue de nodes
            node, dist = l.pop(0)
            if node != s: #se node for diferente de s
                res.append((node, dist)) #não conta o s
            for elem in self.graph[node]: #para
                if not is_in_tuple_list(l, elem) and not is_in_tuple_list(res, elem): # vai ver se o p se encontra dentro de l ou em res
                    l.append((elem, dist + 1)) # adiciona o vertice a que se liga
        return res

    ## mean distances ignoring unreachable nodes
    def mean_distances(self):
        """
        Método da média das distâncias de cada node
        :return: retorna a distância média e a proporção de nodes atingíveis
        """
        total = 0
        num_reachable = 0 #números de nodes no grafo ligados entre si
        for k in self.graph.keys(): #para cada key no grafo
            distsk = self.reachable_with_dist(k) #a lista correspondente aos nodes atingidos e a respetiva distância
            for _, dist in distsk: #para cada carater correspondente à distancia na lista
                total += dist #vamos adicionar o valor da distância ao total
            num_reachable += len(distsk) #número de nodes atingidos vai corresponder ao comprimento da lista (distsk) obtida, todas as ligações entre todos os nodes
        meandist = float(total) / num_reachable #média da distancia total dos nodes atingidos
        n = len(self.get_nodes()) #número total de nodes
        return meandist, float(num_reachable) / ((n - 1) * n)

    def closeness_centrality(self, node):
        """
        Método de aproximação média das distâncias percorridas entre os nodes atingidos
        :param node: node
        :return: retorna a média das distâncias entre os nodes atingidos
        """
        dist = self.reachable_with_dist(node) #a lista correspondente aos nodes atingidos e a respetiva distância
        if len(dist) == 0: #se o número de nodes atingidos for igual a 0
            return 0.0 #retorna 0
        s = 0.0
        for d in dist: s += d[1] #para cada node é adicionada a distância à variavel s
        return len(dist) / s #TODO: Rever

    def highest_closeness(self, top=10):
        """

        :param top:
        :return:
        """
        cc = {} #dicionário
        for k in self.graph.keys(): #para cada key no grafo
            cc[k] = self.closeness_centrality(k) #node corresponde
        ord_cl = sorted(list(cc.items()), key=lambda x: x[1], reverse=True)
        return list(map(lambda x: x[0], ord_cl[:top]))

    def betweenness_centrality(self, node):
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

    ## cycles - aula 8
    def node_has_cycle(self, v):
        """

        :param v: node
        :return:
        """
        l = [v]
        res = False
        visited = [v] #nodes visitados
        while len(l) > 0: #enquanto há elementos na lista l, queue de nodes
            node = l.pop(0) #isolar o primeiro elemento da lista l
            for elem in self.graph[node]: #para todos os sucessores do node
                if elem == v:
                    return True
                elif elem not in visited:
                    l.append(elem)
                    visited.append(elem)
        return res

    def has_cycle(self):
        """

        :return:
        """
        res = False
        for v in self.graph.keys():  #para cada key no grafo
            if self.node_has_cycle(v): #se
                return True
        return res

    ## clustering - aula 9

    def clustering_coef(self, v):
        """
        Método
        :param v:
        :return:
        """
        adjs = self.get_adjacents(v)
        if len(adjs) <= 1: return 0.0
        ligs = 0
        for i in adjs:
            for j in adjs:
                if i != j:
                    if j in self.graph[i] or i in self.graph[j]:
                        ligs = ligs + 1
        return float(ligs) / (len(adjs) * (len(adjs) - 1))

    def all_clustering_coefs(self):
        """
        Método que calcula todos os coeficientes
        :return:
        """
        ccs = {}
        for k in self.graph.keys():
            ccs[k] = self.clustering_coef(k)
        return ccs

    def mean_clustering_coef(self):
        ccs = self.all_clustering_coefs()
        return sum(ccs.values()) / float(len(ccs))

    def mean_clustering_perdegree(self, deg_type="inout"):
        degs = self.all_degrees(deg_type)
        ccs = self.all_clustering_coefs()
        degs_k = {}
        for k in degs.keys():
            if degs[k] in degs_k.keys():
                degs_k[degs[k]].append(k)
            else:
                degs_k[degs[k]] = [k]
        ck = {}
        for k in degs_k.keys():
            tot = 0
            for v in degs_k[k]: tot += ccs[v]
            ck[k] = float(tot) / len(degs_k[k])
        return ck

    ## Hamiltonian - aula 10

    def check_if_valid_path(self, p):
        if p[0] not in self.graph.keys(): return False
        for i in range(1, len(p)):
            if p[i] not in self.graph.keys() or p[i] not in self.graph[p[i - 1]]:
                return False
        return True

    def check_if_hamiltonian_path(self, p):
        if not self.check_if_valid_path(p): return False
        to_visit = list(self.get_nodes())
        if len(p) != len(to_visit): return False
        for i in range(len(p)):
            if p[i] in to_visit:
                to_visit.remove(p[i])
            else:
                return False
        if not to_visit:
            return True
        else:
            return False

    def search_hamiltonian_path(self):
        for ke in self.graph.keys():
            p = self.search_hamiltonian_path_from_node(ke)
            if p != None:
                return p
        return None

    def search_hamiltonian_path_from_node(self, start):
        current = start
        visited = {start: 0}
        path = [start]
        while len(path) < len(self.get_nodes()):
            nxt_index = visited[current]
            if len(self.graph[current]) > nxt_index:
                nxtnode = self.graph[current][nxt_index]
                visited[current] += 1
                if nxtnode not in path:
                    path.append(nxtnode)
                    visited[nxtnode] = 0
                    current = nxtnode
            else:
                if len(path) > 1:
                    rmvnode = path.pop()
                    del visited[rmvnode]
                    current = path[-1]
                else:
                    return None
        return path

    # Eulerian - aula 11

    def check_balanced_node(self, node):
        return self.in_degree(node) == self.out_degree(node)

    def check_balanced_graph(self):
        for n in self.graph.keys():
            if not self.check_balanced_node(n): return False
        return True

    def check_nearly_balanced_graph(self):
        res = None, None
        for n in self.graph.keys():
            indeg = self.in_degree(n)
            outdeg = self.out_degree(n)
            if indeg - outdeg == 1 and res[1] is None:
                res = res[0], n
            elif indeg - outdeg == -1 and res[0] is None:
                res = n, res[1]
            elif indeg == outdeg:
                pass
            else:
                return None, None
        return res

    def is_connected(self):
        total = len(self.graph.keys()) - 1
        for v in self.graph.keys():
            reachable_v = self.reachable_bfs(v)
            if (len(reachable_v) < total): return False
        return True

    def eulerian_cycle(self):
        if not self.is_connected() or not self.check_balanced_graph(): return None
        edges_visit = list(self.get_edges())
        res = []
        while edges_visit:
            pass  ## completar aqui
        return res

    def eulerian_path(self):
        unb = self.check_nearly_balanced_graph()
        if unb[0] is None or unb[1] is None: return None
        self.graph[unb[1]].append(unb[0])
        cycle = self.eulerian_cycle()
        for i in range(len(cycle) - 1):
            if cycle[i] == unb[1] and cycle[i + 1] == unb[0]:
                break
        path = cycle[i + 1:] + cycle[1:i + 1]
        return path


def is_in_tuple_list(tl, val):
    res = False
    for (x, y) in tl:
        if val == x: return True
    return res


def test1():
    gr = MyGraph({1: [2], 2: [3], 3: [2, 4], 4: [2]})
    gr.print_graph()
    print(gr.get_nodes())
    print(gr.get_edges())


def test2():
    gr2 = MyGraph()
    gr2.add_vertex(1)
    gr2.add_vertex(2)
    gr2.add_vertex(3)
    gr2.add_vertex(4)

    gr2.add_edge(1, 2)
    gr2.add_edge(2, 3)
    gr2.add_edge(3, 2)
    gr2.add_edge(3, 4)
    gr2.add_edge(4, 2)

    gr2.print_graph()


def test3():
    gr = MyGraph({1: [2], 2: [3], 3: [2, 4], 4: [2]})
    gr.print_graph()

    print(gr.get_successors(2))
    print(gr.get_predecessors(2))
    print(gr.get_adjacents(2))
    print(gr.in_degree(2))
    print(gr.out_degree(2))
    print(gr.degree(2))


def test4():
    gr = MyGraph({1: [2], 2: [3], 3: [2, 4], 4: [2]})
    print(gr.shortest_path(1, 4))
    print(gr.shortest_path(4, 3))

    print(gr.reachable_with_dist(1))
    print(gr.reachable_with_dist(3))

    gr2 = MyGraph({1: [2, 3], 2: [4], 3: [5], 4: [], 5: []})
    print(gr2.shortest_path(1, 5))
    print(gr2.shortest_path(2, 1))

    print(gr2.reachable_with_dist(1))
    print(gr2.reachable_with_dist(5))


def test5():
    gr = MyGraph({1: [2], 2: [3], 3: [2, 4], 4: [2]})
    print(gr.node_has_cycle(2))
    print(gr.node_has_cycle(1))
    print(gr.has_cycle())

    gr2 = MyGraph({1: [2, 3], 2: [4], 3: [5], 4: [], 5: []})
    print(gr2.node_has_cycle(1))
    print(gr2.has_cycle())


def test6():
    gr = MyGraph()
    gr.add_vertex(1)
    gr.add_vertex(2)
    gr.add_vertex(3)
    gr.add_vertex(4)
    gr.add_edge(1, 2)
    gr.add_edge(2, 3)
    gr.add_edge(3, 2)
    gr.add_edge(3, 4)
    gr.add_edge(4, 2)
    gr.print_graph()
    print(gr.size())

    print(gr.get_successors(2))
    print(gr.get_predecessors(2))
    print(gr.get_adjacents(2))

    print(gr.in_degree(2))
    print(gr.out_degree(2))
    print(gr.degree(2))

    print(gr.all_degrees("inout"))
    print(gr.all_degrees("in"))
    print(gr.all_degrees("out"))

    gr2 = MyGraph({1: [2, 3, 4], 2: [5, 6], 3: [6, 8], 4: [8], 5: [7], 6: [], 7: [], 8: []})
    print(gr2.reachable_bfs(1))
    print(gr2.reachable_dfs(1))

    print(gr2.distance(1, 7))
    print(gr2.shortest_path(1, 7))
    print(gr2.distance(1, 8))
    print(gr2.shortest_path(1, 8))
    print(gr2.distance(6, 1))
    print(gr2.shortest_path(6, 1))

    print(gr2.reachable_with_dist(1))

    print(gr.has_cycle())
    print(gr2.has_cycle())

    print(gr.mean_degree())
    print(gr.prob_degree())
    print(gr.mean_distances())
    print(gr.clustering_coef(1))
    print(gr.clustering_coef(2))


if __name__ == "__main__":
    # test1()
    # test2()
    # test3()
    test4()
    # test5()
    # test6()