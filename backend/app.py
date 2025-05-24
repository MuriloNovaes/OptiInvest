from flask import Flask, request, jsonify
from flask_cors import CORS
from services.static_data import get_static_prices, get_annual_returns, get_covariance_matrix
from services.analysis_services import optimize_portfolio

# Instância principal do app Flask
app = Flask(__name__)
CORS(app)  # Habilita CORS para permitir requisições do frontend local

@app.route('/api/optimize', methods=['POST'])
def optimize():
    """
    Rota de otimização de portfólio.

    Espera um JSON com o capital disponível e o perfil de risco, 
    e retorna a alocação ideal entre os ativos fixos definidos.

    Requisição JSON esperada:
    {
        "capital": 10000,
        "risk_profile": "moderado"  # ou "conservador", "agressivo"
    }

    Resposta JSON:
    {
        "success": True,
        "allocation": [...],
        "expected_return": 12.45,
        "valor_total_investido": 9998.76,
        "risk": 8.32,
        "capital": 10000,
        "melhores_acoes": [...]
    }

    Returns:
        JSON: Resultado da otimização ou erro com status 400/500.
    """
    data = request.get_json()
    capital = data.get("capital")
    risk_profile = data.get("risk_profile", "moderado")

    # Lista fixa de ativos disponíveis
    tickers = ("Petrobras", "Itaú", "B3")

    # Validação básica
    if not tickers or not capital:
        return jsonify({"success": False, "error": "Dados incompletos"}), 400

    try:
        # Dados de retorno e risco dos ativos
        returns = get_annual_returns(tickers)
        cov_matrix = get_covariance_matrix(tickers)

        # Otimização de alocação
        pesos = optimize_portfolio(returns, cov_matrix, risk_profile)

        allocation = []
        total_invested = 0

        # Construção da resposta com peso, valor e percentual por ativo
        for i, ticker in enumerate(tickers):
            peso_pct = round(pesos[i] * 100, 2)
            valor = round(pesos[i] * capital, 2)
            total_invested += valor
            allocation.append({
                "ticker": ticker,
                "peso_percentual": peso_pct,
                "valor_investido": valor
            })

        # Cálculo de retorno esperado e risco (desvio padrão)
        expected_return = round(float(pesos @ returns) * 100, 2)
        risk = round(float((pesos @ cov_matrix @ pesos.T)**0.5) * 100, 2)

        melhores_acoes = [a["ticker"] for a in allocation if a["peso_percentual"] > 0]

        return jsonify({
            "success": True,
            "allocation": allocation,
            "expected_return": expected_return,
            "valor_total_investido": round(total_invested, 2),
            "risk": risk,
            "capital": capital,
            "melhores_acoes": melhores_acoes
        })

    except Exception as e:
        # Erro genérico tratado com status 500
        return jsonify({"success": False, "error": str(e)}), 500

# Execução local da aplicação (apenas para desenvolvimento)
if __name__ == "__main__":
    app.run(debug=True)
