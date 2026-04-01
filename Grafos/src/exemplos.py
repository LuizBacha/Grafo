from grafo import Grafo


def criar_grafo_exemplo_sp():
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
