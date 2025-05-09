import sys
import os
import json
from flask import Flask, request, jsonify
from dotenv import load_dotenv

# Configurar variáveis de ambiente a partir de .env se existir
load_dotenv()

# Adicionar o diretório raiz ao path para permitir importações
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Importar a função de processamento de perguntas
from src.main import process_question

# Criar uma nova instância do Flask para a função serverless
app = Flask(__name__)

@app.route("/", methods=["GET"])
def home():
    return "API do WhatsApp Business Assistant está funcionando! Use o endpoint /ask para fazer perguntas."

@app.route("/ask", methods=["POST"])
def ask():
    try:
        # Obter dados da requisição
        data = request.get_json()

        if not data:
            return jsonify({"error": "Nenhum dado JSON fornecido"}), 400

        user_question = data.get("question")

        if not user_question:
            return jsonify({"error": "Nenhuma pergunta fornecida"}), 400

        # Processar a pergunta usando a função importada
        result = process_question(user_question)

        # Retornar o resultado
        return jsonify(result)

    except Exception as e:
        print(f"Erro ao processar pergunta: {str(e)}")
        return jsonify({"error": f"Erro ao processar sua pergunta: {str(e)}"}), 500
