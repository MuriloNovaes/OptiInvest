import numpy as np
from scipy.optimize import minimize

def optimize_portfolio(returns, cov_matrix, risk_profile="moderado"):
    """
    Versão simplificada da otimização de carteira.
    
    Parâmetros:
        returns (list/np.ndarray): Retornos esperados dos ativos.
        cov_matrix (np.ndarray): Matriz de covariância.
        risk_profile (str): "conservador", "moderado" ou "agressivo".
    
    Retorna:
        np.ndarray: Pesos otimizados (ex: [0.5, 0.5] para 50% em cada ativo).
    """
    n_assets = len(returns)
    pesos_iniciais = np.ones(n_assets) / n_assets  # Começa com pesos iguais
    
    # Restrição básica: soma dos pesos = 100%
    constraints = ({'type': 'eq', 'fun': lambda x: np.sum(x) - 1})
    
    # Limites: cada peso entre 0% e 100%
    bounds = [(0, 1) for _ in range(n_assets)]
    
    # Define o objetivo conforme o perfil
    if risk_profile == "conservador":
        fun = lambda w: np.sqrt(w.T @ cov_matrix @ w)  # Minimiza risco
    elif risk_profile == "agressivo":
        fun = lambda w: -np.dot(w, returns)  # Maximiza retorno
    else:  # moderado
        fun = lambda w: np.sqrt(w.T @ cov_matrix @ w) - 0.5 * np.dot(w, returns)  # Balanceado
    
    # Otimização
    result = minimize(
        fun,
        pesos_iniciais,
        method='SLSQP',
        bounds=bounds,
        constraints=constraints
    )
    
    return result.x


# Exemplo de uso:
if __name__ == "__main__":
    # Dados de exemplo (PETR4 e VALE3)
    returns = np.array([0.12, 0.18])
    cov_matrix = np.array([
        [0.04, 0.02],
        [0.02, 0.09]
    ])
    
    pesos = optimize_portfolio(returns, cov_matrix, "moderado")
    print("Pesos otimizados:", pesos.round(2))
    # Saída esperada: [0.6 0.4] (60% PETR4, 40% VALE3)