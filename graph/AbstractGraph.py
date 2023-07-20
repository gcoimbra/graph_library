# Trabalho prático Teoria e Modelo de Grafos
# Gabriel Coimbra - 3044
# Dalila Vieira - 3030
# 11/2018
import numpy  # requerido para armazenar a matriz de pesos com eficiência
import Utils


class AbstractGraph:
    _matrix = None  # Futura matrix NxN
    vertexes = set()  # set com cada vértice
    edges = set()  # set com cada aresta obtida da entrada
    is_pseudo = None
    is_conexo = None
    degrees_vertexes = {}  # Graus de cada vértice

    def __init__(self, input_number_vertexes, input_edges, is_direcionado):
        """
        Construtor
        :param input_number_vertexes: quantidade de vértices
        :param input_edges: set com tuplas de vértices
        :param is_direcionado:
        :param is_pseudo:
        """

        def generateMatrix():
            """
            Sub-procedimento que gera a matrix de pesos
            :return:
            """
            # Gera uma linha da matriz. Uma linha com uma quantidade de self.vertex zeros
            line = numpy.array([None for x in range(input_number_vertexes)])

            # Agrupa várias linhas geradas anteriormente. Uma matriz com uma quantidade de self.vertex "line"s
            self._matrix = numpy.array([line for x in range(input_number_vertexes)])

            # Inicializa set com vértices
            self.vertexes = list(range(input_number_vertexes))

            # Seta valores dos pesos de acordo com as coordenadas da entrada
            # edge[0, 1, 2] = (x, y, w) -> cordenada x y e peso w
            # edge[0] = (x) -> vértice sozinho
            for edge in input_edges:
                if len(edge) == 3:  # Vértice está conectado a outro
                    edge_from = edge[0]
                    edge_to = edge[1]
                    edge_weight = edge[2]

                    # Checa se o valor da aresta já está lá.
                    try:
                        if self._matrix[edge_from][edge_to] is not None:
                            # Se já estiver, significa que estamos tentando adicionar outra no mesmo lugar.
                            raise RuntimeError("ERRO FATAL grafo não simples! Vértices:", edge_from, edge_to)
                    except IndexError:
                        raise RuntimeError("ERRO FATAL arquivo de entrada inválido!")
                    # Adiciona peso
                    self._matrix[edge_from][edge_to] = edge_weight

                    if not is_direcionado:
                        # Inverte coordenadas para alcançar simetria
                        self._matrix[edge_to][edge_from] = edge_weight
                elif len(edge) == 1:
                    self.is_conexo = False
                else:
                    raise RuntimeError("ERRO FATAL lista de entrada está em um formato inválido!")

        if input_number_vertexes < 2 or len(input_edges) < 1:
            raise RuntimeError("Grafo nulo e/ou vazio não são suportados!")

        self.edges = input_edges

        generateMatrix()
        # Checa a existencia de algum valor diferente de False ou None nas diagonais principais
        self.is_pseudo = any(self._matrix[diagonal][diagonal] for diagonal in range(len(self.vertexes)))

    def showMatrix(self):
        """
        Mostra a matriz de pesos
        :return:
        """

        i = 0
        while i < len(self._matrix):
            j = 0
            print(i, end=": ")
            while j < len(self._matrix[i]):
                # Caso não haja nenhum valor
                if self._matrix[i][j] is None:
                    print("\t*", end="\t")
                else:
                    print("\t" + str(self._matrix[i][j]), end="\t")
                j += 1
            print()
            i += 1

        print()

    def testParameters(self, vertexes=None, edges=None):
        if vertexes is not list:
            vertexes = {vertexes}
        if edges is not list:
            edges = {edges}
        if vertexes is not None:
            filter(lambda x: RuntimeError("Vértice não existe!") if x < 0 or x >= len(self.vertexes) else x, vertexes)
        if edges is not None:
            filter(lambda x: RuntimeError("Aresta não existe!") if x < 0 or x >= len(self.vertexes) else x, vertexes)

    def showProprieties(self):
        """
        Mostra algumas propriedades
        :return:
        """

        def degreeslist():
            """
            Mostra graus de cada vértice
            :return:
            """

            vertex_index = 0
            print("(Índice do vértice, grau)")
            while vertex_index < len(self.vertexes):
                # Indice começa no zero
                print("(", vertex_index + 1, ",", self.degrees_vertexes[vertex_index], ")", sep="", end=" ")
                vertex_index += 1
            print()

        print("Propriedades do Grafo")
        print("Vértices:", len(self.vertexes), "Arestas:", len(self.edges))
        print("Pseudo?", self.is_pseudo)
        print("Graus total:", len(self.degrees_vertexes.values()))

        # Faces de acordo com fórmula de Euler
        print("Faces:", len(self.edges) - len(self.vertexes) + len(self.connectedComponents()) + 1)

        # Sub procedimento
        degreeslist()

    def neighbours(self, vertex):
        """
        Pesquisa na matriz para retornar vizinhos
        elementos não None significa que há vizinho.
        :param: target vertex
        :return: set com vizinhos de vertex
        """
        self.testParameters(vertex)
        return set(x for x in range(len(self.vertexes)) if self._matrix[vertex][x] is not None)

    def checkBiparity(self):
        if self.is_pseudo:
            raise RuntimeError("Algoritmo só funciona em grafos simples")

        # Primeiro vértice em um set
        set1 = {0}

        # Todos seus vizinhos em outro
        set2 = self.neighbours(0)

        # Cria outro set com todos vértices que faltam
        vertexes_left = self.vertexes.copy()
        vertexes_left.difference_update({0} | set2)

        # Enquanto não for vazio
        while vertexes_left != set():
            # Seleciona algum vértice e seus vizinhos
            selected_vertex = vertexes_left.pop()
            selected_neighbours = self.neighbours(selected_vertex)

            # Checa em qual set os vizinhos de selected_vertex estao
            if set1.difference(selected_neighbours) < set1:
                # Está nos dois sets
                if set2.difference(selected_neighbours) < set2:
                    return False

                set2.add(selected_vertex)
                set1 |= selected_neighbours

            elif set2.difference(selected_neighbours) < set2:
                # Está nos dois sets
                if set1.difference(selected_neighbours) < set1:
                    return False

                set1.add(selected_vertex)
                set2 |= selected_neighbours

            # Não está em nenhum dos dois, grafo desconexo ou é mais de 2-partido
            else:
                return False

        return True

    def checkConectivity(self, entrance=None, connected_component=None):
        """
        Realiza uma busca em profundidade na arvore para checar se o grafo é conexo.
        :return: Retorna True se o grafo é conexo. False senão junto em uma lista com o primeiro vértice
        não visitado na segunda posição.  Se no construtor já definimos que o grafo é disconexo,
         retorna None como tal vértice.
        """

        # Verifica a existência desse vértice
        self.testParameters(entrance)

        # Trata caso especial de vértice isolado.
        #  self.is_conexo já é setada no construtor da classe
        if self.is_conexo is False:
            return [False, None]

        visited_vertexes = [False for vertex in range(len(self.vertexes))]  # Lista de vértices visitados

        # Coloca algum elemento na stack
        stack = []
        if entrance is None:
            stack = [0]
        else:
            stack = [entrance]

        while len(stack) > 0:
            vertex = stack.pop()  # Tira vértice do topo da pilha
            if not visited_vertexes[vertex]:  # Se esse vértice não foi visitado ainda
                visited_vertexes[vertex] = True  # Marque-o como visitado
                for neighbour in self.neighbours(vertex):  # Para cada vizinho dele
                    stack.append(neighbour)
        index = 0

        not_visited_vertexes = []
        while index < len(visited_vertexes):
            if not visited_vertexes[index]:
                if connected_component is None:
                    not_visited_vertexes.append(index)
                elif index in connected_component:
                    not_visited_vertexes.append(index)
            index += 1

        if len(not_visited_vertexes) > 0:
            return [False, not_visited_vertexes]

        return [True, None]

    def breadthFirstSearch(self, entrance):
        """
            Realiza uma busca em largura na arvore
            :return: Retorna Arvore de largura
        """

        self.testParameters(entrance)

        visited_vertexes = [False for vertex in range(len(self.vertexes))]  # Lista de vértices visitados
        visited_edges = set()  # Lista de arestas exploradas
        return_edges = set()  # Arestas que não fazem parte da arvore
        sequence = []

        queue = [entrance]
        tree = {}
        visited_vertexes[entrance] = True
        sequence.append(entrance)

        while len(queue) > 0:
            vertex = queue.pop(0)  # Tira vértice da primeira posicao da fila

            if vertex not in tree:  # Verifica se já criamos tal valor no dicionário
                tree[vertex] = []

            for neighbour in self.neighbours(vertex):  # Para cada vizinho dele
                if not visited_vertexes[neighbour]:  # Se esse vértice não foi visitado ainda
                    visited_vertexes[neighbour] = True  # Marque-o como visitado
                    queue.append(neighbour)
                    sequence.append(neighbour)

                    tree.get(vertex).append((neighbour, self._matrix[vertex][neighbour]))
                    visited_edges.add((vertex, neighbour))  # adiciona nas arestas visitadas
                else:
                    if not (neighbour, vertex) in visited_edges:
                        visited_edges.add((vertex, neighbour))  # adiciona nas arestas visitadas
                        return_edges.add((vertex, neighbour, self._matrix[vertex][neighbour]))

        return tree, sequence, return_edges

    def checkCycles(self, entrance):
        """
        Essa função checa a ocorrência de um ciclo que inclua vertex.
        Baseada em uma pesquisa em profundidade.
        :return: True se houver, False caso contrário.
        """

        def recursive(vertex):
            visited_vertexes[vertex] = True
            for neighbour in self.neighbours(vertex):
                # Caso o vértice de destino seja entrance
                # e a aresta até ele não seja a aresta da qual saímos de entrance
                if neighbour == entrance and (entrance, vertex) not in visited_edges:
                    return True

                # Só vai para vértices os quais não visitamos antes
                if not visited_vertexes[neighbour]:
                    visited_edges.add((vertex, neighbour))
                    visited_vertexes[neighbour] = True
                    if recursive(neighbour):
                        return True
            return False

        self.testParameters(entrance)
        visited_vertexes = [False for vertex in range(len(self.vertexes))]
        visited_edges = set()

        return recursive(entrance)

    def runPrim(self, entrance=None):
        if not self.checkConectivity():
            raise RuntimeError("Grafo desconexo, não haverá árvore geradora!")

        # Entrada no grafo

        vertexes_chosen = set()
        vertex = None

        if entrance is None:
            vertexes_chosen.add(0)
            vertex = 0
        else:
            vertex = entrance
            vertexes_chosen.add(entrance)
        edges_chosen = set()

        while len(vertexes_chosen) < len(self.vertexes):
            edges_sorted = []

            for selected in vertexes_chosen:
                for neighbour in self.neighbours(selected):
                    if neighbour not in vertexes_chosen:
                        edges_sorted.append((selected, neighbour, self._matrix[selected][neighbour]))

            edges_sorted.sort(key=lambda x: x[2])
            if len(edges_sorted) > 0:
                edges_chosen.add(edges_sorted[0])
                vertex = edges_sorted[0][1]
                vertexes_chosen.add(vertex)
            else:
                break

        return edges_chosen



    def runFloydWarshall(self):
        """
        Implementacao do algoritmo Floyd-Warshall
        Calcula as rotas entre todos os pares de vertice
        E verifica presenca de circuito negativo
        :return: A menor rota entre 2 vertices quaisquer passados como parametro
        """
        negative_cycle = False
        # Gera uma linha da matriz. Uma linha com uma quantidade de self.vertex zeros

        # Agrupa várias linhas geradas anteriormente. Uma matriz com uma quantidade de self.vertex "line"s
        shortest_rout = numpy.array(
            [numpy.array([None for x in range(len(self.vertexes))]) for x in range(len(self.vertexes))])

        line = numpy.array([None for x in range(len(self.vertexes))])
        antecessor = numpy.array([line for x in range(len(self.vertexes))])

        # Inicializa matriz de caminhos e de antecessores
        for i in range(len(self.vertexes)):
            for j in range(len(self.vertexes)):
                if self._matrix[i][j] is not None:
                    shortest_rout[i][j] = self._matrix[i][j]
                    antecessor[i][j] = i
                elif i == j:
                    shortest_rout[i][j] = 0
                    antecessor[i][j] = i
                else:
                    shortest_rout[i][j] = float('Inf')
                    antecessor[i][j] = 0

        for k in range(len(self.vertexes)):
            for i in range(len(self.vertexes)):
                for j in range(len(self.vertexes)):
                    if shortest_rout[i][j] > shortest_rout[i][k] + shortest_rout[k][j]:
                        shortest_rout[i][j] = shortest_rout[i][k] + shortest_rout[k][j]
                        antecessor[i][j] = antecessor[k][j]

        for j in range(len(self.vertexes)):
            if shortest_rout[j][j] < 0:
                negative_cycle = True

        if negative_cycle:
            print("WARNING Há um ciclo negativo no grafo!")
        # imprime as matrizes de distancias e antecessores

        return shortest_rout

    def connectedComponents(self):
        """
        Realiza uma busca em profundidade na arvore para
        obtermos quantas componentes conexas existem e quais vértices percentem a quais.
        :return: Retorna True se o grafo é conexo
        """

        # Trata caso especial de vértice isolado.
        #  self.is_conexo já é setada no construtor da classe
        if self.is_conexo is False:
            return False

        components = []
        visited_vertexes = set()  # Set de vértices visitados
        left_vertexes = self.vertexes.copy()

        # Coloca algum elemento na stack
        stack = [0]

        while True:
            while len(stack) > 0:
                vertex = stack.pop()  # Tira vértice do topo da pilha
                if vertex not in visited_vertexes:  # Se esse vértice não foi visitado ainda
                    visited_vertexes.add(vertex)  # Marque-o como visitado
                    left_vertexes.remove(vertex)

                    for neighbour in self.neighbours(vertex):  # Para cada vizinho dele
                        # TODO: Isso tenta consertar, não ta funcionando
                        # IMPORTANTE - Conserta bug arquitetural: se fossemos
                        # chamados pela função de verificar articulação, um vértice estaria removido da matrix
                        # mas não teria como esse algoritmo saber, portanto fazemos essa verificação extra
                        if neighbour in left_vertexes:
                            stack.append(neighbour)
            components.append(visited_vertexes)
            if len(visited_vertexes) < len(self.vertexes):

                for vertex in left_vertexes:
                    stack = [vertex]
                    break
                if len(stack) == 0:
                    break
                left_vertexes.add(stack[0])
                visited_vertexes = set()

            else:
                break

        return components

    def independantSet(self):
        independant_set = set()
        ordenados_graus = list(self.degrees_vertexes.items())
        ordenados_graus.sort(reverse=True, key=lambda x: x[1], )
        while len(ordenados_graus) != 0:
            selected = ordenados_graus.pop(0)[0]  # Pega vértice com maior grau
            independant_set.add(selected)
            for neighbour in self.neighbours(selected):
                for tupla in ordenados_graus:
                    if tupla[0] == neighbour:
                        ordenados_graus.remove(tupla)
                        break

        return independant_set

    def checkExistingCycle(self, entrance):
        """
        Essa funcao retorna um ciclo de um grafo euleriano.
        Ou seja, já sabemos que existe um ciclo para ser retornado
        antes de chamar esse metodo.
        :return: True se houver, False caso contrário.
        """

        def recursive(vertex):
            visited_vertexes[vertex] = True
            for neighbour in self.neighbours(vertex):
                # Caso o vértice de destino seja entrance
                # e a aresta até ele não seja a aresta da qual saímos de entrance
                if neighbour == entrance and (entrance, vertex) not in cycle:
                    cycle.add((vertex, neighbour))
                    return True

                # Só vai para vertices as quais não visitamos antes
                if not visited_vertexes[neighbour]:
                    visited_vertexes[neighbour] = True
                    cycle.add((vertex, neighbour))
                    if recursive(neighbour):
                        return True
            return False

        cycle = set()
        visited_vertexes = [False for vertex in range(len(self._matrix))]
        recursive(entrance)

        return cycle

    def hierholzer(self):
        """
        Encontra e retorna um ciclo euleriano
        :return:
        """

        # Define se o algoritmo se aplica ou nao
        if not self.checkEulerTheorem():
            print("Impossível aplicar Hierholzer, grafo não euleriano")
            return

        def degree(vertex_degrees):
            """
            Calcula grau do vertice, independentemente se o grafo é direcionado ou não
            :param vertex_degrees:
            :return: retorna o grau do vertice
            """
            cardinality = 0
            for edge in self.edges:
                if vertex_degrees == edge[0] or vertex_degrees == edge[1]:
                    cardinality += 1
            return cardinality

        def checkCycleC(vertex_cycle):
            """
            :param vertex_cycle:
            :return: se o vertice faz parte do cycle_c ou nao
            """
            for edge in cycle_c:
                if edge[0] == vertex_cycle or edge[1] == vertex_cycle:
                    return True

            return False

        def saveCycle(entrance):
            """
            Função responsável por inserir ciclos na trilha euleriana e
            remover as arestas dessa trilha do grafo original
            :param entrance:
            """
            new_trail = []

            # print("edges ", self.edges)
            # print("CICLO ", self.checkExistingCycle(entrance))

            # Armazena as arestas do ciclo encontrado para o vertice inicial escolhido
            for edge in self.checkExistingCycle(entrance):
                for existingEdge in self.edges:
                    if (existingEdge[0], existingEdge[1]) == edge or (existingEdge[1], existingEdge[0]) == edge:
                        new_trail.append(existingEdge)

            # print("removido ",new_trail)
            first = None
            for edge in new_trail:
                first = edge[0]
                break

            index = 0
            for edge in cycle_c:
                if edge[0] == first or edge[1] == first:
                    index += 1
                    break
                index += 1

            # print("INDICE ",index)

            for edge in new_trail:
                cycle_c.insert(index, edge)

            # Remove as arestas armazenadas em new_trail do grafo original
            for edge in new_trail:
                self.edges.remove(edge)
                self._matrix[edge[0]][edge[1]] = None
                self._matrix[edge[1]][edge[0]] = None
            return

        # Faz cópias das estruturas originais que precisaram ser alteradas
        original_graph = self.edges.copy()
        original_matrix = self._matrix.copy()
        cycle_c = []

        # Realiza alteracoes necessarias ao encontrar o primeiro ciclo
        saveCycle(0)

        # PARA TESTES
        # verifica se ciclo foi removido corretamente
        # print(self.edges)
        # print(cycle_c)
        # print(self.__matrix)
        # print(len(graphG))

        # Enqanto o grafo nao for vazio
        while len(self.edges) > 0:
            for vertex in self.vertexes:
                if (degree(vertex) > 0) and (checkCycleC(vertex)):
                    saveCycle(vertex)

        self.edges = original_graph
        self._matrix = original_matrix

        return cycle_c
