# Trabalho prático Teoria e Modelo de Grafos
# Gabriel Coimbra - 3044
# Dalila Vieira - 3030
# 11/2018

import pygraphviz  # requerido para mostrar o grafo visualmente


def readFile(file=None):
    """
    :param file: string. source graph file
    Output:
    :rtype: vertexes and edges
    vertexes -> quantity of vertexes
    edges -> contains tuples tuples
    tuples -> (vertex1, vertex2, weight)
    vertex1, vertex2, weight -> integer
    """
    # Se a entrada for vazia, por padrão será grafo.txt
    if file is None:
        file = "grafo.txt"

    edges = set()
    i = 0
    with open(file) as file_stream:

        # Primeira linha terá a quantidade de vértices
        try:
            vertexes = int(file_stream.readline())
        except ValueError:
            raise RuntimeError("Arquivo inválido!")


        for line in file_stream:
            i += 1
            # Tira todos finais de linha
            line = line.replace("\n", "")

            # Transforma "line" em lista separando "line" pelos espaços
            line = line.split(" ")

            # Para cada elemento na linha,
            # transforma em inteiro e coloca de volta na linha
            line = [word for word in line]

            future_tuple = []

            # Adiciona no set a tripla obtida na linha anterior
            # Subtrai devido a divergências de notações
            try:
                if len(line) == 1:  # vértice  isolado
                    future_tuple.append(int(line[0]) - 1)

                if len(line) >= 2:  # vértice não isolado
                    future_tuple.append(int(line[0]) - 1)
                    future_tuple.append(int(line[1]) - 1)
                    future_tuple.append(float(line[2]))

            except IndexError:
                print("Erro de índice na linha", line)

            edges.add(tuple(future_tuple))

    # Retorna a lista com vertexes e edges
    return [vertexes, edges]


def write(is_direcionado, edges, file="grafo.png"):
    """
    Escreve no arquivo uma representação gráfica do grafo
    :param is_direcionado:
    :param edges:
    :param file: nome do arquivo
    :return:
    """
    # Inicializa grafo visual
    visual_graph = pygraphviz.AGraph(directed=is_direcionado)
    for edge in edges:
        edge_from = edge[0]
        edge_to = edge[1]
        edge_weight = edge[2]
        if len(edge) == 3:  # Caso o vértice não seja deconexo
            visual_graph.add_edge(edge_from, edge_to, edge_weight, label=str(edge_weight), weight=edge_weight)

        elif len(edge) == 1:  # Caso o vértice esteja desconectado
            node = edge[0]
            # TODO: gambi
            visual_graph.add_edge(node, node)

    visual_graph.layout()
    visual_graph.draw(file)
