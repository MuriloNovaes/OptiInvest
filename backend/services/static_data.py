import pandas as pd
import numpy as np
from datetime import datetime

# Dados estáticos simulados para três ativos fictícios.
# Os preços são gerados com uma distribuição linear simples para simulação.
STATIC_ASSETS = {
    "Petrobras": {
        "prices": np.linspace(30, 40, 252),  # Preços simulados para 252 dias úteis
        "annual_return": 0.12,               # Retorno anual estimado (12%)
        "volatility": 0.25                   # Volatilidade anual estimada (25%)
    },
    "Itaú": {
        "prices": np.linspace(25, 30, 252),
        "annual_return": 0.08,
        "volatility": 0.15
    },
    "B3": {
        "prices": np.linspace(60, 75, 252),
        "annual_return": 0.18,
        "volatility": 0.30
    }
}

def get_static_prices(tickers):
    """
    Retorna um DataFrame com os preços históricos fictícios dos ativos fornecidos.

    Os preços são simulados com base em dados estáticos definidos no dicionário STATIC_ASSETS.

    Args:
        tickers (list[str]): Lista de nomes dos ativos (ex: ["Petrobras", "Itaú"]).

    Returns:
        pd.DataFrame: DataFrame com datas como índice e os preços dos ativos como colunas.

    Raises:
        ValueError: Se algum ticker informado não estiver cadastrado.
    """
    dates = pd.date_range(end=datetime.today(), periods=252, freq='B')  # 252 dias úteis

    data = {}
    for ticker in tickers:
        if ticker in STATIC_ASSETS:
            data[ticker] = STATIC_ASSETS[ticker]["prices"]
        else:
            raise ValueError(f"Ticker {ticker} não cadastrado.")

    return pd.DataFrame(data, index=dates)

def get_annual_returns(tickers):
    """
    Retorna os retornos anuais esperados para os ativos fornecidos.

    Args:
        tickers (list[str]): Lista de nomes dos ativos.

    Returns:
        np.ndarray: Array com os retornos anuais dos ativos em ordem.
    """
    return np.array([STATIC_ASSETS[ticker]["annual_return"] for ticker in tickers])

def get_covariance_matrix(tickers):
    """
    Calcula uma matriz de covariância fictícia com base nas volatilidades dos ativos.

    A covariância entre diferentes ativos é simulada assumindo uma correlação constante de 0.3.

    Args:
        tickers (list[str]): Lista de nomes dos ativos.

    Returns:
        np.ndarray: Matriz de covariância (n x n) entre os ativos.
    """
    n_assets = len(tickers)
    cov_matrix = np.zeros((n_assets, n_assets))

    for i, ticker_i in enumerate(tickers):
        for j, ticker_j in enumerate(tickers):
            if i == j:
                # Diagonal principal: variância (volatilidade²)
                cov_matrix[i][j] = STATIC_ASSETS[ticker_i]["volatility"] ** 2
            else:
                # Correlação fictícia: 0.3 * vol_i * vol_j
                cov_matrix[i][j] = 0.3 * STATIC_ASSETS[ticker_i]["volatility"] * STATIC_ASSETS[ticker_j]["volatility"]

    return cov_matrix
