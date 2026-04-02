"""
Projeto MOBILISP - Mobilidade Turística de São Paulo

Integrantes do grupo:
- Luiz Eduardo Bacha dos Santos — RA 10425296 
- Guilherme Haddad Borro — RA 10427699

Descrição do conteúdo do arquivo:
Este código implementa a solução para o problema de modelagem da mobilidade turística em São Paulo, usando grafos direcionados. 
A aplicação oferece funcionalidades para leitura, gravação, manipulação de vértices e arestas, e análise de conectividade do grafo.
"""

from pathlib import Path 
from grafo import Grafo
from exemplos import criar_grafo_exemplo_sp
from utils import exibir_grafo_reduzido
 
BASE_DIR = Path(__file__).resolve().parent.parent
ARQUIVO_PADRAO = BASE_DIR / "data" / "grafo.txt"
ARQUIVO_COPIA = BASE_DIR / "data" / "grafo - Copia.txt"


def menu(): 
    grafo = Grafo(tipo=6)
    while True:
        print("=" * 55)
        print("  MOBILISP - Mobilidade Turística de São Paulo")
        print("=" * 55)
        print(f"Arquivo padrão: {ARQUIVO_PADRAO}")
        print("1) Ler dados do arquivo grafo - Copia.txt")
        print("2) Gravar dados no arquivo grafo.txt")
        print("3) Inserir vértice")
        print("4) Inserir aresta")
        print("5) Remover vértice")
        print("6) Remover aresta")
        print("7) Mostrar conteúdo do grafo")
        print("8) Mostrar grafo")
        print("9) Apresentar conexidade e grafo reduzido")
        print("10) Carregar exemplo pequeno")
        print("11) Mostrar matriz de adjacência")
        print("0) Encerrar")
        opcao = input("Escolha uma opção: ").strip()

        try:
            if opcao == "1":
                grafo.ler_arquivo(ARQUIVO_COPIA)
                print("Arquivo lido com sucesso.")
            elif opcao == "2":
                grafo.gravar_arquivo(ARQUIVO_PADRAO)
                print("Arquivo gravado com sucesso.")
            elif opcao == "3":
                vid = int(input("ID do vértice: "))
                rotulo = input("Rótulo/localidade: ")
                print(grafo.inserir_vertice(vid, rotulo)[1])
            elif opcao == "4":
                origem = int(input("Origem: "))
                destino = int(input("Destino: "))
                peso = float(input("Tempo (min): "))
                print(grafo.inserir_aresta(origem, destino, peso)[1])
            elif opcao == "5":
                vid = int(input("ID do vértice a remover: "))
                print(grafo.remover_vertice(vid)[1])
            elif opcao == "6":
                origem = int(input("Origem: "))
                destino = int(input("Destino: "))
                print(grafo.remover_aresta(origem, destino)[1])
            elif opcao == "7":
                print(grafo.formatar_conteudo())
            elif opcao == "8":
                print(grafo.formatar_grafo())
            elif opcao == "9":
                print("\nClassificação da conexidade:")
                print(grafo.classificar_conexidade_digrafo())
                exibir_grafo_reduzido(grafo)
            elif opcao == "10":
                grafo = criar_grafo_exemplo_sp()
                print("Exemplo pequeno carregado com sucesso.")
            elif opcao == "11":
                grafo.salvar_matriz_txt()
            elif opcao == "0":
                print("Encerrando aplicação...")
                break
            else:
                print("Opção inválida.")
        except FileNotFoundError:
            print("Arquivo não encontrado. Verifique se data/grafo.txt existe.")
        except ValueError:
            print("Entrada inválida. Confira os números informados.")
        except Exception as e:
            print(f"Ocorreu um erro: {e}")


if __name__ == "__main__":
    menu()
