"""Baixa a base original completa, preservando o CSV do Kaggle."""
from pathlib import Path
from urllib.request import Request, urlopen

URL = "https://raw.githubusercontent.com/Elliot-Taylor/VideoGameSalesPredictions/master/vgsales.csv"
DESTINO = Path(__file__).resolve().parent / "data" / "vgsales.csv"


def baixar_base():
    if DESTINO.is_file() and DESTINO.stat().st_size > 1_000_000:
        return DESTINO
    print("Baixando a base completa de videogames (16.598 registros)...")
    req = Request(URL, headers={"User-Agent": "Mozilla/5.0"})
    with urlopen(req, timeout=45) as resposta:
        conteudo = resposta.read()
    if len(conteudo) < 1_000_000 or not conteudo.startswith(b"Rank,Name,Platform,Year,Genre,"):
        raise ValueError("O arquivo baixado não corresponde ao CSV esperado.")
    DESTINO.parent.mkdir(parents=True, exist_ok=True)
    DESTINO.write_bytes(conteudo)
    print(f"Base salva em {DESTINO} ({len(conteudo):,} bytes).")
    return DESTINO


if __name__ == "__main__":
    try:
        baixar_base()
    except (OSError, ValueError) as erro:
        print(f"Não foi possível baixar a base: {erro}")
        print("Baixe vgsales.csv pelo Kaggle e salve na pasta data/.")
