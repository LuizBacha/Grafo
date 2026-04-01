from collections import defaultdict

class Grafo:
    def __init__(self, tipo=6):
        self.tipo = tipo
        self.vertices = {}
        self.adj = defaultdict(list) 

    def inserir_vertice(self, vid, rotulo):
        if vid in self.vertices:
            return False, f"Vértice {vid} já existe."
        self.vertices[vid] = rotulo
        self.adj[vid] = []
        return True, f"Vértice {vid} inserido com sucesso."

    def inserir_aresta(self, origem, destino, peso):
        if origem not in self.vertices or destino not in self.vertices:
            return False, "Origem ou destino inexistente."
        for d, _ in self.adj[origem]:
            if d == destino:
                return False, "Aresta já existe. Remova antes de inserir novamente."
        self.adj[origem].append((destino, peso))
        return True, f"Aresta {origem} -> {destino} com peso {peso} inserida."

    def remover_aresta(self, origem, destino):
        if origem not in self.vertices:
            return False, "Vértice de origem inexistente."
        tamanho_antes = len(self.adj[origem])
        self.adj[origem] = [(d, p) for d, p in self.adj[origem] if d != destino]
        if len(self.adj[origem]) < tamanho_antes:
            return True, f"Aresta {origem} -> {destino} removida."
        return False, "Aresta não encontrada."

    def remover_vertice(self, vid): 
        if vid not in self.vertices:
            return False, "Vértice inexistente."
        del self.vertices[vid]
        if vid in self.adj:
            del self.adj[vid]
        for origem in list(self.adj.keys()):
            self.adj[origem] = [(d, p) for d, p in self.adj[origem] if d != vid]
        return True, f"Vértice {vid} removido com sucesso."

    def listar_arestas(self):
        arestas = []
        for origem in self.adj:
            for destino, peso in self.adj[origem]:
                arestas.append((origem, destino, peso))
        return arestas

    def formatar_grafo(self):
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
        gt = Grafo(tipo=self.tipo)
        gt.vertices = self.vertices.copy()
        for v in self.vertices:
            gt.adj[v] = []
        for origem in self.adj:
            for destino, peso in self.adj[origem]:
                gt.adj[destino].append((origem, peso))
        return gt

    def _dfs_ordem(self, v, visitados, pilha):
        visitados.add(v)
        for vizinho, _ in self.adj[v]:
            if vizinho not in visitados:
                self._dfs_ordem(vizinho, visitados, pilha)
        pilha.append(v)

    def _dfs_componente(self, v, visitados, componente):
        visitados.add(v)
        componente.append(v)
        for vizinho, _ in self.adj[v]:
            if vizinho not in visitados:
                self._dfs_componente(vizinho, visitados, componente)

    def componentes_fortemente_conexas(self):
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
        matriz, nomes = self.gerar_matriz_adjacencia()

        with open(nome_arquivo, "w") as f:
            f.write("===== MATRIZ DE ADJACÊNCIA =====\n\n")

            for linha in matriz:
                linha_str = ",".join(f"{val:.1f}" for val in linha)
                f.write(linha_str + "\n")

            f.write("\n================================\n")
