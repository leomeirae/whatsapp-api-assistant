import sys
import os
from flask import Flask, request, jsonify

# Adiciona o diretório raiz ao sys.path para permitir importações corretas
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

# Importar a função de processamento de perguntas
from src.vercel_main import process_question

# Criar uma instância do aplicativo Flask
app = Flask(__name__)

# Rota principal para processar perguntas
@app.route("/api/ask", methods=["POST"])
def ask():
    """Processa a pergunta do usuário e retorna a resposta."""
    try:
        data = request.get_json()
        if not data or "question" not in data:
            return jsonify({"error": "Pergunta não fornecida"}), 400

        user_question = data["question"]
        result = process_question(user_question)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Rota de teste para verificar se a API está funcionando
@app.route("/api/test", methods=["GET"])
def test():
    """Rota de teste para API."""
    return jsonify({
        "status": "success",
        "message": "API está funcionando!"
    })

# Rota raiz para informações básicas
@app.route("/", methods=["GET"])
def index():
    """Página inicial."""
    return jsonify({
        "name": "WhatsApp API Assistant",
        "version": "1.0.0",
        "description": "Assistente especializado na API do WhatsApp Business"
    })
