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

from flask import Flask, request, jsonify, render_template, redirect, url_for, flash, session, get_flashed_messages
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash

# Importar configurações e classes para autenticação e histórico
from src.config import SECRET_KEY
from src.database import User, ChatHistory, supabase
from src.forms import LoginForm, RegisterForm

# Cria uma instância do aplicativo Flask
# O nome do aplicativo é definido como "whatsapp_expert_chat" ou o nome do diretório do projeto
# Não altere o nome do aplicativo Flask!
app = Flask("whatsapp_expert_chat", template_folder=os.path.join(os.path.dirname(__file__), 'templates'), static_folder=os.path.join(os.path.dirname(__file__), 'static'))
app.config['SECRET_KEY'] = SECRET_KEY

# Configurar o gerenciador de login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.get_by_id(user_id)

# Configuração da chave da API OpenAI (via variável de ambiente)
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "")
OPENAI_MODEL = os.environ.get("OPENAI_MODEL", "gpt-4o-mini") # Modelo a ser utilizado

# Diretório raiz do projeto
ROOT_DIR = os.path.dirname(os.path.dirname(__file__))

# Importar bibliotecas necessárias para RAG
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import re

# Definir o caminho da base de conhecimento
KNOWLEDGE_BASE_DIR = os.path.join(os.path.dirname(__file__), 'knowledge_base')

# Função para encontrar todos os arquivos markdown na base de conhecimento
def find_markdown_files(directory):
    """Encontra todos os arquivos markdown em um diretório e seus subdiretórios."""
    markdown_files = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.md'):
                markdown_files.append(os.path.join(root, file))
    return markdown_files

# Obter lista de todos os arquivos markdown
KNOWLEDGE_BASE_FILES = find_markdown_files(KNOWLEDGE_BASE_DIR)

# Estrutura para armazenar chunks de documentos
class DocumentChunk:
    def __init__(self, content, source, title=None):
        self.content = content
        self.source = source
        self.title = title or os.path.basename(source)

    def __str__(self):
        return f"{self.title} - {self.content[:50]}..."

# Função para dividir documentos em chunks
def split_document(content, source, chunk_size=1000, overlap=200):
    """Divide um documento em chunks menores com sobreposição."""
    chunks = []

    # Extrair título do documento (primeira linha com #)
    title_match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
    title = title_match.group(1) if title_match else os.path.basename(source)

    # Dividir por parágrafos ou seções
    paragraphs = re.split(r'\n\s*\n', content)

    current_chunk = ""
    for paragraph in paragraphs:
        # Se adicionar este parágrafo exceder o tamanho do chunk, salve o chunk atual e comece um novo
        if len(current_chunk) + len(paragraph) > chunk_size and current_chunk:
            chunks.append(DocumentChunk(current_chunk, source, title))
            # Manter alguma sobreposição para contexto
            current_chunk = current_chunk[-overlap:] if overlap > 0 else ""

        current_chunk += paragraph + "\n\n"

    # Adicionar o último chunk se não estiver vazio
    if current_chunk.strip():
        chunks.append(DocumentChunk(current_chunk, source, title))

    return chunks

def load_knowledge_base():
    """Carrega e processa a base de conhecimento em chunks."""
    all_chunks = []

    for file_path in KNOWLEDGE_BASE_FILES:
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
                # Dividir o documento em chunks
                document_chunks = split_document(content, file_path)
                all_chunks.extend(document_chunks)
                print(f"Carregado: {file_path} - {len(document_chunks)} chunks")
        except Exception as e:
            print(f"Erro ao carregar {file_path}: {e}")

    return all_chunks

# Carregar e processar a base de conhecimento
KNOWLEDGE_BASE_CHUNKS = load_knowledge_base()

# Criar vetorizador TF-IDF para busca semântica
vectorizer = TfidfVectorizer(lowercase=True, stop_words='english')
chunk_contents = [chunk.content for chunk in KNOWLEDGE_BASE_CHUNKS]
tfidf_matrix = vectorizer.fit_transform(chunk_contents)

