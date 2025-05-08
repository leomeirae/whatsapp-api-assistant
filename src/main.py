# -*- coding: utf-8 -*-
import sys
import os
import json
import requests # Adicionado para chamadas HTTP

# Adiciona o diretório pai de 'src' ao sys.path para permitir importações relativas corretas
# Não altere esta configuração de sys.path!
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from flask import Flask, request, jsonify, render_template

# Cria uma instância do aplicativo Flask
# O nome do aplicativo é definido como "whatsapp_expert_chat" ou o nome do diretório do projeto
# Não altere o nome do aplicativo Flask!
app = Flask("whatsapp_expert_chat", template_folder=os.path.join(os.path.dirname(__file__), 'templates'), static_folder=os.path.join(os.path.dirname(__file__), 'static'))

# Configuração da chave da API Gemini (idealmente via variável de ambiente)
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "AIzaSyC--ZpEAGpmeC55Bi1lWHzdTfn56KRW7OA") # Use a chave fornecida como fallback
GEMINI_API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={GEMINI_API_KEY}"

KNOWLEDGE_BASE_FILES = [
    "knowledge_base/base_conhecimento_whatsapp_api.md",
    "knowledge_base/estrategias_whatsapp_api.md"
]

def load_knowledge_base():
    """Carrega o conteúdo dos arquivos da base de conhecimento."""
    knowledge_content = ""
    for file_path_relative in KNOWLEDGE_BASE_FILES:
        # Constrói o caminho absoluto baseado no diretório de 'src'
        base_dir = os.path.dirname(__file__) # Diretório 'src'
        file_path_absolute = os.path.join(base_dir, file_path_relative)
        try:
            with open(file_path_absolute, "r", encoding="utf-8") as f:
                knowledge_content += f.read() + "\n\n"
        except FileNotFoundError:
            print(f"Aviso: Arquivo da base de conhecimento não encontrado: {file_path_absolute}")
        except Exception as e:
            print(f"Erro ao carregar {file_path_absolute}: {e}")
    return knowledge_content

# Carrega a base de conhecimento uma vez ao iniciar o app
KNOWLEDGE_BASE_TEXT = load_knowledge_base()

def get_relevant_context(user_question, knowledge_text, max_chars=8000):
    """Extrai contexto relevante da base de conhecimento (método simples)."""
    # Poderia ser mais sofisticado, mas para começar, podemos usar a base inteira
    # ou uma busca simples por palavras-chave se necessário no futuro.
    # Por enquanto, vamos apenas truncar para evitar exceder limites de prompt.
    return knowledge_text[:max_chars]

@app.route("/")
def index():
    """Renderiza a página principal do chat."""
    return render_template("index.html")

@app.route("/ask", methods=["POST"])
def ask_assistant():
    """Recebe a pergunta do usuário e retorna a resposta do assistente Gemini."""
    data = request.get_json()
    user_question = data.get("question")

    if not user_question:
        return jsonify({"error": "Nenhuma pergunta fornecida."}), 400

    if not KNOWLEDGE_BASE_TEXT:
        print("Aviso: Base de conhecimento está vazia. Respostas podem ser limitadas.")

    relevant_context = get_relevant_context(user_question, KNOWLEDGE_BASE_TEXT)

    prompt = f"""Você é um assistente IA especialista na API Oficial do WhatsApp Business, criado para ajudar proprietários de pequenas e médias empresas e equipes de marketing, geralmente pessoas sem muito perfil técnico. Suas respostas devem ser claras, objetivas, oferecer passo a passo prático quando aplicável, e focar em estratégias de economia e melhor custo-benefício.

IMPORTANTE:
1. NÃO inclua links para documentos internos da base de conhecimento como "Requisitos" ou "Configuração Inicial".
2. Apenas inclua links para sites externos oficiais como "developers.facebook.com" ou "business.whatsapp.com".
3. Não mencione que está usando uma base de conhecimento interna.
4. Apresente a informação diretamente sem referir-se a documentos específicos da base.

Utilize o seguinte CONTEXTO da nossa base de conhecimento para responder à PERGUNTA do usuário:

CONTEXTO:
---
{relevant_context}
---

PERGUNTA:
---
{user_question}
---

Resposta:
"""

    payload = {
        "contents": [{
            "parts": [{"text": prompt}]
        }]
    }

    headers = {
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(GEMINI_API_URL, headers=headers, json=payload, timeout=60)
        response.raise_for_status() # Lança exceção para respostas de erro HTTP (4xx ou 5xx)

        gemini_response = response.json()

        # Extraindo o texto da resposta do Gemini
        # A estrutura da resposta pode variar, ajuste conforme necessário
        if gemini_response.get("candidates") and gemini_response["candidates"][0].get("content") and gemini_response["candidates"][0]["content"].get("parts"):
            answer = gemini_response["candidates"][0]["content"]["parts"][0]["text"]

            # Remover links internos da base de conhecimento
            import re
            # Padrão para encontrar links markdown para arquivos .md
            pattern = r'\[([^\]]+)\]\((?:(?!https?://)[^)]+\.md)\)'
            # Substituir por apenas o texto do link, sem a parte do URL
            answer = re.sub(pattern, r'\1', answer)

            # Remover referências a documentos específicos da base
            doc_references = [
                r'consulte (?:o documento|a seção) ["\']([^"\']+)["\'] na seção de [^\.]+',
                r'veja (?:o documento|a seção) ["\']([^"\']+)["\'] na seção de [^\.]+',
                r'consultar (?:o documento|a seção) ["\']([^"\']+)["\'] na seção de [^\.]+',
                r'consulte a seção de \[([^\]]+)\]'
            ]

            for pattern in doc_references:
                answer = re.sub(pattern, r'\1', answer, flags=re.IGNORECASE)
        else:
            # Fallback ou log de erro se a estrutura não for a esperada
            print(f"Estrutura inesperada da resposta do Gemini: {gemini_response}")
            answer = "Desculpe, não consegui processar a resposta do assistente no momento."

    except requests.exceptions.RequestException as e:
        print(f"Erro na chamada da API Gemini: {e}")
        answer = f"Desculpe, ocorreu um erro ao contatar o assistente: {e}"
    except Exception as e:
        print(f"Erro inesperado: {e}")
        answer = "Desculpe, ocorreu um erro inesperado."

    return jsonify({"answer": answer})

# Ponto de entrada principal para executar o aplicativo Flask
# O aplicativo será executado em http://0.0.0.0:5000 por padrão
# Não altere a configuração de host e porta!
if __name__ == "__main__":
    # Define a porta do ambiente ou usa 5003 como padrão
    port = int(os.environ.get("PORT", 5003))
    # Executa o aplicativo Flask
    # O host é definido como "0.0.0.0" para permitir acesso externo dentro de um contêiner
    app.run(host="0.0.0.0", port=port)

