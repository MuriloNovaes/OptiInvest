import pandas as pd
import numpy as np
from datetime import datetime

# Dados estáticos dos ativos (PETR4.SA, ITUB4.SA, VALE3.SA, etc.)
STATIC_ASSETS = {
    "Petrobras": {
        "prices": np.linspace(30, 40, 252),  # Preços diários (252 dias úteis)
        "annual_return": 0.12,               # Retorno anual esperado (12%)
        "volatility": 0.25                    # Volatilidade anual (25%)
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
    Retorna um DataFrame com preços históricos fictícios no formato do yfinance.
    """
    dates = pd.date_range(end=datetime.today(), periods=252, freq='B')  # 252 dias úteis
    
    # Filtra apenas os tickers solicitados
    data = {}
    for ticker in tickers:
        if ticker in STATIC_ASSETS:
            data[ticker] = STATIC_ASSETS[ticker]["prices"]
        else:
            raise ValueError(f"Ticker {ticker} não cadastrado.")
    
    return pd.DataFrame(data, index=dates)

def get_annual_returns(tickers):
    """
    Retorna os retornos anuais pré-definidos (array numpy).
    """
    return np.array([STATIC_ASSETS[ticker]["annual_return"] for ticker in tickers])

def get_covariance_matrix(tickers):
    """
    Gera uma matriz de covariância fictícia baseada na volatilidade dos ativos.
    """
    n_assets = len(tickers)
    cov_matrix = np.zeros((n_assets, n_assets))
    
    for i, ticker_i in enumerate(tickers):
        for j, ticker_j in enumerate(tickers):
            if i == j:
                cov_matrix[i][j] = STATIC_ASSETS[ticker_i]["volatility"] ** 2  # Variância (volatilidade²)
            else:
                # Correlação fictícia (ex: 0.3 entre PETR4 e VALE3)
                cov_matrix[i][j] = 0.3 * STATIC_ASSETS[ticker_i]["volatility"] * STATIC_ASSETS[ticker_j]["volatility"]
    
    return cov_matrix