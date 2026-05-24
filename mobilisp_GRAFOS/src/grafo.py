"""
============================================================================
Projeto MOBILISP - Mobilidade Turística de São Paulo
Disciplina: Teoria dos Grafos - Turma 6G
Professor: Ivan Carlos Alcântara de Oliveira

Integrantes do grupo:
- Luiz Eduardo Bacha dos Santos — RA 10425296
- Guilherme Haddad Borro       — RA 10427699

Síntese do conteúdo do arquivo:
Define a classe Grafo (dígrafo ponderado, representado por lista de
adjacência) com todas as operações da aplicação: leitura/gravação em
arquivo, manipulação de vértices e arestas, matriz de adjacência, análise
de conexidade (CFCs por Kosaraju e classificação C0..C3) e, a partir da
Parte 3, a solução do problema por caminho mínimo (Dijkstra) e quatro
técnicas para descobrir características do grafo (graus, euleriano,
hamiltoniano e coloração).

============================================================================
"""

import heapq
from collections import defaultdict


class Grafo:
    """Dígrafo ponderado representado por lista de adjacência.

    Atributos:
        tipo (int): código do tipo de grafo (6 = direcionado e ponderado).
        vertices (dict): mapeia id do vértice -> rótulo (str).
        adj (defaultdict[list]): adj[origem] = lista de tuplas (destino, peso).
    """

    def __init__(self, tipo):
        self.tipo = tipo
        self.vertices = {}
        self.adj = defaultdict(list)

    # ------------------------------------------------------------------ #
    # Manipulação de vértices e arestas
    # ------------------------------------------------------------------ #
    def inserir_vertice(self, vid, rotulo):
        """
        Insere um vértice no grafo com um identificador e rótulo.

        Parâmetros:
        vid (int): ID do vértice a ser inserido.
        rotulo (str): Rótulo (nome) do vértice.

        Retorna:
        Tuple: (bool, str) - True se o vértice foi inserido com sucesso e a mensagem correspondente.
        """
        if vid in self.vertices:
            return (False, "Vértice " + str(vid) + " já existe.")
        self.vertices[vid] = rotulo
        self.adj[vid]  # garante a entrada na lista de adjacência
        return (True, "Vértice " + str(vid) + " inserido com sucesso.")

    def inserir_aresta(self, origem, destino, peso):
        """
        Insere uma aresta direcionada entre dois vértices com peso especificado.

        Parâmetros:
        origem (int): Vértice de origem da aresta.
        destino (int): Vértice de destino da aresta.
        peso (float): Peso da aresta (tempo de deslocamento, por exemplo).

        Retorna:
        Tuple: (bool, str) - True se a aresta foi inserida com sucesso e a mensagem correspondente.
        """
        if origem not in self.vertices or destino not in self.vertices:
            return (False, "Origem ou destino inexistente.")
        for d, _ in self.adj[origem]:
            if d == destino:
                return (False, "Aresta já existe. Remova antes de inserir novamente.")
        self.adj[origem].append((destino, peso))
        return (True, "Aresta " + str(origem) + " -> " + str(destino) +
                " com peso " + str(peso) + " inserida.")

    def remover_aresta(self, origem, destino):
        """
        Remove uma aresta direcionada entre dois vértices.

        Parâmetros:
        origem (int): Vértice de origem da aresta a ser removida.
        destino (int): Vértice de destino da aresta a ser removida.

        Retorna:
        Tuple: (bool, str) - True se a aresta foi removida com sucesso e a mensagem correspondente.
        """
        if origem not in self.vertices:
            return (False, "Vértice de origem inexistente.")
        tamanho_antes = len(self.adj[origem])
        self.adj[origem] = [(d, p) for d, p in self.adj[origem] if d != destino]
        if len(self.adj[origem]) < tamanho_antes:
            return (True, "Aresta " + str(origem) + " -> " + str(destino) + " removida.")
        return (False, "Aresta não encontrada.")

    def remover_vertice(self, vid):
        """
        Remove um vértice do grafo, bem como todas as arestas associadas a ele.

        Parâmetros:
        vid (int): ID do vértice a ser removido.

        Retorna:
        Tuple: (bool, str) - True se o vértice foi removido com sucesso e a mensagem correspondente.
        """
        if vid not in self.vertices:
            return (False, "Vértice inexistente.")
        del self.vertices[vid]
        if vid in self.adj:
            del self.adj[vid]
        # remove arestas que apontavam para o vértice excluído
        for origem in list(self.adj.keys()):
            self.adj[origem] = [(d, p) for d, p in self.adj[origem] if d != vid]
        return (True, "Vértice " + str(vid) + " removido com sucesso.")

    def listar_arestas(self):
        """
        Retorna todas as arestas do grafo.

        Retorna:
        List: Uma lista contendo tuplas de arestas (origem, destino, peso).
        """
        arestas = []
        for origem in self.adj:
            for destino, peso in self.adj[origem]:
                arestas.append((origem, destino, peso))
        return arestas

    # ------------------------------------------------------------------ #
    # Exibição
    # ------------------------------------------------------------------ #
    def formatar_grafo(self):
        """
        Formata e retorna uma representação textual do grafo como lista de adjacência.

        Retorna:
        str: Representação textual do grafo.
        """
        linhas = ["\n===== GRAFO (Lista de Adjacência) ====="]
        if not self.vertices:
            linhas.append("Grafo vazio.")
            return "\n".join(linhas)
        for vid in sorted(self.vertices):
            rotulo = self.vertices[vid]
            conexoes = []
            for destino, peso in sorted(self.adj.get(vid, [])):
                nome = self.vertices.get(destino, "???")
                conexoes.append("(" + nome + " - " + str(peso) + " min)")
            linhas.append(str(vid) + " - " + rotulo + " -> [" + ", ".join(conexoes) + "]")
        linhas.append("=======================================\n")
        return "\n".join(linhas)

    def formatar_conteudo(self):
        """
        Formata e retorna o conteúdo atual do grafo, incluindo vértices e arestas.

        Retorna:
        str: Representação do conteúdo atual do grafo.
        """
        linhas = ["\n===== CONTEÚDO ATUAL DO GRAFO ====="]
        linhas.append("Tipo do grafo: " + str(self.tipo))
        linhas.append("Número de vértices: " + str(len(self.vertices)))
        for vid in sorted(self.vertices):
            linhas.append(str(vid) + " \"" + self.vertices[vid] + "\"")
        arestas = self.listar_arestas()
        linhas.append("Número de arestas: " + str(len(arestas)))
        for origem, destino, peso in sorted(arestas):
            linhas.append(str(origem) + " " + str(destino) + " " + str(peso))
        linhas.append("===================================\n")
        return "\n".join(linhas)

    # ------------------------------------------------------------------ #
    # Arquivo
    # ------------------------------------------------------------------ #
    def gravar_arquivo(self, nome_arquivo):
        """
        Grava o grafo atual em um arquivo .txt.

        Parâmetros:
        nome_arquivo (str): Nome do arquivo onde os dados do grafo serão gravados.
        """
        with open(nome_arquivo, "w", encoding="utf-8") as f:
            f.write(str(self.tipo) + "\n")
            f.write(str(len(self.vertices)) + "\n")
            for vid in sorted(self.vertices):
                f.write(str(vid) + " \"" + self.vertices[vid] + "\"\n")
            arestas = self.listar_arestas()
            f.write(str(len(arestas)) + "\n")
            for origem, destino, peso in sorted(arestas):
                f.write(str(origem) + " " + str(destino) + " " + str(peso) + "\n")

    def ler_arquivo(self, nome_arquivo):
        """
        Lê um arquivo .txt e monta o grafo com base nas informações do arquivo.

        Parâmetros:
        nome_arquivo (str): Nome do arquivo do qual o grafo será lido.
        """
        with open(nome_arquivo, "r", encoding="utf-8") as f:
            linhas = [linha.strip() for linha in f if linha.strip()]
        idx = 0
        self.tipo = int(linhas[idx]); idx += 1
        n = int(linhas[idx]); idx += 1
        self.vertices.clear()
        self.adj.clear()
        for _ in range(n):
            partes = linhas[idx].split(" ", 1); idx += 1
            id_vertice = int(partes[0])
            rotulo = partes[1].strip().strip("\"")
            self.vertices[id_vertice] = rotulo
            self.adj[id_vertice]
        m = int(linhas[idx]); idx += 1
        for _ in range(m):
            partes = linhas[idx].split(); idx += 1
            origem = int(partes[0])
            destino = int(partes[1])
            peso = float(partes[2])
            self.adj[origem].append((destino, peso))

    # ------------------------------------------------------------------ #
    # Conexidade (Kosaraju + classificação C0..C3)
    # ------------------------------------------------------------------ #
    def _grafo_transposto(self):
        """
        Cria e retorna o grafo transposto, onde as arestas são invertidas.

        Retorna:
        Grafo: Uma nova instância de Grafo com as arestas invertidas.
        """
        gt = Grafo(tipo=self.tipo)
        gt.vertices = self.vertices.copy()
        for v in self.adj:
            for destino, peso in self.adj[v]:
                gt.adj[destino].append((v, peso))
        return gt

    def _dfs_ordem(self, v, visitados, pilha):
        """
        DFS que ordena os vértices pela ordem de término (1ª fase de Kosaraju).
        """
        visitados.add(v)
        for vizinho, _ in self.adj[v]:
            if vizinho not in visitados:
                self._dfs_ordem(vizinho, visitados, pilha)
        pilha.append(v)

    def _dfs_componente(self, v, visitados, componente):
        """
        DFS que coleta os vértices de uma componente fortemente conexa.
        """
        visitados.add(v)
        componente.append(v)
        for vizinho, _ in self.adj[v]:
            if vizinho not in visitados:
                self._dfs_componente(vizinho, visitados, componente)

    def componentes_fortemente_conexas(self):
        """
        Encontra as Componentes Fortemente Conexas (CFCs) usando o algoritmo de Kosaraju.

        Retorna:
        list: Uma lista de listas, cada sublista contém os vértices de uma CFC.
        """
        pilha = []
        visitados = set()
        for v in self.vertices:
            if v not in visitados:
                self._dfs_ordem(v, visitados, pilha)
        gt = self._grafo_transposto()
        visitados.clear()
        componentes = []
        while pilha:
            v = pilha.pop()
            if v not in visitados:
                componente = []
                gt._dfs_componente(v, visitados, componente)
                componentes.append(componente)
        return componentes

    def simplesmente_conexo(self):
        """
        Verifica se o grafo é simplesmente conexo (conexo desconsiderando a direção).

        Retorna:
        bool: True se for simplesmente conexo, False caso contrário.
        """
        if not self.vertices:
            return True
        adj_nao_dir = defaultdict(list)
        for v in self.vertices:
            adj_nao_dir[v]
        for origem in self.adj:
            for destino, _ in self.adj[origem]:
                adj_nao_dir[origem].append(destino)
                adj_nao_dir[destino].append(origem)
        inicio = next(iter(self.vertices))
        visitados = set()
        pilha = [inicio]
        while pilha:
            v = pilha.pop()
            if v not in visitados:
                visitados.add(v)
                for vizinho in adj_nao_dir[v]:
                    if vizinho not in visitados:
                        pilha.append(vizinho)
        return len(visitados) == len(self.vertices)

    def semifortemente_conexo(self):
        """
        Verifica se o grafo é semi-fortemente conexo (para todo par u,v existe
        caminho de u para v OU de v para u).

        Retorna:
        bool: True se for semi-fortemente conexo, False caso contrário.
        """
        vertices = list(self.vertices.keys())

        def alcanca(origem, destino):
            visitados = set()
            pilha = [origem]
            while pilha:
                u = pilha.pop()
                if u == destino:
                    return True
                if u not in visitados:
                    visitados.add(u)
                    for v, _ in self.adj[u]:
                        pilha.append(v)
            return destino in visitados

        for i in range(len(vertices)):
            for j in range(i + 1, len(vertices)):
                u = vertices[i]
                v = vertices[j]
                if not alcanca(u, v) and not alcanca(v, u):
                    return False
        return True

    def classificar_conexidade_digrafo(self):
        """
        Classifica a conectividade do dígrafo nas categorias C3, C2, C1 ou C0.

        Retorna:
        str: A classificação da conectividade (C3, C2, C1 ou C0).
        """
        if not self.vertices:
            return "C3 (grafo vazio tratado localmente como fortemente conexo)"
        if len(self.componentes_fortemente_conexas()) == 1:
            return "C3 - Fortemente conexo"
        if self.semifortemente_conexo():
            return "C2 - Semi-fortemente conexo"
        if self.simplesmente_conexo():
            return "C1 - Simplesmente conexo"
        return "C0 - Desconexo"

    def grafo_reduzido(self):
        """
        Constrói o grafo reduzido (condensação) a partir das CFCs.

        Retorna:
        Tuple: (lista das CFCs, dict de adjacência entre componentes).
        """
        cfc = self.componentes_fortemente_conexas()
        mapa = {}
        for i, comp in enumerate(cfc):
            for v in comp:
                mapa[v] = i
        reduzido = defaultdict(set)
        for origem in self.adj:
            for destino, _ in self.adj[origem]:
                co = mapa[origem]
                cd = mapa[destino]
                if co != cd:
                    reduzido[co].add(cd)
        return cfc, reduzido

    # ------------------------------------------------------------------ #
    # Matriz de adjacência
    # ------------------------------------------------------------------ #
    def gerar_matriz_adjacencia(self):
        """
        Gera a matriz de adjacência do grafo.

        Retorna:
        Tuple: (matriz, nomes) - matriz de pesos e a lista de nomes dos vértices.
        """
        ids = sorted(self.vertices.keys())
        nomes = [self.vertices[vid] for vid in ids]
        indice = {vid: i for i, vid in enumerate(ids)}
        n = len(ids)
        matriz = [[0.0 for _ in range(n)] for _ in range(n)]
        for origem in self.adj:
            for destino, peso in self.adj[origem]:
                if origem in indice and destino in indice:
                    matriz[indice[origem]][indice[destino]] = peso
        return matriz, nomes

    def salvar_matriz_txt(self, nome_arquivo="matriz.txt"):
        """
        Salva a matriz de adjacência do grafo em um arquivo .txt.

        Parâmetros:
        nome_arquivo (str): Nome do arquivo (padrão: "matriz.txt").
        """
        matriz, nomes = self.gerar_matriz_adjacencia()
        with open(nome_arquivo, "w", encoding="utf-8") as f:
            f.write("===== MATRIZ DE ADJACÊNCIA =====\n\n")
            for linha in matriz:
                linha_str = ",".join(str(p) for p in linha)
                f.write(linha_str + ",\n")
            f.write("\n================================\n")
        print("Matriz de adjacência salva em '" + str(nome_arquivo) + "'.")

    # ================================================================== #
    #                          PARTE 3                                    #
    # ================================================================== #
    # Item 1 - SOLUÇÃO DO PROBLEMA: caminho mínimo (Dijkstra)             #
    # ------------------------------------------------------------------ #
    def dijkstra(self, origem, destino):
        """
        Calcula a rota de MENOR TEMPO entre dois pontos com o algoritmo de
        Dijkstra (resolve o problema central do MOBILISP: deslocamento mais
        rápido entre estações/pontos turísticos). Válido pois todos os pesos
        (tempos de deslocamento) são positivos.

        Parâmetros:
        origem (int): vértice de partida.
        destino (int): vértice de chegada.

        Retorna:
        Tuple: (distancia_total, caminho) onde caminho é a lista de ids de
        vértices. Se não houver caminho, retorna (float('inf'), []).
        """
        if origem not in self.vertices or destino not in self.vertices:
            return (float("inf"), [])

        distancia = {v: float("inf") for v in self.vertices}
        anterior = {v: None for v in self.vertices}
        distancia[origem] = 0.0

        # fila de prioridade: (distancia_acumulada, vertice)
        fila = [(0.0, origem)]
        visitados = set()

        while fila:
            dist_u, u = heapq.heappop(fila)
            if u in visitados:
                continue
            visitados.add(u)
            if u == destino:
                break
            for vizinho, peso in self.adj[u]:
                if vizinho in visitados:
                    continue
                nova = dist_u + peso
                if nova < distancia[vizinho]:
                    distancia[vizinho] = nova
                    anterior[vizinho] = u
                    heapq.heappush(fila, (nova, vizinho))

        if distancia[destino] == float("inf"):
            return (float("inf"), [])

        # reconstrói o caminho de trás para frente
        caminho = []
        atual = destino
        while atual is not None:
            caminho.append(atual)
            atual = anterior[atual]
        caminho.reverse()
        return (distancia[destino], caminho)

    # ------------------------------------------------------------------ #
    # Item 2 - Característica 1: grau dos vértices                        #
    # ------------------------------------------------------------------ #
    def grau_vertices(self):
        """
        Calcula o grau de entrada, de saída e total de cada vértice do dígrafo.

        Retorna:
        dict: {vid: {"entrada": int, "saida": int, "total": int}}.
        """
        graus = {v: {"entrada": 0, "saida": 0, "total": 0} for v in self.vertices}
        for origem in self.adj:
            for destino, _ in self.adj[origem]:
                if origem in graus:
                    graus[origem]["saida"] += 1
                if destino in graus:
                    graus[destino]["entrada"] += 1
        for v in graus:
            graus[v]["total"] = graus[v]["entrada"] + graus[v]["saida"]
        return graus

    # ------------------------------------------------------------------ #
    # Item 2 - Característica 2: euleriano (circuito / caminho)           #
    # ------------------------------------------------------------------ #
    def _conexo_ignorando_isolados(self):
        """Verifica conexidade (sentido fraco) considerando só vértices com grau > 0."""
        graus = self.grau_vertices()
        ativos = [v for v in self.vertices if graus[v]["total"] > 0]
        if not ativos:
            return True
        adj_nao_dir = defaultdict(set)
        for origem in self.adj:
            for destino, _ in self.adj[origem]:
                adj_nao_dir[origem].add(destino)
                adj_nao_dir[destino].add(origem)
        visitados = set()
        pilha = [ativos[0]]
        while pilha:
            u = pilha.pop()
            if u not in visitados:
                visitados.add(u)
                for w in adj_nao_dir[u]:
                    if w not in visitados:
                        pilha.append(w)
        return all(v in visitados for v in ativos)

    def verificar_euleriano(self):
        """
        Verifica se o dígrafo admite CIRCUITO euleriano ou CAMINHO euleriano.

        Para dígrafos conexos (no sentido fraco):
        - Circuito euleriano: grau_entrada == grau_saida em todos os vértices.
        - Caminho euleriano: exatamente um vértice com saida-entrada=+1 (início),
          exatamente um com entrada-saida=+1 (fim) e os demais equilibrados.

        Retorna:
        Tuple: (tem_circuito, tem_caminho, mensagem).
        """
        if not self.vertices:
            return (False, False, "Grafo vazio.")
        if not self._conexo_ignorando_isolados():
            return (False, False, "Não é euleriano: o grafo não é conexo.")

        graus = self.grau_vertices()
        mais_saida = 0   # vértices com saida = entrada + 1
        mais_entrada = 0  # vértices com entrada = saida + 1
        equilibrados = 0
        for v in self.vertices:
            dif = graus[v]["saida"] - graus[v]["entrada"]
            if dif == 0:
                equilibrados += 1
            elif dif == 1:
                mais_saida += 1
            elif dif == -1:
                mais_entrada += 1
            else:
                return (False, False, "Não é euleriano: diferença de grau maior que 1 em algum vértice.")

        if mais_saida == 0 and mais_entrada == 0:
            return (True, True, "Admite CIRCUITO euleriano (todo vértice tem grau de entrada igual ao de saída).")
        if mais_saida == 1 and mais_entrada == 1:
            return (False, True, "Admite CAMINHO euleriano (um vértice inicial e um final), mas não circuito.")
        return (False, False, "Não é euleriano (condição de graus não satisfeita).")

    # ------------------------------------------------------------------ #
    # Item 2 - Característica 3: hamiltoniano (caminho / ciclo)           #
    # ------------------------------------------------------------------ #
    def verificar_hamiltoniano(self, limite_passos=30_000_000):
        """
        Procura, por backtracking, um CAMINHO hamiltoniano (passa por todos os
        vértices exatamente uma vez) e, em caso afirmativo, verifica se ele
        fecha em CICLO hamiltoniano. O problema é NP-difícil, por isso usam-se
        duas estratégias para tornar a busca viável e conclusiva:

        1. Poda de alcançabilidade: se algum vértice ainda não visitado não
           puder mais ser alcançado (não tem predecessor não visitado e não é
           sucessor direto do vértice atual), o ramo é abandonado.
        2. Ordenação de Warnsdorff: tenta primeiro o sucessor com menos opções
           de saída disponíveis, reduzindo drasticamente a árvore de busca.

        Parâmetros:
        limite_passos (int): teto de chamadas recursivas (proteção de tempo).

        Retorna:
        Tuple: (tem_caminho, tem_ciclo, caminho, mensagem).
        caminho é a lista de ids (vazia se não houver / limite atingido).
        """
        vertices = list(self.vertices.keys())
        n = len(vertices)
        if n == 0:
            return (False, False, [], "Grafo vazio.")

        # sucessores e predecessores para checagens em O(1)
        suc = {v: {d for d, _ in self.adj[v]} for v in self.vertices}
        pred = {v: set() for v in self.vertices}
        for origem in self.adj:
            for destino, _ in self.adj[origem]:
                pred[destino].add(origem)

        passos = [0]
        estouro = [False]

        def backtrack(atual, visitados, caminho):
            passos[0] += 1
            if passos[0] > limite_passos:
                estouro[0] = True
                return False
            if len(caminho) == n:
                return True
            # poda de alcançabilidade
            for w in self.vertices:
                if w not in visitados and not ((pred[w] - visitados) or w in suc[atual]):
                    return False
            # candidatos ordenados por menor nº de saídas disponíveis (Warnsdorff)
            candidatos = [w for w in suc[atual] if w not in visitados]
            candidatos.sort(key=lambda w: sum(1 for x in suc[w] if x not in visitados))
            for prox in candidatos:
                visitados.add(prox)
                caminho.append(prox)
                if backtrack(prox, visitados, caminho):
                    return True
                caminho.pop()
                visitados.discard(prox)
            return False

        for inicio in vertices:
            caminho = [inicio]
            visitados = {inicio}
            if backtrack(inicio, visitados, caminho):
                fecha = caminho[0] in suc[caminho[-1]]
                if fecha:
                    return (True, True, caminho,
                            "Admite CAMINHO e CICLO hamiltoniano.")
                return (True, False, caminho,
                        "Admite CAMINHO hamiltoniano, mas não foi encontrado ciclo a partir dele.")
            if estouro[0]:
                break

        if estouro[0]:
            return (False, False, [],
                    "Busca interrompida pelo limite de passos (problema NP-difícil); "
                    "nenhum caminho hamiltoniano encontrado até o limite.")
        return (False, False, [],
                "Não admite caminho hamiltoniano (logo, também não admite ciclo hamiltoniano).")

    # ------------------------------------------------------------------ #
    # Item 2 - Característica 4: coloração (Welsh-Powell)                 #
    # ------------------------------------------------------------------ #
    def colorir_welsh_powell(self):
        """
        Aplica a coloração gulosa de Welsh-Powell sobre o grafo subjacente
        (não direcionado). Fornece um limite superior para o número cromático
        e o número de partições (conjuntos independentes) usadas.

        Retorna:
        Tuple: (num_cores, cores) onde cores = {vid: indice_da_cor}.
        """
        # grafo subjacente não direcionado (ignora sentido e laços)
        adj_nd = {v: set() for v in self.vertices}
        for origem in self.adj:
            for destino, _ in self.adj[origem]:
                if origem != destino:
                    adj_nd[origem].add(destino)
                    adj_nd[destino].add(origem)

        # ordena vértices por grau (não crescente) - heurística Welsh-Powell
        ordem = sorted(self.vertices.keys(),
                       key=lambda v: len(adj_nd[v]), reverse=True)

        cores = {}
        for v in ordem:
            usadas = {cores[w] for w in adj_nd[v] if w in cores}
            cor = 0
            while cor in usadas:
                cor += 1
            cores[v] = cor

        num_cores = (max(cores.values()) + 1) if cores else 0
        return num_cores, cores
