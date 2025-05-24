from functools import lru_cache
import pandas as pd
from typing import Union, List
from investiny import historical_data

def fetch_br_stocks(tickers: Union[str, List[str]]) -> pd.DataFrame:
    """
    Wrapper que normaliza os tickers para uma tupla e chama a função cacheada.
    """
    if isinstance(tickers, str):
        tickers = (tickers,)
    elif isinstance(tickers, list):
        tickers = tuple(tickers)
    return _fetch_br_stocks_cached(tickers)

@lru_cache(maxsize=32)
def _fetch_br_stocks_cached(tickers: tuple) -> pd.DataFrame:
    """
    Função interna que usa cache com tickers como tupla (hashable).
    """
    dfs = []

    for ticker in tickers:
        data = historical_data(ticker)
        df = pd.DataFrame(data.get_daily_historical_data_as_df())
        df["ticker"] = ticker
        dfs.append(df)

    return pd.concat(dfs)