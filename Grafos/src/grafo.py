"""
Projeto MOBILISP - Mobilidade Turística de São Paulo

Integrantes do grupo:
- Luiz Eduardo Bacha dos Santos — RA 10425296 
- Guilherme Haddad Borro — RA 10427699

Descrição do conteúdo do arquivo:
Este código implementa a solução para o problema de modelagem da mobilidade turística em São Paulo, usando grafos direcionados. 
A aplicação oferece funcionalidades para leitura, gravação, manipulação de vértices e arestas, e análise de conectividade do grafo.
"""

from collections import defaultdict

class Grafo:
    """
    Classe Grafo:
    Representa um grafo direcionado com pesos nas arestas, utilizando lista de adjacência.

    Atributos:
    tipo: Define o tipo do grafo (0 a 7). O tipo 6 indica um grafo direcionado com pesos nas arestas.
    vertices: Dicionário que mapeia o ID do vértice para o rótulo do vértice.
    adj: Lista de adjacência que mapeia cada vértice para suas arestas e pesos.
    """
    def __init__(self, tipo=6):
        self.tipo = tipo
        self.vertices = {}
        self.adj = defaultdict(list) 

    def inserir_vertice(self, vid, rotulo):
        """
        Insere um vértice no grafo com um identificador e rótulo.

        Parâmetros:
        vid (int): ID do vértice a ser inserido.
        rotulo (str): Rótulo (nome) do vértice.

        Retorna:
        Tuple: (bool, str) - Retorna True se o vértice foi inserido com sucesso e a mensagem correspondente.
        """    
        if vid in self.vertices:
            return False, f"Vértice {vid} já existe."
        self.vertices[vid] = rotulo
        self.adj[vid] = []
        return True, f"Vértice {vid} inserido com sucesso."

    def inserir_aresta(self, origem, destino, peso):
        """
        Insere uma aresta direcionada entre dois vértices com peso especificado.

        Parâmetros:
        origem (int): Vértice de origem da aresta.
        destino (int): Vértice de destino da aresta.
        peso (float): Peso da aresta (tempo de deslocamento, por exemplo).

        Retorna:
        Tuple: (bool, str) - Retorna True se a aresta foi inserida com sucesso e a mensagem correspondente.
        """
        if origem not in self.vertices or destino not in self.vertices:
            return False, "Origem ou destino inexistente."
        for d, _ in self.adj[origem]:
            if d == destino:
                return False, "Aresta já existe. Remova antes de inserir novamente."
        self.adj[origem].append((destino, peso))
        return True, f"Aresta {origem} -> {destino} com peso {peso} inserida."

    def remover_aresta(self, origem, destino):
        """
        Remove uma aresta direcionada entre dois vértices.

        Parâmetros:
        origem (int): Vértice de origem da aresta a ser removida.
        destino (int): Vértice de destino da aresta a ser removida.

        Retorna:
        Tuple: (bool, str) - Retorna True se a aresta foi removida com sucesso e a mensagem correspondente.
        """
        if origem not in self.vertices:
            return False, "Vértice de origem inexistente."
        tamanho_antes = len(self.adj[origem])
        self.adj[origem] = [(d, p) for d, p in self.adj[origem] if d != destino]
        if len(self.adj[origem]) < tamanho_antes:
            return True, f"Aresta {origem} -> {destino} removida."
        return False, "Aresta não encontrada."

    def remover_vertice(self, vid): 
        """
        Remove um vértice do grafo, bem como todas as arestas associadas a ele.

        Parâmetros:
        vid (int): ID do vértice a ser removido.

        Retorna:
        Tuple: (bool, str) - Retorna True se o vértice foi removido com sucesso e a mensagem correspondente.
        """        
        if vid not in self.vertices:
            return False, "Vértice inexistente."
        del self.vertices[vid]
        if vid in self.adj:
            del self.adj[vid]
        for origem in list(self.adj.keys()):
            self.adj[origem] = [(d, p) for d, p in self.adj[origem] if d != vid]
        return True, f"Vértice {vid} removido com sucesso."

    def listar_arestas(self):
        """
        Retorna todas as arestas do grafo.

        Parâmetros:
        Nenhum

        Retorna:
        List: Uma lista contendo tuplas de arestas (origem, destino, peso).
        """
        arestas = []
        for origem in self.adj:
            for destino, peso in self.adj[origem]:
                arestas.append((origem, destino, peso))
        return arestas

    def formatar_grafo(self):
        """
        Formata e retorna uma representação textual do grafo como lista de adjacência.

        Parâmetros:
        Nenhum

        Retorna:
        str: Representação textual do grafo.
        """
        linhas = ["\n===== GRAFO (Lista de Adjacência) ====="]
        if not self.vertices:
            linhas.append("Grafo vazio.")
            return "\n".join(linhas)
        for vid in sorted(self.vertices):
            rotulo = self.vertices[vid]
            conexoes = ", ".join(
                [f"{destino}({self.vertices.get(destino, '???')}, {peso} min)" for destino, peso in self.adj[vid]]
            )
            linhas.append(f"{vid} - {rotulo} -> [{conexoes}]")
        linhas.append("=======================================\n")
        return "\n".join(linhas)

    def formatar_conteudo(self):
        """
        Formata e retorna o conteúdo atual do grafo, incluindo vértices e arestas.

        Parâmetros:
        Nenhum

        Retorna:
        str: Representação do conteúdo atual do grafo.
        """
        linhas = ["\n===== CONTEÚDO ATUAL DO GRAFO ====="]
        linhas.append(f"Tipo do grafo: {self.tipo}")
        linhas.append(f"Número de vértices: {len(self.vertices)}")
        for vid in sorted(self.vertices):
            linhas.append(f'{vid} "{self.vertices[vid]}"')
        arestas = self.listar_arestas()
        linhas.append(f"Número de arestas: {len(arestas)}")
        for origem, destino, peso in arestas:
            linhas.append(f"{origem} {destino} {peso}")
        linhas.append("===================================\n")
        return "\n".join(linhas)

    def gravar_arquivo(self, nome_arquivo):
        """
        Grava o grafo atual em um arquivo .txt.

        Parâmetros:
        nome_arquivo (str): Nome do arquivo onde os dados do grafo serão gravados.

        Retorna:
        Nenhum
        """
        with open(nome_arquivo, "w", encoding="utf-8") as f:
            f.write(f"{self.tipo}\n")
            f.write(f"{len(self.vertices)}\n")
            for vid in sorted(self.vertices):
                f.write(f'{vid} "{self.vertices[vid]}"\n')
            arestas = self.listar_arestas()
            f.write(f"{len(arestas)}\n")
            for origem, destino, peso in arestas:
                f.write(f"{origem} {destino} {peso}\n")

    def ler_arquivo(self, nome_arquivo):
        """
        Lê um arquivo .txt e monta o grafo com base nas informações do arquivo.

        Parâmetros:
        nome_arquivo (str): Nome do arquivo do qual o grafo será lido.

        Retorna:
        Nenhum
        """
        with open(nome_arquivo, "r", encoding="utf-8") as f:
            linhas = [linha.strip() for linha in f if linha.strip()]
        idx = 0
        self.tipo = int(linhas[idx]); idx += 1
        n = int(linhas[idx]); idx += 1
        self.vertices.clear(); self.adj.clear()
        for _ in range(n):
            linha = linhas[idx]; idx += 1
            partes = linha.split('"')
            id_vertice = int(partes[0].strip())
            rotulo = partes[1].strip()
            self.vertices[id_vertice] = rotulo
            self.adj[id_vertice] = []
        m = int(linhas[idx]); idx += 1
        for _ in range(m):
            origem, destino, peso = linhas[idx].split(); idx += 1
            self.adj[int(origem)].append((int(destino), float(peso)))

    def _grafo_transposto(self):
        """
        Cria e retorna o grafo transposto, onde as arestas são invertidas.

        Parâmetros:
        Nenhum

        Retorna:
        Grafo: Uma nova instância de Grafo com as arestas invertidas.
        """
        gt = Grafo(tipo=self.tipo)
        gt.vertices = self.vertices.copy()
        for v in self.vertices:
            gt.adj[v] = []
        for origem in self.adj:
            for destino, peso in self.adj[origem]:
                gt.adj[destino].append((origem, peso))
        return gt

    def _dfs_ordem(self, v, visitados, pilha):
        """
        Realiza a busca em profundidade (DFS) para ordenar os vértices pela ordem de término.

        Parâmetros:
        v (int): Vértice atual da DFS.
        visitados (set): Conjunto de vértices já visitados.
        pilha (list): Lista de vértices ordenados pela ordem de término.

        Retorna:
        Nenhum
        """
        visitados.add(v)
        for vizinho, _ in self.adj[v]:
            if vizinho not in visitados:
                self._dfs_ordem(vizinho, visitados, pilha)
        pilha.append(v)

    def _dfs_componente(self, v, visitados, componente):
        """
        Realiza a busca em profundidade (DFS) para encontrar uma componente fortemente conexa.

        Parâmetros:
        v (int): Vértice inicial da DFS.
        visitados (set): Conjunto de vértices já visitados.
        componente (list): Lista onde a componente fortemente conexa será armazenada.

        Retorna:
        Nenhum
        """
        visitados.add(v)
        componente.append(v)
        for vizinho, _ in self.adj[v]:
            if vizinho not in visitados:
                self._dfs_componente(vizinho, visitados, componente)

    def componentes_fortemente_conexas(self):
        """
        Encontra as Componentes Fortemente Conexas (CFCs) do grafo usando o algoritmo de Kosaraju.

        Parâmetros:
        Nenhum

        Retorna:
        list: Uma lista de listas, onde cada sublista contém os vértices de uma CFC.
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
        Verifica se o grafo é simplesmente conexo (conexo, desconsiderando a direção das arestas).

        Parâmetros:
        Nenhum

        Retorna:
        bool: True se o grafo for simplesmente conexo, False caso contrário.
        """
        if not self.vertices:
            return True
        adj_nao_dir = defaultdict(list)
        for v in self.vertices:
            adj_nao_dir[v] = []
        for origem in self.adj:
            for destino, _ in self.adj[origem]:
                adj_nao_dir[origem].append(destino)
                adj_nao_dir[destino].append(origem)
        inicio = next(iter(self.vertices))
        visitados = set(); pilha = [inicio]
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
        Verifica se o grafo é semi-fortemente conexo.

        Parâmetros:
        Nenhum

        Retorna:
        bool: True se o grafo for semi-fortemente conexo, False caso contrário.
        """
        vertices = list(self.vertices.keys())
        def alcanca(origem, destino):
            visitados = set(); pilha = [origem]
            while pilha:
                v = pilha.pop()
                if v == destino:
                    return True
                if v not in visitados:
                    visitados.add(v)
                    for vizinho, _ in self.adj[v]:
                        if vizinho not in visitados:
                            pilha.append(vizinho)
            return False
        for i in range(len(vertices)):
            for j in range(i + 1, len(vertices)):
                u, v = vertices[i], vertices[j]
                if not (alcanca(u, v) or alcanca(v, u)):
                    return False
        return True

    def classificar_conexidade_digrafo(self):
        """
        Classifica a conectividade do grafo direcionado nas categorias C3, C2, C1 ou C0.

        Parâmetros:
        Nenhum

        Retorna:
        str: A classificação da conectividade (C3, C2, C1, ou C0).
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
        Exibe as componentes fortemente conexas e o grafo reduzido do grafo fornecido.

        Parâmetros:
        grafo (Grafo): Instância da classe Grafo contendo o grafo a ser analisado.

        Retorna:
        Nenhum. A função imprime as componentes e o grafo reduzido.
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
    
    def gerar_matriz_adjacencia(self):
        """
        Gera a matriz de adjacência do grafo.

        Parâmetros:
        Nenhum

        Retorna:
        Tuple: (list, list) - A primeira lista é a matriz de adjacência e a segunda lista contém os nomes dos vértices.
        """
        if not self.vertices:
            return []

        ids = sorted(self.vertices.keys())
        nomes = [self.vertices[vid] for vid in ids]
        indice = {vid: i for i, vid in enumerate(ids)}

        n = len(ids)
        matriz = [[0.0 for _ in range(n)] for _ in range(n)]

        for origem in self.adj:
            for destino, peso in self.adj[origem]:
                i = indice[origem]
                j = indice[destino]
                matriz[i][j] = peso

        return matriz, nomes
    
    def salvar_matriz_txt(self, nome_arquivo="matriz.txt"):
        """
        Salva a matriz de adjacência do grafo em um arquivo .txt.

        Parâmetros:
        nome_arquivo (str): Nome do arquivo para salvar a matriz de adjacência (padrão: "matriz.txt").
        
        Retorna:
        Nenhum. A função escreve diretamente no arquivo.
        """
        matriz, nomes = self.gerar_matriz_adjacencia()

        with open(nome_arquivo, "w") as f:
            f.write("===== MATRIZ DE ADJACÊNCIA =====\n\n")

            for linha in matriz:
                linha_str = ",".join(f"{val:.1f}" for val in linha)
                f.write(linha_str + "\n")

            f.write("\n================================\n")
