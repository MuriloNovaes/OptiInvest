from src.fetch_data import obter_precos
from src.utils import ver_resumo

dados = obter_precos(['PETR4.SA', 'ITUB4.SA'])
ver_resumo(dados)

