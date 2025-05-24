from flask import Flask, request, jsonify
from flask_cors import CORS
from services.static_data import get_static_prices, get_annual_returns, get_covariance_matrix
from services.analysis_services import optimize_portfolio

app = Flask(__name__)
CORS(app)  # Permite o frontend local se conectar

@app.route('/api/optimize', methods=['POST'])
def optimize():
    data = request.get_json()
    capital = data.get("capital")
    risk_profile = data.get("risk_profile", "moderado")
    tickers = ("Petrobras", "Itaú", "B3") # tickers fixos
    if not tickers or not capital:
        return jsonify({"success": False, "error": "Dados incompletos"}), 400

    try:
        returns = get_annual_returns(tickers)
        cov_matrix = get_covariance_matrix(tickers)
        pesos = optimize_portfolio(returns, cov_matrix, risk_profile)

        allocation = []
        total_invested = 0


        for i, ticker in enumerate(tickers):
            peso_pct = round(pesos[i] * 100, 2)
            valor = round(pesos[i] * capital, 2)
            total_invested += valor
            allocation.append({
                "ticker": ticker,
                "peso_percentual": peso_pct,
                "valor_investido": valor
            })

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
        return jsonify({"success": False, "error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)