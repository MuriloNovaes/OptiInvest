import numpy as np
from scipy.optimize import minimize

def optimize_portfolio(returns, cov_matrix, risk_profile="moderado"):
    """
    Otimiza a alocação de ativos com base no perfil de risco.

    Parâmetros:
        returns (list/np.ndarray): Retornos esperados dos ativos.
        cov_matrix (np.ndarray): Matriz de covariância.
        risk_profile (str): "conservador", "moderado" ou "agressivo".

    Retorna:
        np.ndarray: Pesos otimizados.
    """
    n_assets = len(returns)
    pesos_iniciais = np.ones(n_assets) / n_assets

    constraints = ({'type': 'eq', 'fun': lambda x: np.sum(x) - 1})
    bounds = [(0, 1) for _ in range(n_assets)]

    if risk_profile == "conservador":
        fun = lambda w: np.sqrt(w.T @ cov_matrix @ w)
    elif risk_profile == "agressivo":
        fun = lambda w: -np.dot(w, returns)
    else:  # moderado
        fun = lambda w: np.sqrt(w.T @ cov_matrix @ w) - 0.7 * np.dot(w, returns)

    result = minimize(
        fun,
        pesos_iniciais,
        method='SLSQP',
        bounds=bounds,
        constraints=constraints
    )

    return result.x

if __name__ == "__main__":
    returns = np.array([0.12, 0.18, 0.1])
    cov_matrix = np.array([
        [0.0625, 0.015, 0.012],
        [0.015, 0.09, 0.018],
        [0.012, 0.018, 0.0144]
    ])

    for profile in ["conservador", "moderado", "agressivo"]:
        pesos = optimize_portfolio(returns, cov_matrix, profile)
        print(f"Perfil: {profile} - Pesos: {pesos.round(2)}")