import yfinance as yf
import pandas as pd

def obter_precos(tickers, inicio='2023-01-01', fim='2024-01-01'):
    """
    Obtém dados históricos de preços das ações fornecidas.

    Parâmetros:
    - tickers (list): Lista de símbolos das ações (ex: ['PETR4.SA', 'ITUB4.SA'])
    - inicio (str): Data de início no formato 'YYYY-MM-DD'
    - fim (str): Data de fim no formato 'YYYY-MM-DD'

    Retorna:
    - pandas.DataFrame: Tabela com dados de preços ajustados e outros campos
      (Abertura, Alta, Baixa, Fechamento, Fechamento Ajustado, Volume)
    """

    print(f"📥 Baixando dados de: {tickers} de {inicio} até {fim}")
    
    # Baixa os dados com todas as colunas disponíveis (Open, High, Low, Close, Adj Close, Volume)
    dados = yf.download(tickers, start=inicio, end=fim, group_by='ticker')

    # Verifica se os dados foram baixados corretamente
    if dados.empty:
        print("⚠️ Nenhum dado retornado. Verifique os tickers ou as datas.")
        return None

    return dados
