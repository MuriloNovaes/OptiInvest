from flask import Flask, request, jsonify
from flask_cors import CORS
from services.data_service import fetch_br_stocks, calculate_returns
from services.analysis_services import optimize_portfolio
import numpy as np

app = Flask(__name__)
CORS(app)

@app.route('/api/optimize', methods=['POST'])
def optimize():
    try:
        # 1. Recebe dados do frontend
        user_data = request.json
        tickers = user_data.get('tickers', ['PETR4.SA', 'VALE3.SA', 'ITUB4.SA'])
        risk_profile = user_data.get('risk_profile', 'moderado')
        capital = float(user_data['capital'])

        # 2. Baixa e processa dados
        prices = fetch_br_stocks(tickers)
        returns = calculate_returns(prices)
        cov_matrix = prices.pct_change().cov() * 252  # Matriz de covariância anualizada

        # 3. Otimiza a carteira
        weights = optimize_portfolio(returns, cov_matrix, risk_profile)

        # 4. Formata resposta
        allocation = {
            ticker: {
                "peso": round(weight * 100, 2),  # Em %
                "valor": round(weight * capital, 2)  # Em R$
            }
            for ticker, weight in zip(tickers, weights)
        }

        return jsonify({
            "success": True,
            "allocation": allocation,
            "expected_return": round(np.dot(weights, returns) * 100, 2),  # Em %
            "risk": round(np.sqrt(np.dot(weights.T, np.dot(cov_matrix, weights))) * 100, 2)  # Em %
        })

    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 400

if __name__ == '__main__':
    app.run(debug=True)