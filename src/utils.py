import pandas as pd

def ver_resumo(df):
    """
    Exibe as 5 primeiras e 5 últimas linhas de um DataFrame.
    Útil para verificar rapidamente o conteúdo dos dados.
    
    Parâmetros:
    - df (pandas.DataFrame): O DataFrame a ser visualizado.
    
    Retorno:
    - None (apenas exibe no console)
    """
    print("📊 Resumo do DataFrame (5 primeiras e 5 últimas):")
    print(pd.concat([df.head(), df.tail()]))


def analise_risco_retorno(retornos):
    """
    Mostra o retorno medio e volatilidade de cada ação;

    Parâmetros:
    - retornos (pandas.DataFrame): DataFrame com os retornos diários das ações.

    Retorna:
    - DataFrame com métricas de cada ação. 
    """
    analise = pd.DataFrame({
        'Retorno Médio (%)': retornos.mean() * 100,
        'Volatilidade (%)': retornos.std() * 100 # Riscp (desvio padrão) 
    })
    return analise.sort_values(by='Retorno Médio (%)', ascending=False)