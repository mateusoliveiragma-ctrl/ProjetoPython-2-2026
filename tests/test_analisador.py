import os
import tempfile
import unittest

os.environ["MPLBACKEND"] = "Agg"
from src.analisador import AnalisadorDeDados
from pathlib import Path


class TestAnalisador(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.a = AnalisadorDeDados(Path(__file__).resolve().parents[1] / "data" / "vgsales_amostra.csv")

    def test_csv_real(self):
        self.assertEqual(self.a.resumo_geral()["validos"], 50)

    def test_agrupamentos(self):
        self.assertGreater(self.a.vendas_por_genero().sum(), 0)
        self.assertGreater(self.a.vendas_por_plataforma().sum(), 0)

    def test_filtro(self):
        self.assertTrue((self.a.filtrar_genero("Ação")["Gênero"] == "Ação").all())
        with self.assertRaises(ValueError):
            self.a.filtrar_genero("gênero inexistente")

    def test_analises_adicionais(self):
        self.assertGreater(len(self.a.vendas_por_ano()), 0)
        self.assertEqual(len(self.a.vendas_por_regiao()), 4)
        self.assertFalse(self.a.buscar_jogo("Mario").empty)

    def test_top(self):
        self.assertEqual(len(self.a.top_jogos()), 10)

    def test_graficos(self):
        with tempfile.TemporaryDirectory() as pasta:
            for nome, funcao in (
                ("barras.png", self.a.grafico_barras),
                ("histograma.png", self.a.grafico_histograma),
                ("dispersao.png", self.a.grafico_dispersao),
                ("linha.png", self.a.grafico_linha),
                ("regioes.png", self.a.grafico_regioes),
            ):
                caminho = os.path.join(pasta, nome)
                funcao(caminho)
                self.assertTrue(os.path.getsize(caminho) > 0)


if __name__ == "__main__":
    unittest.main()
