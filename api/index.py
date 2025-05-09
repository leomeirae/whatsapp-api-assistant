import sys
import os
from flask import Flask, request, jsonify, render_template, send_from_directory
from dotenv import load_dotenv

# Configurar variáveis de ambiente a partir de .env se existir
load_dotenv()

# Adicionar o diretório raiz ao path para permitir importações
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Importar a função de processamento de perguntas
from src.main import process_question

# Obter o diretório raiz do projeto
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Criar uma nova instância do Flask para a função serverless
app = Flask(__name__,
            template_folder=os.path.join(ROOT_DIR, 'src', 'templates'),
            static_folder=os.path.join(ROOT_DIR, 'src', 'static'))

@app.route("/", methods=["GET"])
def index():
    """Renderiza a página principal do chat."""
    return render_template("index_new.html")


@app.route("/calculadora", methods=["GET"])
def calculadora():
    """Renderiza a página da calculadora de preços da API do WhatsApp."""
    return render_template("calculadora_new.html")


@app.route("/static/<path:path>")
def serve_static(path):
    """Serve arquivos estáticos."""
    return send_from_directory(app.static_folder, path)


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
        error_msg = f"Erro ao processar sua pergunta: {str(e)}"
        return jsonify({"error": error_msg}), 500