def get_relevant_context(user_question, knowledge_chunks=KNOWLEDGE_BASE_CHUNKS, top_k=5, max_chars=8000):
    """Extrai contexto relevante da base de conhecimento usando similaridade TF-IDF."""
    if not knowledge_chunks:
        return "Base de conhecimento não disponível."

    # Vetorizar a pergunta do usuário
    question_vector = vectorizer.transform([user_question])

    # Calcular similaridade com todos os chunks
    similarities = cosine_similarity(question_vector, tfidf_matrix).flatten()

    # Obter os índices dos top_k chunks mais relevantes
    top_indices = similarities.argsort()[-top_k:][::-1]

    # Construir o contexto com os chunks mais relevantes
    relevant_context = ""
    sources_used = set()

    for idx in top_indices:
        chunk = KNOWLEDGE_BASE_CHUNKS[idx]
        similarity_score = similarities[idx]

        # Apenas incluir chunks com alguma relevância
        if similarity_score > 0.1:  # Limiar de similaridade
            relevant_context += f"\n\n--- Trecho de {chunk.title} ---\n"
            relevant_context += chunk.content
            sources_used.add(chunk.source)

    # Se não encontrou nada relevante, use os primeiros chunks
    if not relevant_context:
        print("Nenhum conteúdo relevante encontrado, usando chunks padrão.")
        for i in range(min(3, len(KNOWLEDGE_BASE_CHUNKS))):
            chunk = KNOWLEDGE_BASE_CHUNKS[i]
            relevant_context += f"\n\n--- Trecho de {chunk.title} ---\n"
            relevant_context += chunk.content

    # Limitar o tamanho do contexto para não exceder limites de tokens
    if len(relevant_context) > max_chars:
        relevant_context = relevant_context[:max_chars]

    print(f"Fontes utilizadas: {', '.join([os.path.basename(src) for src in sources_used])}")
    return relevant_context

@app.route("/login", methods=["GET", "POST"])
def login():
    """Página de login."""
    form = LoginForm()
    if form.validate_on_submit():
        try:
            # Verificar credenciais com Supabase
            response = supabase.table('users').select('*').eq('email', form.email.data).execute()

            if response.data and len(response.data) > 0:
                user_data = response.data[0]
                # Verificar senha
                if check_password_hash(user_data['password_hash'], form.password.data):
                    user = User(
                        id=user_data['id'],
                        email=user_data['email'],
                        is_authenticated=True
                    )
                    login_user(user)
                    flash('Login realizado com sucesso!', 'success')
                    return redirect(url_for('index'))
                else:
                    flash('Senha incorreta.', 'error')
            else:
                flash('Email não encontrado.', 'error')
        except Exception as e:
            flash(f'Erro ao fazer login: {e}', 'error')

    return render_template("login.html", form=form, messages=get_flashed_messages(with_categories=True))

@app.route("/register", methods=["GET", "POST"])
def register():
    """Página de registro."""
    form = RegisterForm()
    if form.validate_on_submit():
        try:
            # Verificar se o email já existe
            response = supabase.table('users').select('*').eq('email', form.email.data).execute()

            if response.data and len(response.data) > 0:
                flash('Este email já está em uso.', 'error')
            else:
                # Criar hash da senha
                password_hash = generate_password_hash(form.password.data)

                # Inserir novo usuário
                user_data = {
                    'email': form.email.data,
                    'password_hash': password_hash,
                    'created_at': 'now()'
                }

                response = supabase.table('users').insert(user_data).execute()

                if response.data:
                    flash('Registro realizado com sucesso! Faça login para continuar.', 'success')
                    return redirect(url_for('login'))
                else:
                    flash('Erro ao registrar usuário.', 'error')
        except Exception as e:
            flash(f'Erro ao registrar: {e}', 'error')

    return render_template("register.html", form=form, messages=get_flashed_messages(with_categories=True))

@app.route("/logout")
@login_required
def logout():
    """Rota para logout."""
    logout_user()
    flash('Logout realizado com sucesso!', 'success')
    return redirect(url_for('login'))

@app.route("/")
@login_required
def index():
    """Renderiza a página principal do chat."""
    return render_template("index_new.html")

@app.route("/calculadora")
@login_required
def calculadora():
    """Renderiza a página da calculadora de preços da API do WhatsApp."""
    return render_template("calculadora_new.html")

