#!/usr/bin/python3
# Trabalho prático Teoria e Modelo de Grafos
# Gabriel Coimbra - 3044
# Dalila Vieira - 3030
# 11/2018

from os import system

from AbstractGraph.Graph import Graph

from AbstractGraph.Utils import readFile


def menu():
    print("Trabalho Prático - Teoria e Modelo De Grafos")
    print("\tGabriel Coimbra - 3044")
    print("\tDalila Vieira - 3030")
    print("Digite uma opção:")
    print("1 - Exibir matriz de pesos")
    print("2 - Exibir algumas propriedades do grafo")
    print("3 - Checar se o grafo é bipartido")
    print("4 - Checar se o grafo é conexo")
    print("5 - Checar se dado vértice é uma articulação")
    print("6 - Checar se dada aresta é uma ponte")
    print("7 - Escrever no arquivo imagem do grafo")
    print("8 - Exibir árvore de profundidade dado vértice")
    print("9 - Exibir árvore de largura dado vértice")
    print("10 - Matriz com menores distâncias")
    print("11 - Escrever no arquivo imagem da árvore geradora mínima dado vértice")
    print("12 - Checar se vértice é parte de ciclo")
    print("13 - Imprimir a cardinalidade de componentes conexas")
    print("14 - Checar se grafo é euleriano")
    print("15 - Imprimir maior conjunto independente encontrado")
    print("16 - Imprimir ciclo euleriano com algoritmo de Hierholzer")
    print("0 - Sair")


print("graph Discover Utility - GDU")

vertexes, edges_s = None, None
try:
    [vertexes, edges_s] = readFile("../testes/grafo-2.txt")

except FileNotFoundError:
    print("ERRO FATAL Arquivo inválido!")
    exit(-1)

while True:
    print("É um grafo direcionado? (s/n)")
    direcionado = str(input())
    if direcionado == "s":
        graph = Graph(vertexes, edges_s, True)
        break
    elif direcionado == "n":
        graph = Graph(vertexes, edges_s, False)
        break
    else:
        print("Opção inválida...")

while True:
    system("clear")
    menu()

    try:
        opcao = int(input())
    except ValueError:
        print("Opção inválida. Digite qualquer tecla para continuar...")
        input()
        continue

    if opcao == 0:
        exit()
    elif opcao == 1:
        graph.showMatrix()
    elif opcao == 2:
        graph.showProprieties()
    elif opcao == 3:
        print("Sim") if graph.checkBiparity() else print("Não")
    elif opcao == 4:
        print("Sim") if graph.checkConectivity()[0] else print("Não")
    elif opcao == 5:
        print("Qual vértice?")
        vertice = int(input())
        if graph.checkArticulation(vertice):
            print("Sim")
        else:
            print("Não")

    elif opcao == 6:
        print("Qual aresta? (x,y,w)")
        s = str(input())
        print(s[1], s[3])
        print("Sim") if graph.checkBridge((int(s[1]), int(s[3]), int(s[5]))) else print("Não")
    elif opcao == 7:
        graph.write()
    elif opcao == 8:
        print("Qual vértice?")
        retorno = graph.deepFirstSearch(int(input()))
        print("Sequencia de vértices visitados:", retorno[0], "\nArestas de retorno:", retorno[1], "\nArestas de avanço:", retorno[2])

    elif opcao == 9:
        print("Qual vértice?")
        retorno = graph.breadthFirstSearch(int(input()))
        print("Árvore",retorno[0],"\nSequencia de vértices visitados:", retorno[1], "\nArestas de retorno:", retorno[2])

    elif opcao == 10:
        shortest_route_matrix = graph.runFloydWarshall()


        i = 0
        while i < len(shortest_route_matrix):
            j = 0
            print(i, end=": ")
            while j < len(shortest_route_matrix[i]):
                # Caso não haja nenhum valor
                if shortest_route_matrix[i][j] is None:
                    print("\t*", end="\t")
                else:
                    print("\t" + str(shortest_route_matrix[i][j]), end="\t")
                j += 1
            print()
            i += 1

    elif opcao == 11:
        print("Qual vértice?")
        graph.writePrim(int(input()))
    elif opcao == 12:
        print("Qual vértice?")
        print("Sim") if graph.checkCycles(int(input())) else print("Não")
    elif opcao == 13:
        components = graph.connectedComponents()
        print(len(components), components)
    elif opcao == 14:
        print("Sim") if graph.checkEulerTheorem() else print("Não")
    elif opcao == 15:
        independant_set = graph.independantSet()
        print(len(independant_set), independant_set)
    elif opcao == 16:
        print(graph.hierholzer())

    print("Digite qualquer coisa para continuar...")
    input()
