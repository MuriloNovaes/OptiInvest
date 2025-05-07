from typing import List, Union
from functools import lru_cache
import yfinance as yf
import pandas as pd
import logging

# Configuração básica de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@lru_cache(maxsize=32)
def fetch_br_stocks(tickers: Union[str, List[str]]) -> pd.DataFrame:
    """
    Baixa dados históricos de ações brasileiras do Yahoo Finance com cache.

    Args:
        tickers (str ou list[str]): Ticker(s) da(s) ação(ções) (ex: "PETR4.SA" ou ["PETR4.SA", "VALE3.SA"]).
                                   Tickers brasileiros devem terminar com '.SA'.

    Returns:
        pd.DataFrame: DataFrame com os preços ajustados de fechamento (colunas = tickers),
                     indexado por data, sem valores nulos.

    Raises:
        ValueError: Se nenhum ticker válido for fornecido.
        TypeError: Se o tipo de tickers não for string ou lista.
        Exception: Se falhar ao baixar dados do Yahoo Finance.

    Example:
        >>> fetch_br_stocks("PETR4.SA")
                     PETR4.SA
        Date
        2023-01-01     25.50
        2023-01-02     26.10

        >>> fetch_br_stocks(["PETR4.SA", "VALE3.SA"])
                     PETR4.SA  VALE3.SA
        Date
        2023-01-01     25.50     67.80
    """
    # Validação de inputs
    if not tickers:
        raise ValueError("Pelo menos um ticker deve ser fornecido.")
    
    if isinstance(tickers, str):
        tickers = [tickers]
    elif not isinstance(tickers, list):
        raise TypeError("tickers deve ser uma string ou lista de strings.")

    logger.info(f"Iniciando download de dados para {tickers}")

    try:
        data = yf.download(
            tickers,
            period="1y",
            progress=False,
            group_by='ticker'
        )['Adj Close']
        
        if data.empty:
            raise ValueError("Nenhum dado encontrado para os tickers fornecidos.")
            
        logger.info(f"Dados baixados com sucesso para {tickers}")
        return data.dropna()

    except Exception as e:
        logger.error(f"Falha ao baixar dados: {str(e)}")
        raise RuntimeError(f"Erro ao acessar Yahoo Finance: {str(e)}")


def calculate_returns(prices: pd.DataFrame) -> pd.Series:
    """
    Calcula retornos logarítmicos médios anualizados a partir de preços históricos.

    Args:
        prices (pd.DataFrame): DataFrame de preços (output de fetch_br_stocks).
                              Espera-se colunas = tickers, index = datas.

    Returns:
        pd.Series: Retornos médios anualizados (252 dias úteis),
                  com tickers como índice.

    Raises:
        ValueError: Se o DataFrame de preços estiver vazio ou contiver apenas um registro.

    Example:
        >>> prices = fetch_br_stocks(["PETR4.SA"])
        >>> calculate_returns(prices)
        PETR4.SA    0.15  # 15% ao ano
    """
    if prices.empty or len(prices) < 2:
        raise ValueError("O DataFrame de preços deve conter pelo menos 2 registros.")

    try:
        daily_returns = prices.pct_change().dropna()
        annual_returns = daily_returns.mean() * 252
        logger.debug(f"Retornos calculados: {annual_returns.to_dict()}")
        return annual_returns

    except Exception as e:
        logger.error(f"Erro no cálculo de retornos: {str(e)}")
        raise RuntimeError(f"Falha ao calcular retornos: {str(e)}")


if __name__ == "__main__":
    # Teste das funções
    try:
        test_tickers = ["PETR4.SA", "VALE3.SA"]
        print(f"Testando com tickers: {test_tickers}")
        
        prices = fetch_br_stocks(test_tickers)
        print("\nPreços (5 primeiras linhas):")
        print(prices.head())
        
        returns = calculate_returns(prices)
        print("\nRetornos anuais:")
        print(returns)
        
    except Exception as e:
        print(f"\nErro durante teste: {str(e)}")