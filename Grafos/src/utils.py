"""
Projeto MOBILISP - Mobilidade Turística de São Paulo

Integrantes do grupo:
- Luiz Eduardo Bacha dos Santos — RA 10425296 
- Guilherme Haddad Borro — RA 10427699

Descrição do conteúdo do arquivo:
Este código implementa a solução para o problema de modelagem da mobilidade turística em São Paulo, usando grafos direcionados. 
A aplicação oferece funcionalidades para leitura, gravação, manipulação de vértices e arestas, e análise de conectividade do grafo.
"""

def exibir_grafo_reduzido(grafo):
    cfc, reduzido = grafo.grafo_reduzido()
    print("\n===== COMPONENTES FORTEMENTE CONEXAS =====") 
    for i, comp in enumerate(cfc):
        nomes = [grafo.vertices[v] for v in comp]
        print(f"Componente {i}: vértices {comp} | locais {nomes}")
    print("\n===== GRAFO REDUZIDO =====")
    for comp_origem in range(len(cfc)):
        destinos = sorted(list(reduzido.get(comp_origem, [])))
        print(f"Componente {comp_origem} -> {destinos}")
    print("==========================================\n")
