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
