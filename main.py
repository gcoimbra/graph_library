#!/usr/bin/python3
# Trabalho prático Teoria e Modelo de Grafos
# Gabriel Coimbra - 3044
# Dalila Vieira - 3030
# 11/2018

from graph.Digraph import Digraph
from graph.AbstractGraph import AbstractGraph
from graph.Utils import readFile

[num_vertexes, input_edges] = readFile("../testes/grafo-1.txt")

graph = Digraph(num_vertexes, input_edges)
graph.write()
graph.neighbours(1)

# graph.showMatrix()
# graph.showProprieties()
# print("é bipartido?", graph.checkBiparity())
# print("é conexo?", graph.checkConectivity())
# print("busca largura", graph.breadthFirstSearch(0))
# print("busca profundidade", graph.deepFirstSearch(0))
# print("articulações", list(filter(graph.checkArticulation, range(num_vertexes))))
# print("pontes", list(filter(graph.checkBridge, input_edges)))

# shortest_route_matrix = graph.runFloydWarshall()
# print("tabela de distâncias\n")
# print(end="\t\t")
# for j in range(len(shortest_route_matrix)):
#     print(j, end="\t\t\t")
# print()
# for i in range(len(shortest_route_matrix)):
#     print(i, end="\t\t")
#     for j in range(len(shortest_route_matrix)):
#         print(shortest_route_matrix[i][j], end="\t\t\t")
#     print("\n")
#
#
# print("vértices em ciclos", list(filter(graph.checkCycles,graph.vertexes)))
# print("Escrevendo árvore geradora mínima")
# graph.writePrim()
# print("componentes conexas", graph.connectedComponents())
# print("É euleriano?", graph.checkEulerTheorem())
# print("conjunto independente", len(graph.independantSet()))
# print("Ciclo euleriano", graph.hierholzer())
