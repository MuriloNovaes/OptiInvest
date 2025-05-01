import numpy as np
from scipy.optimize import minimaze

def optimize_portfolio(returns, cov_matrix, risk_profile="moderado"):
    """
    Otimiza a alocação de carteira baseada no perfil de risco.
    
    Parâmetros:
    - returns: Retornos médios anuais das ações (Series do pandas).
    - cov_matrix: Matriz de covariância anualizada dos retornos (DataFrame).
    - risk_profile: "conservador", "moderado" ou "agressivo".

    Retorna:
    - pesos_otimizados: Array com pesos (%) par acada ação.
    """

    n_assets = len(returns)
    pesos_iniciais = np.ones(n_assets) / n_assets

    # Restrições: soma dos pesos = 100
    constraints = ({'type': 'eq', 'fun': lambda x: np.sum(x) - 1})
    bounds = tuple((0, 1) for _ in range(n_assets))

    # Função objetivo (minimizar risco ou maximizar retorno)
    if risk_profile == "conservador":
        # Minimiza a volatilidade (risco)
        def objetivo(w):
            return np.sqrt(np.dot(w.T, np.dot(cov_matrix, w)))
    elif risk_profile == "agressivo":
        # Maximiza o retorno (observe o sinal negativo na minimização)
        def objetivo(w):
            return -np.dot(w, returns)
    else: # moderado
        # Maximiza o Indice de Sharpe (retorno ajustado pelo risco)
        def objetivo(w):
            retorno = np.dot(w, returns)
            risco = np.sqrt(np.dot(w.t, np.dot(cov_matrix, w)))
            return -retorno / risco # Queremos maximizar o índice de Sharpe
        
    # Otimização
    resultado = minimaze(
        objetivo,
        pesos_iniciais,
        method='SLSQP',
        bounds=bounds,
        constraints=constraints 
    )
    return resultado.x 