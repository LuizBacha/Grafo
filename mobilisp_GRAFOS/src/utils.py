"""
============================================================================
Projeto MOBILISP - Mobilidade Turística de São Paulo
Disciplina: Teoria dos Grafos - Turma 6G
Professor: Ivan Carlos Alcântara de Oliveira

Integrantes do grupo:
- Luiz Eduardo Bacha dos Santos — RA 10425296
- Guilherme Haddad Borro       — RA 10427699

Síntese do conteúdo do arquivo:
Funções auxiliares de exibição usadas pelo menu: apresentação das
componentes fortemente conexas e do grafo reduzido (Parte 2) e a
formatação dos resultados das técnicas da Parte 3 (caminho mínimo,
graus, euleriano, hamiltoniano e coloração).

============================================================================
"""

from collections import Counter


def exibir_grafo_reduzido(grafo):
    """Imprime as componentes fortemente conexas e o grafo reduzido."""
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


# --------------------------------------------------------------------- #
# Exibição das técnicas da Parte 3
# --------------------------------------------------------------------- #
def exibir_caminho_minimo(grafo, origem, destino):
    """Imprime a rota de menor tempo (Dijkstra) entre dois pontos."""
    distancia, caminho = grafo.dijkstra(origem, destino)
    print("\n===== CAMINHO MÍNIMO (Dijkstra) =====")
    if not caminho:
        print(f"Não existe rota de {origem} até {destino}.")
        print("=====================================\n")
        return
    nomes = " -> ".join(f"{v} ({grafo.vertices[v]})" for v in caminho)
    print(f"Origem : {origem} ({grafo.vertices[origem]})")
    print(f"Destino: {destino} ({grafo.vertices[destino]})")
    print(f"Tempo total estimado: {distancia} min")
    print(f"Rota: {nomes}")
    print("=====================================\n")


def exibir_graus(grafo):
    """Imprime grau de entrada, saída e total de cada vértice."""
    graus = grafo.grau_vertices()
    print("\n===== GRAU DOS VÉRTICES =====")
    for vid in sorted(graus):
        g = graus[vid]
        print(f"{vid:>3} {grafo.vertices[vid]:<32} "
              f"entrada={g['entrada']:>2}  saída={g['saida']:>2}  total={g['total']:>2}")
    totais = [g["total"] for g in graus.values()]
    if totais:
        print(f"\nGrau total mínimo: {min(totais)} | máximo: {max(totais)} | "
              f"médio: {sum(totais)/len(totais):.2f}")
    print("=============================\n")


def exibir_euleriano(grafo):
    """Imprime o resultado da verificação euleriana."""
    tem_circuito, tem_caminho, msg = grafo.verificar_euleriano()
    print("\n===== VERIFICAÇÃO EULERIANA =====")
    print(f"Admite circuito euleriano? {'SIM' if tem_circuito else 'NÃO'}")
    print(f"Admite caminho euleriano?  {'SIM' if tem_caminho else 'NÃO'}")
    print(f"Conclusão: {msg}")
    print("=================================\n")


def exibir_hamiltoniano(grafo):
    """Imprime o resultado da verificação hamiltoniana."""
    print("\n===== VERIFICAÇÃO HAMILTONIANA =====")
    print("(busca com poda; pode levar alguns segundos...)")
    tem_caminho, tem_ciclo, caminho, msg = grafo.verificar_hamiltoniano()
    print(f"Admite caminho hamiltoniano? {'SIM' if tem_caminho else 'NÃO'}")
    print(f"Admite ciclo hamiltoniano?   {'SIM' if tem_ciclo else 'NÃO'}")
    print(f"Conclusão: {msg}")
    if caminho:
        nomes = " -> ".join(f"{v} ({grafo.vertices[v]})" for v in caminho)
        print(f"Sequência: {nomes}")
    print("====================================\n")


def exibir_coloracao(grafo):
    """Imprime o resultado da coloração de Welsh-Powell."""
    num_cores, cores = grafo.colorir_welsh_powell()
    print("\n===== COLORAÇÃO (Welsh-Powell) =====")
    print(f"Número de cores utilizadas (partições): {num_cores}")
    contagem = Counter(cores.values())
    for cor in sorted(contagem):
        membros = [grafo.vertices[v] for v in sorted(cores) if cores[v] == cor]
        print(f"  Cor {cor}: {contagem[cor]} vértices -> {membros}")
    print("Obs.: número cromático <= cores acima (Welsh-Powell é um limite superior).")
    print("====================================\n")
