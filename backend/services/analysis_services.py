import numpy as np
from scipy.optimize import minimize
from typing import Literal, Tuple

def optimize_portfolio(
    returns: np.ndarray,
    cov_matrix: np.ndarray,
    risk_profile: Literal["conservador", "moderado", "agressivo"] = "moderado"
) -> np.ndarray:
    """
    Otimiza a alocação de carteira usando o modelo de média-variância de Markowitz.

    Args:
        returns (np.ndarray): Vetor de retornos esperados dos ativos (anualizados).
        cov_matrix (np.ndarray): Matriz de covariância dos retornos dos ativos.
        risk_profile (str): Perfil de risco do investidor. Valores possíveis:
            - "conservador": Minimiza a volatilidade
            - "moderado": Maximiza o Índice de Sharpe (padrão)
            - "agressivo": Maximiza o retorno esperado

    Returns:
        np.ndarray: Vetor de pesos otimizados para cada ativo (entre 0 e 1).

    Raises:
        ValueError: Se os inputs tiverem formatos incompatíveis.

    Example:
        >>> returns = np.array([0.12, 0.18])
        >>> cov_matrix = np.array([[0.04, 0.02], [0.02, 0.09]])
        >>> optimize_portfolio(returns, cov_matrix, "moderado")
        array([0.6, 0.4])
    """
    # Validação dos inputs
    if len(returns) != cov_matrix.shape[0]:
        raise ValueError("Número de ativos em returns e cov_matrix não coincide")
    
    if not np.allclose(cov_matrix, cov_matrix.T):
        raise ValueError("Matriz de covariância deve ser simétrica")

    n_assets = len(returns)
    initial_weights = np.ones(n_assets) / n_assets  # Distribuição uniforme inicial

    # Restrições: soma dos pesos = 1 (100%) e cada peso entre 0 e 1
    constraints = ({'type': 'eq', 'fun': lambda x: np.sum(x) - 1})
    bounds = tuple((0.0, 1.0) for _ in range(n_assets))

    # Definição da função objetivo baseada no perfil de risco
    if risk_profile == "conservador":
        def objective(w: np.ndarray) -> float:
            """Minimiza a volatilidade da carteira (risco)."""
            return np.sqrt(w.T @ cov_matrix @ w)  # Notação matricial mais limpa
            
    elif risk_profile == "agressivo":
        def objective(w: np.ndarray) -> float:
            """Maximiza o retorno esperado (sinal negativo para minimização)."""
            return -w @ returns  # Equivalente a -np.dot(w, returns)
            
    else:  # moderado
        def objective(w: np.ndarray) -> float:
            """Maximiza o Índice de Sharpe (retorno/risco)."""
            portfolio_return = w @ returns
            portfolio_volatility = np.sqrt(w.T @ cov_matrix @ w)
            return -portfolio_return / portfolio_volatility if portfolio_volatility > 0 else -np.inf

    # Otimização usando SLSQP
    result = minimize(
        fun=objective,
        x0=initial_weights,
        method='SLSQP',
        bounds=bounds,
        constraints=constraints,
        options={'disp': False}
    )

    if not result.success:
        raise RuntimeError(f"Falha na otimização: {result.message}")

    return result.x


def calculate_portfolio_metrics(
    weights: np.ndarray,
    returns: np.ndarray,
    cov_matrix: np.ndarray
) -> Tuple[float, float, float]:
    """
    Calcula métricas importantes da carteira otimizada.

    Args:
        weights: Pesos dos ativos
        returns: Retornos esperados
        cov_matrix: Matriz de covariância

    Returns:
        Tuple[float, float, float]: (retorno esperado, volatilidade, Sharpe ratio)
    """
    portfolio_return = weights @ returns
    portfolio_volatility = np.sqrt(weights.T @ cov_matrix @ weights)
    sharpe_ratio = portfolio_return / portfolio_volatility if portfolio_volatility > 0 else 0.0
    
    return portfolio_return, portfolio_volatility, sharpe_ratio