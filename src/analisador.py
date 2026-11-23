"""Análise orientada a objetos de vendas de videogames."""
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


class AnalisadorDeDados:
    """Carrega, limpa, agrupa, filtra e visualiza vendas de jogos."""

    TRADUCOES_GENEROS = {
        "Action": "Ação", "Adventure": "Aventura", "Fighting": "Luta",
        "Misc": "Diversos", "Platform": "Plataforma", "Puzzle": "Quebra-cabeça",
        "Racing": "Corrida", "Role-Playing": "RPG", "Shooter": "Tiro",
        "Simulation": "Simulação", "Sports": "Esportes", "Strategy": "Estratégia",
    }
    COLUNAS = ("Year", "Genre", "Platform", "Name", "Global_Sales", "NA_Sales", "EU_Sales", "JP_Sales", "Other_Sales")

    def __init__(self, caminho_csv=None):
        caminho = Path(caminho_csv) if caminho_csv else (
            Path(__file__).resolve().parents[1] / "data" / "vgsales.csv"
        )
        self.df = pd.read_csv(caminho)
        faltantes = set(self.COLUNAS) - set(self.df.columns)
        if faltantes:
            raise ValueError(f"Colunas ausentes: {', '.join(sorted(faltantes))}")
        self.total_original = len(self.df)
        for coluna in ("Year", "Global_Sales", "NA_Sales", "EU_Sales", "JP_Sales", "Other_Sales"):
            self.df[coluna] = pd.to_numeric(self.df[coluna], errors="coerce")
        for coluna in ("Genre", "Platform", "Name"):
            self.df[coluna] = self.df[coluna].astype("string").str.strip().replace("", pd.NA)
        self.df = self.df.dropna(subset=list(self.COLUNAS))
        self.df = self.df.loc[(self.df["Global_Sales"] >= 0) &
                             self.df["Year"].between(1970, 2030)]
        self.df = self.df.drop_duplicates().reset_index(drop=True)
        if self.df.empty:
            raise ValueError("Não há registros válidos após a limpeza.")
        self.df["Genero_PT"] = self.df["Genre"].map(self.TRADUCOES_GENEROS).fillna(self.df["Genre"])
        sns.set_theme(style="whitegrid")

    def resumo_geral(self):
        return {
            "originais": self.total_original,
            "validos": len(self.df),
            "removidos": self.total_original - len(self.df),
            "vendas_totais": self.df["Global_Sales"].sum(),
            "vendas_medias": self.df["Global_Sales"].mean(),
            "por_genero": self.df.groupby("Genero_PT").size().sort_values(ascending=False),
        }

    def vendas_por_genero(self):
        return self.df.groupby("Genero_PT")["Global_Sales"].sum().sort_values(ascending=False)

    def vendas_por_plataforma(self):
        return self.df.groupby("Platform")["Global_Sales"].sum().sort_values(ascending=False)

    def generos(self):
        return sorted(self.df["Genero_PT"].unique().tolist())

    def filtrar_genero(self, genero):
        filtrados = self.df.loc[
            ((self.df["Genero_PT"].str.casefold() == genero.strip().casefold()) |
             (self.df["Genre"].str.casefold() == genero.strip().casefold()))
        ]
        if filtrados.empty:
            raise ValueError("Gênero não encontrado. Disponíveis: " + ", ".join(self.generos()))
        return self._tabela_em_portugues(filtrados)

    def top_jogos(self, quantidade=10):
        return self._tabela_em_portugues(self.df.nlargest(quantidade, "Global_Sales"))

    @staticmethod
    def _tabela_em_portugues(dados):
        return dados[["Name", "Platform", "Year", "Genero_PT", "Global_Sales"]].rename(
            columns={"Name": "Jogo", "Platform": "Console", "Year": "Ano",
                     "Genero_PT": "Gênero", "Global_Sales": "Vendas (milhões)"}
        ).copy()

    @staticmethod
    def _finalizar(arquivo=None):
        plt.tight_layout()
        if arquivo:
            destino = Path(arquivo)
            destino.parent.mkdir(parents=True, exist_ok=True)
            plt.savefig(destino, dpi=150, bbox_inches="tight")
            plt.close()
            return destino
        plt.show()
        plt.close()

    def grafico_barras(self, arquivo=None):
        dados = self.vendas_por_genero().head(10).reset_index()
        plt.figure(figsize=(10, 5))
        sns.barplot(data=dados, x="Global_Sales", y="Genero_PT", color="#4472c4")
        plt.title("Vendas mundiais por gênero de jogo")
        plt.xlabel("Vendas globais (milhões de unidades)")
        plt.ylabel("Gênero")
        return self._finalizar(arquivo)

    def grafico_histograma(self, arquivo=None):
        dados = self.df.loc[self.df["Global_Sales"] >= 0, "Global_Sales"]
        plt.figure(figsize=(9, 5))
        sns.histplot(dados, bins=12, color="#16a085")
        plt.title("Distribuição das vendas mundiais")
        plt.xlabel("Vendas globais por jogo (milhões de unidades)")
        plt.ylabel("Quantidade de registros")
        return self._finalizar(arquivo)

    def grafico_dispersao(self, arquivo=None):
        """Compara as vendas de cada jogo na América do Norte e na Europa."""
        dados = self.df.loc[
            self.df["NA_Sales"].notna() & self.df["EU_Sales"].notna()
            & (self.df["NA_Sales"] >= 0) & (self.df["EU_Sales"] >= 0)
        ]
        plt.figure(figsize=(10, 5))
        sns.scatterplot(data=dados, x="NA_Sales", y="EU_Sales", alpha=0.55, s=35)
        plt.title("Comparação das vendas: América do Norte e Europa")
        plt.xlabel("Vendas na América do Norte (milhões de unidades)")
        plt.ylabel("Vendas na Europa (milhões de unidades)")
        return self._finalizar(arquivo)

    def vendas_por_ano(self):
        return self.df.groupby(self.df["Year"].astype(int))["Global_Sales"].sum().sort_index()

    def vendas_por_regiao(self):
        colunas = {"NA_Sales": "América do Norte", "EU_Sales": "Europa",
                   "JP_Sales": "Japão", "Other_Sales": "Outras regiões"}
        return self.df[list(colunas)].sum().rename(index=colunas).sort_values(ascending=False)

    def buscar_jogo(self, termo):
        termo = termo.strip()
        if not termo:
            raise ValueError("Digite o nome ou parte do nome de um jogo.")
        dados = self.df.loc[self.df["Name"].str.contains(termo, case=False, regex=False, na=False)]
        return self._tabela_em_portugues(dados.nlargest(20, "Global_Sales"))

    def grafico_linha(self, arquivo=None):
        dados = self.vendas_por_ano()
        plt.figure(figsize=(10, 5))
        sns.lineplot(x=dados.index, y=dados.values, marker="o", color="#4472c4")
        plt.title("Evolução das vendas mundiais por ano de lançamento")
        plt.xlabel("Ano de lançamento")
        plt.ylabel("Vendas globais (milhões de unidades)")
        return self._finalizar(arquivo)

    def grafico_regioes(self, arquivo=None):
        dados = self.vendas_por_regiao()
        plt.figure(figsize=(9, 5))
        sns.barplot(x=dados.index, y=dados.values, color="#16a085")
        plt.title("Vendas por região")
        plt.xlabel("Região")
        plt.ylabel("Vendas (milhões de unidades)")
        return self._finalizar(arquivo)
