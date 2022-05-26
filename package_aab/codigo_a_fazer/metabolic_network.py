# -*- coding: utf-8 -*-
"""
Package dos algoritmos implementados em aula
Algoritmos Avançados de Bioinformática
"""

"""
Class: Metabolic Network 
"""

from MyGraph import MyGraph


class MetabolicNetwork(MyGraph):
    #subclasse da classe MyGraph que representa as redes metabólicas

    def __init__(self, network_type="metabolite-reaction", split_rev=False):
        MyGraph.__init__(self, {})
        self.net_type = network_type
        self.node_types = {} # dicionário com as listas de nodos de cada tipo
        if network_type == "metabolite-reaction":
            self.node_types["metabolite"] = [] # lista com o nodos do tipo "metabolite"
            self.node_types["reaction"] = [] # lista com os nodos do tipo "reaction"
        self.split_rev = split_rev
        # indica se as reações reversíveis são para serem consideradas como duas reações distintas, sendo que como é
        ## dado como 'False' consideramos que não são duas reações distintas

    def add_vertex_type(self, v : str, nodetype : str):
        """
        Método que adiciona o nodo v ao dicionário node_types, conferindo se este já não existe
        :param v: nodo
        :param nodetype: tipo do nodo
        """
        self.add_vertex(v)
        self.node_types[nodetype].append(v)

    def get_nodes_type(self, node_type : str) -> Union[dict,None]:
        """
        Método que retorna o dicionário com as listas de nodos de cada tipo
        :param node_type: tipo de nodo
        :return: se o node_type dado como input pertence ao dicionário node_types é retornado o mesmo
        se não, não retorna nada
        """
        if node_type in self.node_types:
            return self.node_types[node_type]
        else:
            return None

    def load_from_file(self, filename : str):
        """
        Método que recebe e abre o ficheiro criado anteriormente com as informações da rede metabólica e
        (onde cada reação será uma linha) e converte a informação do mesmo para ser introduzida nos
        atributos desta subcalsse
        :param filename: nome do ficheiro que queremos abrir
        :return: caso haja um erro numa linha do ficheiro retorna a indicação que aquela linha é inválida
        """
        file = open(filename) #abre o ficheiro
        graph_mr = MetabolicNetwork("metabolite-reaction") #cria o grafo da rede metabólica do tipo metabolite-reaction
        for line in file: #para cada linha do ficheiro
            if ":" in line: #se houver ":" na linha
                tokens = line.split(":") #divide a linha desde os ":"
                reac_id = tokens[0].strip() #remove os caracteres antes e depois do id da reação
                gmr.add_vertex_type(reac_id, "reaction")
                #adiciona a reação ao dicionário node_types, identificando o tipo "reaction"
                reaction_line = tokens[1]
            else:
                raise Exception("Invalid line:") #se a linha não possuir ":" é uma linha inválida
            if "<=>" in reaction_line: #se houver "<=>" na linha da reação (reação reversível)
                left, right = rline.split("<=>") #divide a linha desde os "<=>" em "left" e "right"
                metabolites_left = left.split("+") #divide os metabolitos da esquerda desde o "+"
                for met in metabolites_left: #para cada metabolito na esqueda
                    met_id = met.strip() #remove os caracteres antes e depois do id dos metabolitos
                    if met_id not in gmr.graph: #se o metabolito não pertencer ao grafo
                        gmr.add_vertex_type(met_id, "metabolite")
                        #adiciona o nodo do metabolito ao dicionário node_types, identificando o tipo "metabolite"
                    if self.split_rev: #True - se considerarmos a reação reversível como duas reações distintas
                        gmr.add_vertex_type(reac_id + "_b", "reaction")
                        #adiciona a reação b ao dicionário node_types, identificando o tipo "reaction"
                        gmr.add_edge(met_id, reac_id) #adiciona o arco da primeira reação (met_id,reac_id) ao grafo
                        gmr.add_edge(reac_id + "_b", met_id) #adiciona o arco reação b (met_id,reac_id) ao grafo
                    else: #False - se não considerarmos a reação reversível como duas reações distintas
                        gmr.add_edge(met_id, reac_id) #adiciona o arco da reação num sentido (met_id,reac_id) ao grafo
                        gmr.add_edge(reac_id, met_id) #adiciona o arco da reação noutro sentido(reac_id,met_id) ao grafo
                metabolites_right = right.split("+") #divide os metabolitos da direita desde o "+"
                for met in metabolites_right:#para cada metabolito na direita
                    met_id = met.strip() #remove os caracteres antes e depois do id dos metabolitos
                    if met_id not in gmr.graph: #se o metabolito não pertencer ao grafo
                        gmr.add_vertex_type(met_id, "metabolite")
                        #adiciona o nodo do metabolito ao dicionário node_types, identificando o tipo "metabolite"
                    if self.split_rev: #True - se considerarmos a reação reversível como duas reações distintas
                        gmr.add_edge(met_id, reac_id + "_b") #adiciona o arco reação b (met_id,reac_id) ao grafo
                        gmr.add_edge(reac_id, met_id) #adiciona o arco da reação contrária (met_id,reac_id) ao grafo
                    else: #False - se não considerarmos a reação reversível como duas reações distintas
                        gmr.add_edge(met_id, reac_id) #adiciona o arco da reação num sentido (met_id,reac_id) ao grafo
                        gmr.add_edge(reac_id, met_id) #adiciona o arco da reação noutro sentido(reac_id,met_id) ao grafo
            elif "=>" in line: #se houver "=>" na linha da reação (reação irreversível)
                left, right = rline.split("=>") #divide a linha desde os "=>" em "left" e "right"
                metabolites_left = left.split("+") #divide os metabolitos da esquerda desde o "+"
                for met in metabolites_left: #para cada metabolito na esqueda
                    met_id = met.strip() #remove os caracteres antes e depois do id dos metabolitos
                    if met_id not in gmr.graph: #se o metabolito não pertencer ao grafo
                        gmr.add_vertex_type(met_id, "metabolite")
                        #adiciona o nodo do metabolito ao dicionário node_types, identificando o tipo "metabolite"
                    gmr.add_edge(met_id, reac_id) #adiciona o arco da reação (met_id,reac_id) ao grafo
                metabolites_right = right.split("+") #divide os metabolitos da direita desde o "+"
                for met in metabolites_right: #para cada metabolito na direita
                    met_id = met.strip() #remove os caracteres antes e depois do id dos metabolitos
                    if met_id not in gmr.graph: #se o metabolito não pertencer ao grafo
                        gmr.add_vertex_type(met_id, "metabolite")
                        #adiciona o nodo do metabolito ao dicionário node_types, identificando o tipo "metabolite"
                    gmr.add_edge(reac_id, met_id) #adiciona o arco da reação (met_id,reac_id) ao grafo
            else: #se a linha não possuir "<=>" ou "=>" é uma linha inválida
                raise Exception("Invalid line:")

        if self.net_type == "metabolite-reaction": #se a rede metabólica for do tipo metabolite-reaction
            self.graph = gmr.graph #cria o grafo da rede metabólica do tipo metabolite-reaction
            self.node_types = gmr.node_types  #dicionário com as listas de nodos de cada tipo
        elif self.net_type == "metabolite-metabolite": #se a rede metabólica for do tipo metabolite-metabolite
            self.convert_metabolite_net(gmr) #converter para uma rede do tipo metabolite-reaction
        elif self.net_type == "reaction-reaction": #se a rede metabólica for do tipo reaction-reaction
            self.convert_reaction_graph(gmr) #converter para uma rede do tipo metabolite-reaction
        else:
            self.graph = {}

    def convert_metabolite_net(self, gmr):
        for m in gmr.node_types["metabolite"]:
            pass

    def convert_reaction_graph(self, gmr):
        for r in gmr.node_types["reaction"]:
            pass


