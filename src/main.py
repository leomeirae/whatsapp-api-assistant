# -*- coding: utf-8 -*-
import sys
import os
import json
import requests # Adicionado para chamadas HTTP
from openai import OpenAI # Adicionado para usar a API OpenAI

# Carregar variáveis de ambiente do arquivo .env
from dotenv import load_dotenv
load_dotenv()  # Carrega as variáveis do arquivo .env

# Adiciona o diretório pai de 'src' ao sys.path para permitir importações relativas corretas
# Não altere esta configuração de sys.path!
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from flask import Flask, request, jsonify, render_template

# Cria uma instância do aplicativo Flask
# O nome do aplicativo é definido como "whatsapp_expert_chat" ou o nome do diretório do projeto
# Não altere o nome do aplicativo Flask!
app = Flask("whatsapp_expert_chat", template_folder=os.path.join(os.path.dirname(__file__), 'templates'), static_folder=os.path.join(os.path.dirname(__file__), 'static'))

# Configuração da chave da API OpenAI (via variável de ambiente)
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "")
OPENAI_MODEL = os.environ.get("OPENAI_MODEL", "gpt-4o-mini") # Modelo a ser utilizado

# Diretório raiz do projeto
ROOT_DIR = os.path.dirname(os.path.dirname(__file__))

KNOWLEDGE_BASE_FILES = [
    os.path.join(ROOT_DIR, "knowledge_base/base_conhecimento_whatsapp_api.md"),
    os.path.join(ROOT_DIR, "knowledge_base/estrategias_whatsapp_api.md"),
    os.path.join(ROOT_DIR, "knowledge_base/05_verificacao_empresas/verificacao_empresas_meta.md"),
    os.path.join(ROOT_DIR, "knowledge_base/05_verificacao_empresas/verificacao_whatsapp_business.md"),
    os.path.join(ROOT_DIR, "knowledge_base/05_verificacao_empresas/guia_passo_a_passo_verificacao.md")
]

def load_knowledge_base():
    """Carrega o conteúdo dos arquivos da base de conhecimento."""
    knowledge_content = ""
    for file_path in KNOWLEDGE_BASE_FILES:
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                knowledge_content += f.read() + "\n\n"
        except FileNotFoundError:
            print(f"Aviso: Arquivo da base de conhecimento não encontrado: {file_path}")
        except Exception as e:
            print(f"Erro ao carregar {file_path}: {e}")
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
    return render_template("index_new.html")

@app.route("/calculadora")
def calculadora():
    """Renderiza a página da calculadora de preços da API do WhatsApp."""
    return render_template("calculadora_new.html")

def process_question(user_question):
    """Processa a pergunta do usuário e retorna a resposta do assistente."""
    if not KNOWLEDGE_BASE_TEXT:
        print("Aviso: Base de conhecimento está vazia. Respostas podem ser limitadas.")

    relevant_context = get_relevant_context(user_question, KNOWLEDGE_BASE_TEXT)

    # Inicializar o cliente OpenAI
    # Removendo qualquer configuração de proxy que possa estar causando problemas
    client = OpenAI(api_key=OPENAI_API_KEY)

    # Criar o sistema de prompt e o prompt do usuário
    system_prompt = """Você é um assistente IA especialista na API Oficial do WhatsApp Business, criado para ajudar proprietários de pequenas e médias empresas e equipes de marketing, geralmente pessoas sem muito perfil técnico. Suas respostas devem ser claras, objetivas, oferecer passo a passo prático quando aplicável, e focar em estratégias de economia e melhor custo-benefício.

IMPORTANTE:
1. NÃO inclua links para documentos internos da base de conhecimento como "Requisitos" ou "Configuração Inicial".
2. Apenas inclua links para sites externos oficiais como "developers.facebook.com" ou "business.whatsapp.com".
3. Não mencione que está usando uma base de conhecimento interna.
4. Apresente a informação diretamente sem referir-se a documentos específicos da base.
5. NUNCA use formatação como [texto](caminho/arquivo.md) ou [texto](01_introducao/tipos_de_api.md).
6. Se precisar mencionar um documento, apenas mencione o nome sem criar um link.
"""

    user_prompt = f"""Utilize o seguinte CONTEXTO para responder à PERGUNTA do usuário:

CONTEXTO:
---
{relevant_context}
---

PERGUNTA:
---
{user_question}
---
"""

    try:
        # Fazer a chamada para a API OpenAI
        response = client.chat.completions.create(
            model=OPENAI_MODEL,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.7,
            max_tokens=1000
        )

        # Extrair a resposta
        answer = response.choices[0].message.content

        # Pós-processamento para remover qualquer link interno que possa ter passado
        import re

        # Padrões para encontrar e remover links internos
        patterns = [
            r'\[([^\]]+)\]\((?:(?!https?://)[^)]+\.md)\)',  # Links markdown para arquivos .md
            r'\[([^\]]+)\]\((?:\d+_[^)]+/[^)]+\.md)\)',     # Links com padrão específico da base
            r'consulte (?:o documento|a seção) ["\']([^"\']+)["\'] na seção de [^\.]+',
            r'veja (?:o documento|a seção) ["\']([^"\']+)["\'] na seção de [^\.]+',
            r'consultar (?:o documento|a seção) ["\']([^"\']+)["\'] na seção de [^\.]+',
            r'consulte a seção de \[([^\]]+)\]',
            r'Para mais detalhes sobre .+, consulte o documento \[([^\]]+)\]',
            r'Veja mais em \[([^\]]+)\]'
        ]

        for pattern in patterns:
            answer = re.sub(pattern, r'\1', answer, flags=re.IGNORECASE)

        return {"answer": answer}

    except Exception as e:
        print(f"Erro ao chamar a API OpenAI: {e}")
        return {"error": f"Desculpe, ocorreu um erro ao processar sua pergunta: {e}"}


@app.route("/ask", methods=["POST"])
def ask_assistant():
    """Recebe a pergunta do usuário e retorna a resposta do assistente."""
    data = request.get_json()
    user_question = data.get("question")

    if not user_question:
        return jsonify({"error": "Nenhuma pergunta fornecida."}), 400

    result = process_question(user_question)
    return jsonify(result)

# Ponto de entrada principal para executar o aplicativo Flask
# O aplicativo será executado em http://0.0.0.0:5000 por padrão
# Não altere a configuração de host e porta!
if __name__ == "__main__":
    # Define a porta do ambiente ou usa 5003 como padrão
    port = int(os.environ.get("PORT", 5003))
    # Executa o aplicativo Flask
    # O host é definido como "0.0.0.0" para permitir acesso externo dentro de um contêiner
    app.run(host="0.0.0.0", port=port)

