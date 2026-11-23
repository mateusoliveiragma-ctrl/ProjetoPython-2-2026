# Projeto Final - Análise de Vendas de Games

**Disciplina:** Linguagem de Programação em Python (2026.2)  
**Professor:** Ruben Prado  
**Instituição:** Faculdade Senac-DF de Tecnologia e Inovação  
**Turma:** ADS-B

## Objetivo do projeto

Desenvolver um Sistema Analítico Interativo (CLI) em Python para analisar dados reais de vendas de jogos eletrônicos, utilizando Pandas para o processamento, Orientação a Objetos para organizar a lógica e Matplotlib/Seaborn para gerar gráficos.

## Instalação e execução

É necessário ter o Python instalado. No terminal, dentro da pasta do projeto:

```bash
python -m pip install -r requirements.txt
python baixar_base.py
python main.py
```

O arquivo completo `data/vgsales.csv` está incluído no repositório. O script `baixar_base.py` permite obter novamente a base, se necessário. A amostra `data/vgsales_amostra.csv` pode ser utilizada em testes.

Para executar os testes:

```bash
python -m unittest discover -s tests -v
```

---

# Formulário Oficial de Entrega

## Integrantes da equipe

- Mateus Oliveira
- Ronald Alvez
- Airton Dias
- João Gabriel Ribeiro
- Ricardo Fernandes
- Rodrigo Fernades

## Sobre o conjunto de dados

**Tema Geral:** Análise de Vendas de Jogos Eletrônicos.

**Fonte de Dados (URL):** https://www.kaggle.com/datasets/gregorut/videogamesales

**Motivação:** A análise reúne informações sobre vendas de jogos eletrônicos para identificar os gêneros, plataformas e títulos com maior destaque comercial. Os dados também permitem comparar o desempenho entre regiões e observar a evolução das vendas ao longo dos anos.

O dataset `Video Game Sales` contém registros históricos de vendas de jogos, incluindo nome, plataforma, gênero, ano, editora e vendas por região. Os valores de vendas são apresentados em milhões de unidades.

## Arquitetura e organização do sistema

**Módulos / Classes Criadas:** A classe `AnalisadorDeDados`, localizada no arquivo `src/analisador.py`, é responsável por carregar e processar os dados de vendas de jogos eletrônicos utilizando a biblioteca Pandas. Ela organiza as operações de limpeza, filtragem, agrupamento e análise estatística dos dados, além de gerar gráficos com Matplotlib e Seaborn. O arquivo `main.py` contém o menu interativo com `while True` e tratamento de entradas inválidas por `try/except`, permitindo que o usuário escolha as análises diretamente pelo terminal. O arquivo `baixar_base.py` auxilia na obtenção do CSV.

**Limpeza de Dados:** O sistema identifica e remove registros com valores ausentes nos campos necessários para a análise, utilizando o método `dropna()` da biblioteca Pandas. Também realiza conversões de tipos numéricos, trata registros inconsistentes e duplicados e prepara os dados para cálculos, agrupamentos e visualizações. A limpeza ocorre na classe `AnalisadorDeDados`.

## Gráficos desenvolvidos

1. **Visão 1 - Gráfico de barras: vendas por gênero.** Apresenta o total de vendas globais agrupadas por gênero, como Ação, Esportes, RPG e Corrida. Permite identificar quais categorias de jogos tiveram maior sucesso comercial. O eixo horizontal apresenta os gêneros e o eixo vertical mostra as vendas globais em milhões de unidades.

2. **Visão 2 - Histograma: distribuição das vendas globais.** Mostra a frequência dos jogos em diferentes faixas de vendas globais. Ajuda a identificar se a maioria dos títulos apresenta vendas baixas, médias ou elevadas. O eixo horizontal representa as vendas globais e o vertical indica a quantidade de jogos.

3. **Visão 3 - Gráfico de dispersão: vendas na América do Norte e Europa.** Compara as vendas dos jogos nas duas regiões. Cada ponto representa um jogo, permitindo observar possíveis relações entre seu desempenho comercial nesses mercados. O eixo horizontal representa as vendas na América do Norte e o vertical as vendas na Europa, ambos em milhões de unidades.

**Visualizações adicionais:** gráfico de linha das vendas globais por ano de lançamento e gráfico de barras das vendas por região. Todos os gráficos possuem títulos e identificação dos eixos em português.

## Estrutura do projeto

```text
projeto-games/
├── data/
│   ├── .gitkeep
│   ├── vgsales_amostra.csv
│   └── vgsales.csv             # Obtido pelo script ou pelo Kaggle
├── src/
│   ├── __init__.py
│   └── analisador.py
├── tests/
│   └── test_analisador.py
├── baixar_base.py
├── main.py
├── requirements.txt
├── .gitignore
└── README.md
```

## Repositório e entrega

O código foi desenvolvido na branch `dev-equipe-games` e enviado para avaliação por meio do Pull Request #5 no repositório da disciplina: https://github.com/rubaun/ProjetoPython-2-2026/pull/5.

