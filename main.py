from src.fetch_data import obter_precos
from src.utils import ver_resumo
from src.data_processing import preparar_dados
from src.utils import analise_risco_retorno
import pandas as pd

# Passo 1: Baixar os dados
dados = obter_precos(['PETR4.SA', 'ITUB4.SA'])

# Passo 2: Tratar os dados
retornos = preparar_dados(dados)

# Passo 3: Visualizar os dados tratados
ver_resumo(retornos)
# Após ver_resumo(retornos), adicione:
print("\n📊 Métricas  de Risco-Retorno: ")
print(analise_risco_retorno(retornos))
