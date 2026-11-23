"""Menu interativo para análise de vendas de games."""
from pathlib import Path
from src.analisador import AnalisadorDeDados
from baixar_base import baixar_base


def main():
    try:
        try:
            caminho_csv = baixar_base()
        except (OSError, ValueError) as erro_download:
            print(f"Falha ao baixar a base completa: {erro_download}")
            print("Usando AMOSTRA de 50 registros. Para a base completa, salve vgsales.csv em data/.")
            caminho_csv = Path(__file__).resolve().parent / "data" / "vgsales_amostra.csv"
        analise = AnalisadorDeDados(caminho_csv)
        print(f"Base carregada: {analise.total_original} registros.")
    except (FileNotFoundError, OSError, ValueError) as erro:
        print(f"Erro ao carregar CSV: {erro}")
        return

    while True:
        print("\n" + "=" * 48)
        print("          PAINEL DE ANÁLISE DE JOGOS")
        print("=" * 48)
        print("1 - Estatísticas gerais")
        print("2 - Vendas por gênero")
        print("3 - Vendas por plataforma")
        print("4 - Filtrar jogos por gênero")
        print("5 - Top 10 jogos mais vendidos")
        print("6 - Gráfico de barras por gênero")
        print("7 - Histograma de vendas")
        print("8 - Gráfico de dispersão por ano")
        print("9 - Vendas por ano")
        print("10 - Vendas por região")
        print("11 - Buscar jogo pelo nome")
        print("12 - Gráfico de linha: vendas por ano")
        print("13 - Gráfico de barras: vendas por região")
        print("0 - Sair")
        try:
            opcao = int(input("Escolha uma opção: ").strip())
        except ValueError:
            print("Entrada inválida! Digite um número.")
            continue
        except (EOFError, KeyboardInterrupt):
            print("\nPrograma encerrado.")
            break

        try:
            if opcao == 0:
                print("Até logo!")
                break
            elif opcao == 1:
                resumo = analise.resumo_geral()
                print(f"Registros originais: {resumo['originais']}")
                print(f"Registros válidos: {resumo['validos']}")
                print(f"Registros removidos: {resumo['removidos']}")
                print(f"Vendas totais: {resumo['vendas_totais']:.2f} milhões")
                print(f"Média por registro: {resumo['vendas_medias']:.2f} milhões")
                print("\nQuantidade de jogos por gênero:\n" + resumo["por_genero"].to_string())
            elif opcao == 2:
                print("Vendas por gênero (em milhões):\n" + analise.vendas_por_genero().to_string())
            elif opcao == 3:
                print("Vendas por console (em milhões):\n" + analise.vendas_por_plataforma().to_string())
            elif opcao == 4:
                genero = input("Digite o gênero em português (ex.: Ação, Corrida, RPG): ")
                print(analise.filtrar_genero(genero).head(20).to_string(index=False))
            elif opcao == 5:
                print(analise.top_jogos().to_string(index=False))
            elif opcao == 6:
                analise.grafico_barras()
            elif opcao == 7:
                analise.grafico_histograma()
            elif opcao == 8:
                analise.grafico_dispersao()
            elif opcao == 9:
                print(analise.vendas_por_ano().to_string())
            elif opcao == 10:
                print(analise.vendas_por_regiao().to_string())
            elif opcao == 11:
                termo = input("Nome do jogo: ")
                resultados = analise.buscar_jogo(termo)
                print(resultados.to_string(index=False) if not resultados.empty else "Nenhum jogo encontrado.")
            elif opcao == 12:
                analise.grafico_linha()
            elif opcao == 13:
                analise.grafico_regioes()
            else:
                print("Opção inexistente.")
        except ValueError as erro:
            print(f"Aviso: {erro}")
        except (OSError, RuntimeError) as erro:
            print(f"Erro na operação: {erro}")
        except (EOFError, KeyboardInterrupt):
            print("\nPrograma encerrado.")
            break


if __name__ == "__main__":
    main()
