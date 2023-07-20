# Trabalho prático Teoria e Modelo de Grafos
# Gabriel Coimbra - 3044
# Dalila Vieira - 3030
# 11/2018
from AbstractGraph import AbstractGraph


class Graph(AbstractGraph):
    def __init__(self, input_number_vertexes, input_edges):
        """
        Construtor
        :param input_number_vertexes: quantidade de vértices
        :param input_edges: set com tuplas de vértices
        :param is_pseudo:
        """

        super().__init__(input_number_vertexes, input_edges, False)
        self.checkHandshake()

    @staticmethod
    def showProprieties():
        print("Grafo direcionado")
        super().showProprieties()

    def checkArticulation(self, vertex):
        """
        Checa se um vértice dado é uma articulação do grafo.

        :param vertex: indice do vértice
        :returns: Retorna True se sim, False se não
        """
        def removeVertex(vertex_removal):

            i = 0
            while i < len(self.vertexes):
                self.matrix[vertex_removal][i] = None
                self.matrix[i][vertex_removal] = None
                i += 1

            self.edges = set(filter(lambda edge: edge[0] != vertex and edge[1] != vertex, self.edges))

        if not self.checkConectivity():
            raise RuntimeError("Grafo já não é conexo!")

        self.testParameters(vertex)
        orginal_graph = self.matrix.copy()
        original_edges = self.edges.copy()

        connected_components = self.connectedComponents()
        current_component = set()
        for component in connected_components:
            if vertex in component:
                current_component = component

        removeVertex(vertex)

        returns = []
        # Procura um vértice diferente de vertex
        for entrance in current_component:
            if entrance != vertex:
                returns = self.checkConectivity(entrance,current_component)

        is_articulation = None
        if returns[0] is False:
            # É articulação sse existe vértice não visitado diferente do passado como parâmetros
            is_articulation = True if len(list(filter(lambda x: x != vertex, returns[1]))) > 0 else False
        else:
            is_articulation = False

        super().__matrix = orginal_graph
        super().__edges = original_edges

        return is_articulation

    def checkHandshake(self):
        """
        Verifica se grafo é válido usando handshake
        e a propriedade do máximo de pesos de um vértices.
        Também constróis dicionário de graus para cada vértice.
        :return: Sem retorno. Dá raise se houver problemas
        """
        vertex = 0
        while vertex < len(self.vertexes):

            degrees_vertex = len(self.neighbours(vertex))
            # Em pseudografos tempos laços. Um vértice pode no máximo a quantidade de vértices + 1,
            # já que um laço conta quando sai e quando entra
            if self.is_pseudo is True and degrees_vertex > len(self.vertexes):
                raise RuntimeError("ERRO FATAL: PseudoGrafo inválido, número de vizinhos do vértice", vertex,
                                   "é muito grande:", degrees_vertex)

            elif self.is_pseudo is False and degrees_vertex > len(self.vertexes) - 1:
                raise RuntimeError("ERRO FATAL: Grafo inválido, número de vizinhos do vértice", vertex,
                                   "é muito grande:", degrees_vertex)

            else:
                self.degrees_vertexes[vertex] = degrees_vertex
                vertex += 1

        if sum(self.degrees_vertexes.values()) / 2 != len(self.edges):
            raise RuntimeError("ERRO FATAL! Grafo inválido, handshake falhou! soma de graus",
                               sum(self.degrees_vertexes.values()), "arestas", len(self.edges))

    def write(self):
        """
        Escreve em arquivo a imagem do grafo
        :return:
        """
        Utils.write(False, self.edges)

    def checkBridge(self, edge):
        """
        :param edge: checa se essa aresta é ponte
        :return: Retorna veradeiro se for ponte
        """

        def removeEdge(vertex, neighbour, is_direcionado=False):
            """
            :param vertex: vertice cujo vizinho sera removido
            :param neighbour: qual vizinho remover
            :param is_direcionado:
            :return:
            """
            self.testParameters({vertex, neighbour})

            self._matrix[vertex][neighbour] = None

            self._matrix[neighbour - 1][vertex - 1] = None

            new_edges = set()
            for old_edge in self.edges:
                if vertex == old_edge[0] and neighbour == old_edge[1]:
                    new_edges.add(old_edge)
                elif vertex == old_edge[1] and neighbour == old_edge[0]:
                    new_edges.add(old_edge)
            self.edges = new_edges

        self.testParameters(None, edge)
        orginal_graph = self._matrix.copy()
        original_edges = self.edges.copy()
        removeEdge(edge[0], edge[1])
        is_bridge = not self.checkConectivity()
        self._matrix = orginal_graph
        self.edges = original_edges
        return is_bridge

    def writePrim(self, entrance=None):
        utilsWrite(False, self.runPrim(entrance), "prim.png")

    def deepFirstSearch(self, entrance=None):
        """
        Realiza uma busca em profundidade na arvore
        :return: Retorna Arvore de profundidade
        """

        def recursive(target):
            """
            Função auxiliar recursiva para realizar a busca em profundidade propriamente dita
            :param target:  Definido por deepFirstSearch
            :return: Sem retorno. As variáveis são modificadas, por referência, no escopo de deepFirstSearch
            """

            def isFather(father, son):
                """
                Função auxiliar recursiva. Verifica se o vértice father é pai de son.
                :param father: Definido pela recursive
                :param son: Definido pela recursive
                :return: Retorna True se sim.
                """
                self.testParameters({father, son})

                visited_vertexes2 = [False for vertex in range(len(self._matrix))]  # Lista de vértices visitados
                stack = [father]

                while len(stack) > 0:
                    vertex = stack.pop()  # Tira vértice do topo da pilha
                    if not visited_vertexes2[vertex]:  # Se esse vértice não foi visitado ainda
                        visited_vertexes2[vertex] = True  # Marque-o como visitado
                        for neighbour2 in self.neighbours(vertex):  # Para cada vizinho dele
                            if neighbour2 == son:
                                return True
                            stack.append(neighbour2)
                return False

            self.testParameters(target)
            visited_vertexes[target] = True
            sequence.append(target)
            for neighbour in self.neighbours(target):
                if not visited_vertexes[neighbour]:
                    visited_edges.add((target, neighbour))
                    visited_vertexes[neighbour] = True
                    recursive(neighbour)
                elif (target, neighbour) not in visited_edges and (neighbour, target) not in visited_edges:
                    # Vértice já visitado, precisamos verificar se temos uma aresta de retorno ou avanço
                        return_edges.append((target, neighbour))

        self.testParameters(entrance)
        visited_vertexes = [False for vertex in range(len(self._matrix))]
        visited_edges = set()
        return_edges = []
        foward_edges = []
        sequence = []

        if entrance is None:
            entrance = 0

        else:
            recursive(entrance)

        return sequence, return_edges, foward_edges

    def checkEulerTheorem(self):
        """
            Verifica o teorema de Euler
           :return: Retorna True se o grafo é euleriano
        """

        # inicializa
        degree = 0
        has_euler_path = True

        for vertex in self.vertexes:

            degree = len(self.neighbours(vertex))

            # Verifica se todos os vertices tem grau par
            if degree % 2 == 1:
                has_euler_path = False
                break
        return has_euler_path