def test1():
    m = MetabolicNetwork("metabolite-reaction")
    m.add_vertex_type("R1", "reaction")
    m.add_vertex_type("R2", "reaction")
    m.add_vertex_type("R3", "reaction")
    m.add_vertex_type("M1", "metabolite")
    m.add_vertex_type("M2", "metabolite")
    m.add_vertex_type("M3", "metabolite")
    m.add_vertex_type("M4", "metabolite")
    m.add_vertex_type("M5", "metabolite")
    m.add_vertex_type("M6", "metabolite")
    m.add_edge("M1", "R1")
    m.add_edge("M2", "R1")
    m.add_edge("R1", "M3")
    m.add_edge("R1", "M4")
    m.add_edge("M4", "R2")
    m.add_edge("M6", "R2")
    m.add_edge("R2", "M3")
    m.add_edge("M4", "R3")
    m.add_edge("M5", "R3")
    m.add_edge("R3", "M6")
    m.add_edge("R3", "M4")
    m.add_edge("R3", "M5")
    m.add_edge("M6", "R3")
    m.print_graph()
    print("Reactions: ", m.get_nodes_type("reaction"))
    print("Metabolites: ", m.get_nodes_type("metabolite"))


def test2():
    print("metabolite-reaction network:")
    mrn = MetabolicNetwork("metabolite-reaction")
    mrn.load_from_file("example-net.txt")
    mrn.print_graph()
    print("Reactions: ", mrn.get_nodes_type("reaction"))
    print("Metabolites: ", mrn.get_nodes_type("metabolite"))
    print()

    print("metabolite-metabolite network:")
    mmn = MetabolicNetwork("metabolite-metabolite")
    mmn.load_from_file("example-net.txt")
    mmn.print_graph()
    print()

    print("reaction-reaction network:")
    rrn = MetabolicNetwork("reaction-reaction")
    rrn.load_from_file("example-net.txt")
    rrn.print_graph()
    print()

    print("metabolite-reaction network (splitting reversible):")
    mrsn = MetabolicNetwork("metabolite-reaction", True)
    mrsn.load_from_file("example-net.txt")
    mrsn.print_graph()
    print()

    print("reaction-reaction network (splitting reversible):")
    rrsn = MetabolicNetwork("reaction-reaction", True)
    rrsn.load_from_file("example-net.txt")
    rrsn.print_graph()
    print()


test1()
print()
test2()