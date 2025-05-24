from functools import lru_cache
import pandas as pd
from typing import Union, List
from investiny import historical_data

def fetch_br_stocks(tickers: Union[str, List[str]]) -> pd.DataFrame:
    """
    Busca dados históricos diários de ações brasileiras, normalizando a entrada de tickers.

    Esta função é um wrapper que aceita uma string (um único ticker) ou uma lista de strings,
    normaliza para uma tupla (necessária para o uso com lru_cache) e chama a função cacheada.

    Args:
        tickers (Union[str, List[str]]): Um ticker ou uma lista de tickers de ações brasileiras.

    Returns:
        pd.DataFrame: Um DataFrame contendo os dados históricos diários com a coluna 'ticker' associada.
    """
    if isinstance(tickers, str):
        tickers = (tickers,)  # Converte string única para tupla
    elif isinstance(tickers, list):
        tickers = tuple(tickers)  # Converte lista para tupla
    return _fetch_br_stocks_cached(tickers)


@lru_cache(maxsize=32)
def _fetch_br_stocks_cached(tickers: tuple) -> pd.DataFrame:
    """
    Função interna cacheada que obtém dados históricos de ações brasileiras.

    Essa função utiliza o decorador lru_cache para evitar múltiplas chamadas à API para os mesmos tickers,
    otimizando o desempenho.

    Args:
        tickers (tuple): Uma tupla com tickers válidos para consulta.

    Returns:
        pd.DataFrame: Um DataFrame com os dados históricos de preços das ações, com uma coluna extra 'ticker'.
    """
    dfs = []

    for ticker in tickers:
        data = historical_data(ticker)  # Busca dados via investiny
        df = pd.DataFrame(data.get_daily_historical_data_as_df())
        df["ticker"] = ticker  # Adiciona a coluna de identificação do ticker
        dfs.append(df)

    return pd.concat(dfs)  # Concatena todos os DataFrames
