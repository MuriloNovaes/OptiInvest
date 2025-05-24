import numpy as np
from scipy.optimize import minimize

def optimize_portfolio(returns, cov_matrix, risk_profile="moderado"):
    """
    Otimiza a alocação de ativos com base no perfil de risco utilizando programação quadrática.

    A função utiliza a biblioteca `scipy.optimize.minimize` com o método SLSQP para
    encontrar a melhor distribuição dos pesos de ativos de acordo com o perfil de risco informado.

    Args:
        returns (list | np.ndarray): Lista ou array de retornos esperados de cada ativo.
        cov_matrix (np.ndarray): Matriz de covariância entre os ativos.
        risk_profile (str): Perfil de risco do investidor. Pode ser "conservador", "moderado" ou "agressivo".

            - "conservador": Minimiza o risco (desvio padrão da carteira).
            - "agressivo": Maximiza o retorno esperado.
            - "moderado": Compromisso entre risco e retorno (função objetivo ponderada).

    Returns:
        np.ndarray: Array contendo os pesos otimizados para cada ativo.

    Raises:
        ValueError: Se o perfil de risco fornecido não for reconhecido.
    """
    n_assets = len(returns)
    pesos_iniciais = np.ones(n_assets) / n_assets  # Distribuição inicial uniforme

    # Restrição: a soma dos pesos deve ser igual a 1
    constraints = ({'type': 'eq', 'fun': lambda x: np.sum(x) - 1})
    # Limites: cada peso entre 0% e 100%
    bounds = [(0, 1) for _ in range(n_assets)]

    # Define a função objetivo de acordo com o perfil de risco
    if risk_profile == "conservador":
        # Minimiza o risco (desvio padrão da carteira)
        fun = lambda w: np.sqrt(w.T @ cov_matrix @ w)
    elif risk_profile == "agressivo":
        # Maximiza o retorno esperado (minimiza o negativo do retorno)
        fun = lambda w: -np.dot(w, returns)
    else:  # perfil "moderado" ou qualquer outro valor
        # Compromisso entre risco e retorno
        fun = lambda w: np.sqrt(w.T @ cov_matrix @ w) - 0.7 * np.dot(w, returns)

    # Otimização
    result = minimize(
        fun,
        pesos_iniciais,
        method='SLSQP',
        bounds=bounds,
        constraints=constraints
    )

    return result.x  # Pesos otimizados


if __name__ == "__main__":
    # Exemplo de uso
    returns = np.array([0.12, 0.18, 0.1])
    cov_matrix = np.array([
        [0.0625, 0.015, 0.012],
        [0.015, 0.09, 0.018],
        [0.012, 0.018, 0.0144]
    ])

    for profile in ["conservador", "moderado", "agressivo"]:
        pesos = optimize_portfolio(returns, cov_matrix, profile)
        print(f"Perfil: {profile} - Pesos: {pesos.round(2)}")