def process_question(user_question):
    """Processa a pergunta do usuário e retorna a resposta do assistente."""
    if not KNOWLEDGE_BASE_CHUNKS:
        print("Aviso: Base de conhecimento está vazia. Respostas podem ser limitadas.")

    relevant_context = get_relevant_context(user_question)

    # Inicializar o cliente OpenAI
    # Removendo qualquer configuração de proxy que possa estar causando problemas
    client = OpenAI(api_key=OPENAI_API_KEY)

    # Criar o sistema de prompt e o prompt do usuário
    system_prompt = """Você é um assistente IA especialista técnico na API Oficial do WhatsApp Business, criado para fornecer informações precisas e detalhadas sobre a implementação e uso da API do WhatsApp. Você deve priorizar respostas técnicas e específicas, com exemplos de código quando relevante.

IMPORTANTE:
1. Você é um ESPECIALISTA TÉCNICO na API do WhatsApp Business. Suas respostas devem ser detalhadas, precisas e focadas em aspectos técnicos da API.
2. Quando o usuário fizer perguntas sobre a API, forneça detalhes técnicos específicos, incluindo endpoints, parâmetros, formatos de resposta e exemplos de código.
3. Diferencie claramente entre o aplicativo WhatsApp Business (para pequenas empresas) e a API do WhatsApp Business (para integração programática).
4. Quando o usuário perguntar sobre implementação, forneça exemplos de código em Python ou JavaScript.
5. Apenas inclua links para sites externos oficiais como "developers.facebook.com" ou "business.whatsapp.com".
6. Não mencione que está usando uma base de conhecimento interna.
7. Apresente a informação diretamente sem referir-se a documentos específicos da base.
8. NUNCA use formatação como [texto](caminho/arquivo.md) ou [texto](01_introducao/tipos_de_api.md).
9. Quando o usuário perguntar sobre como usar o WhatsApp Business (não a API), esclareça a diferença e explique que você é especialista na API, mas pode fornecer informações básicas sobre o aplicativo.
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
@login_required
def ask_assistant():
    """Recebe a pergunta do usuário e retorna a resposta do assistente."""
    data = request.get_json()
    user_question = data.get("question")

    if not user_question:
        return jsonify({"error": "Nenhuma pergunta fornecida."}), 400

    # Processar a pergunta
    result = process_question(user_question)

    # Salvar a pergunta e a resposta no histórico se o usuário estiver autenticado
    if current_user.is_authenticated:
        try:
            # Salvar a pergunta do usuário usando Supabase
            ChatHistory.save_message(
                user_id=current_user.id,
                role="user",
                content=user_question
            )

            # Salvar a resposta do assistente
            if "answer" in result:
                ChatHistory.save_message(
                    user_id=current_user.id,
                    role="assistant",
                    content=result["answer"]
                )
        except Exception as e:
            print(f"Erro ao salvar histórico: {e}")
            import traceback
            traceback.print_exc()

    return jsonify(result)

@app.route("/history")
@login_required
def view_history():
    """Exibe o histórico de conversas do usuário."""
    try:
        # Obter histórico do usuário usando Supabase
        history = ChatHistory.get_user_history(current_user.id)

        # Formatar o histórico para exibição
        formatted_history = []

        if history:
            for msg in history:
                # Verificar se as chaves existem no dicionário
                role = msg.get("role", "unknown")
                content = msg.get("content", "")
                timestamp = msg.get("created_at", "")

                formatted_history.append({
                    "role": role,
                    "content": content,
                    "timestamp": timestamp
                })

        print(f"Histórico formatado: {formatted_history}")

        return render_template(
            "history.html",
            history=formatted_history
        )
    except Exception as e:
        import traceback
        traceback.print_exc()
        flash(f"Erro ao carregar histórico: {e}", "error")
        return redirect(url_for("index"))

# Ponto de entrada principal para executar o aplicativo Flask
# O aplicativo será executado em http://0.0.0.0:5000 por padrão
# Não altere a configuração de host e porta!
if __name__ == "__main__":
    # Define a porta do ambiente ou usa 5003 como padrão
    port = int(os.environ.get("PORT", 5003))
    # Executa o aplicativo Flask
    # O host é definido como "0.0.0.0" para permitir acesso externo dentro de um contêiner
    app.run(host="0.0.0.0", port=port)

