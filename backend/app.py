from flask import Flask, request, jsonify
from flask_cors import CORS
from services.data_service import fetch_br_stocks, calculate_returns
from services.analysis_services import optimize_portfolio
import numpy as np
import pandas as pd
import yfinance as yf


# Configuração básica do Flask
app = Flask(__name__)
CORS(app)  # Permite requisições do frontend


def fetch_br_stocks(tickers):
    # Garante que é uma lista de strings
    if isinstance(tickers, str):
        tickers = [tickers]
    if isinstance(tickers, list) and len(tickers) == 1 and isinstance(tickers[0], list):
        tickers = tickers[0]

    print("🎯 Tickers processados:", tickers)

    # Faz o download com yfinance
    data = yf.download(tickers, period="1y", interval="1d", auto_adjust=False, group_by='ticker')

    # Verifica se é 1 ou mais tickers e extrai corretamente os preços de fechamento ajustado
    if len(tickers) == 1:
        df = data['Adj Close'].to_frame()
        df.columns = [tickers[0]]
        return df.dropna()
    else:
        return data['Adj Close'].dropna()
def calculate_returns(prices):
    daily_returns = prices.pct_change().dropna()
    mean_returns = daily_returns.mean() * 252  # Retorno médio anualizado
    return mean_returns.values  # <- retorna como array, não Series

@app.route('/api/optimize', methods=['POST','GET'])
def optimize():
    """
    Rota principal que recebe os dados do frontend e retorna a alocação otimizada.

    Espera um JSON no formato:
    {
        "capital": 10000,
        "risk_profile": "moderado",
        "tickers": ["PETR4.SA", "VALE3.SA"]  # Opcional
    }

    Retorna:
    {
        "success": bool,
        "allocation": {
            "PETR4.SA": {"peso": 60.5, "valor": 6050.0},
            ...
        },
        "expected_return": 12.5,  # Em %
        "risk": 10.2  # Em %
    }
    """
    try:
        
        # Se for GET, retorna dados de exemplo sem processar
        if request.method == 'GET':
            return jsonify({
                "success": True,
                "allocation": {
                    "PETR4.SA": {"peso": 45.5, "valor": 4550.0},
                    "VALE3.SA": {"peso": 32.5, "valor": 3210.0}
                },
                "expected_return": 12.5,
                "risk": 10.2,
                "message": "Dados de exemplo(use POST para otimização real)"
            })
        
        # 1.(POST) Valida e extrai dados da requisição
        user_data = request.json
        
        if not user_data or 'capital' not in user_data:
            return jsonify({"success": False, "error": "Dados incompletos"}), 400

        capital = float(user_data['capital'])
        if capital <= 0:
            return jsonify({"success": False, "error": "Capital deve ser positivo"}), 400

        tickers = user_data.get('tickers', ['PETR4.SA', 'VALE3.SA', 'ITUB4.SA'])
                # Corrige caso venha string única
        if isinstance(tickers, str):
            tickers = [tickers]
        # Corrige se vier como lista dentro de lista
        if isinstance(tickers, list) and len(tickers) == 1 and isinstance(tickers[0], list):
            tickers = tickers[0]
        risk_profile = user_data.get('risk_profile', 'moderado')

        # 2. Busca e processa dados
        prices = fetch_br_stocks(tickers)
        returns = calculate_returns(prices)
        cov_matrix = prices.pct_change().cov() * 252  # Anualizada
        
        

        # 3. Otimização
        
        weights = optimize_portfolio(returns, cov_matrix, risk_profile)

        # 4. Formata resposta
        allocation = {
            ticker: {
                "peso": round(weight * 100, 2),
                "valor": round(weight * capital, 2)
            }
            for ticker, weight in zip(tickers, weights)
        }

        # Cálculos adicionais
        expected_return = round(np.dot(weights, returns) * 100, 2)
        risk = round(np.sqrt(weights.T @ cov_matrix @ weights) * 100, 2)

        return jsonify({
            "success": True,
            "allocation": allocation,
            "expected_return": expected_return,
            "risk": risk
        })

    except Exception as e:
        print(e)
        return jsonify({
            "success": False,
            "error": f"Erro interno: {str(e)}"
        }), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
