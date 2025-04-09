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

