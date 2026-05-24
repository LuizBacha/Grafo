# MobiLISP - Mobilidade Turística de São Paulo

Projeto em Python para modelar a mobilidade urbana de São Paulo com **grafo orientado e ponderado**.

## Estrutura

- `src/main.py`: menu principal
- `src/grafo.py`: classe do grafo e algoritmos principais
- `src/exemplos.py`: exemplo pequeno para testes rápidos
- `src/utils.py`: funções auxiliares de exibição
- `data/grafo.txt`: base com 80 vértices e 230 arestas

## Como executar

No terminal, dentro da pasta do projeto:

```bash
cd src
python main.py
```

## Menu de opções

Partes 1 e 2:
1. Ler dados do arquivo
2. Gravar dados no arquivo
3. Inserir vértice
4. Inserir aresta
5. Remover vértice
6. Remover aresta
7. Mostrar conteúdo do grafo
8. Mostrar grafo (lista de adjacência)
9. Conexidade (C0–C3) e grafo reduzido (CFCs por Kosaraju)
10. Carregar exemplo pequeno
11. Mostrar/salvar matriz de adjacência

Parte 3 — solução do problema e características:
12. **Caminho mínimo (Dijkstra)** — rota de menor tempo entre dois pontos
13. **Grau dos vértices** — grau de entrada, saída e total
14. **Verificação euleriana** — circuito/caminho euleriano
15. **Verificação hamiltoniana** — caminho/ciclo hamiltoniano (backtracking com poda)
16. **Coloração (Welsh-Powell)** — número de partições

## Observação

O arquivo `data/grafo.txt` já vem preenchido com uma base inicial de estações e pontos turísticos reais de São Paulo.
