import pandas as pd

def preparar_dados(dados):
    """
    Limpa e prepara os dados para a análise:
    - Selecione apenas os preços de fechamento.
    - Remove Linhas com valores ausentes.
    - Calcula os retornos diários.

    Parâmetros:
    - dados (pandas.DataFrame): Dados brutos baixados com o yfinance.
    
    Retorna:
    - pandas.DataFrame: Retornos diários limpos.
    """
    print("🔍 Iniciando o tratamento dos dados...")

    # Extrai os preços de fechamento para todos os tickers
    fechamento = dados.xs('Close', level=1, axis=1)

    # Remove valores ausentes
    fechamento = fechamento.dropna()

    # Calcula os retornos diários
    retornos = fechamento.pct_change().dropna()

    return retornos