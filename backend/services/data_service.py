import yfinance as yf
import pandas as pd

def fetch_br_stocks(tickers):
    """Baixa dados de ações brasileiras usando yfinance, (.SA)."""
    data = yf.download(tickers, period="1y")['Adj Close']
    return data.dropna()

def calculate_returns(data):
    """Calcula os retornos diários e medios"""
    returns = data.pct_change()
    annual_returns = returns.mean() * 252
    return annual_returns

print("Data service loaded")
