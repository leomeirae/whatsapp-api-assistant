import os
import re
from flask import Flask, request, jsonify
from openai import OpenAI
from dotenv import load_dotenv

# Criar uma instância do aplicativo Flask
app = Flask(__name__)

# Carregar variáveis de ambiente
load_dotenv()

# Configuração da chave da API OpenAI (via variável de ambiente)
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "")
OPENAI_MODEL = os.environ.get("OPENAI_MODEL", "gpt-4o-mini")


def process_question(user_question):
    """Processa a pergunta do usuário e retorna a resposta do assistente."""
    # Inicializar o cliente OpenAI
    client = OpenAI(api_key=OPENAI_API_KEY)

    # Criar o sistema de prompt e o prompt do usuário
    system_prompt = """Você é um assistente IA especialista técnico na API Oficial do WhatsApp Business, criado para fornecer informações precisas e detalhadas sobre a implementação e uso da API do WhatsApp. Você deve priorizar respostas técnicas e específicas, com exemplos de código quando relevante.

IMPORTANTE:
1. Você é um ESPECIALISTA TÉCNICO na API do WhatsApp Business. Suas respostas devem ser detalhadas, precisas e focadas em aspectos técnicos da API.
2. Quando o usuário fizer perguntas sobre a API, forneça detalhes técnicos específicos, incluindo endpoints, parâmetros, formatos de resposta e exemplos de código.
3. Diferencie claramente entre o aplicativo WhatsApp Business (para pequenas empresas) e a API do WhatsApp Business (para integração programática).
4. Quando o usuário perguntar sobre implementação, forneça exemplos de código em Python ou JavaScript.
5. Apenas inclua links para sites externos oficiais como "developers.facebook.com" ou "business.whatsapp.com".
"""

    try:
        # Fazer a chamada para a API OpenAI
        response = client.chat.completions.create(
            model=OPENAI_MODEL,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_question}
            ],
            temperature=0.7,
            max_tokens=1000
        )

        # Extrair a resposta
        answer = response.choices[0].message.content

        # Pós-processamento para remover qualquer link interno que possa ter passado
        patterns = [
            r'\[([^\]]+)\]\((?:(?!https?://)[^)]+\.md)\)',  # Links markdown para arquivos .md
            r'\[([^\]]+)\]\((?:\d+_[^)]+/[^)]+\.md)\)',     # Links com padrão específico da base
        ]

        for pattern in patterns:
            answer = re.sub(pattern, r'\1', answer, flags=re.IGNORECASE)

        return {"answer": answer}

    except Exception as e:
        print(f"Erro ao chamar a API OpenAI: {e}")
        return {"error": f"Desculpe, ocorreu um erro ao processar sua pergunta: {e}"}


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


@app.route("/api/test", methods=["GET"])
def test():
    """Rota de teste para API."""
    return jsonify({
        "status": "success",
        "message": "API está funcionando!"
    })


@app.route("/", methods=["GET"])
def index():
    """Página inicial."""
    return jsonify({
        "name": "WhatsApp API Assistant",
        "version": "1.0.0",
        "description": "Assistente especializado na API do WhatsApp Business"
    })
