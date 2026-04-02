"""
Projeto MOBILISP - Mobilidade Turística de São Paulo

Integrantes do grupo:
- Luiz Eduardo Bacha dos Santos — RA 10425296 
- Guilherme Haddad Borro — RA 10427699

Descrição do conteúdo do arquivo:
Este código implementa a solução para o problema de modelagem da mobilidade turística em São Paulo, usando grafos direcionados. 
A aplicação oferece funcionalidades para leitura, gravação, manipulação de vértices e arestas, e análise de conectividade do grafo.
"""

from grafo import Grafo


def criar_grafo_exemplo_sp():
    """
    Cria um grafo de exemplo com 6 vértices representando estações de São Paulo e pontos turísticos.

    Retorna:
    Grafo: Uma instância do grafo com 6 vértices e algumas arestas de exemplo.
    """ 
    g = Grafo(tipo=6)
    g.inserir_vertice(1, "Estação Sé")
    g.inserir_vertice(2, "Estação Luz")
    g.inserir_vertice(3, "Estação Consolação")
    g.inserir_vertice(4, "MASP")
    g.inserir_vertice(5, "Mercadão")
    g.inserir_vertice(6, "Terminal Parque Dom Pedro")
    g.inserir_aresta(1, 2, 7)
    g.inserir_aresta(2, 1, 7)
    g.inserir_aresta(1, 3, 10)
    g.inserir_aresta(3, 4, 4)
    g.inserir_aresta(1, 5, 8)
    g.inserir_aresta(5, 6, 6)
    g.inserir_aresta(6, 1, 9)
    g.inserir_aresta(2, 5, 5)
    return g
