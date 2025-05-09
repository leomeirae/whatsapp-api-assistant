import os
import re
from openai import OpenAI
from dotenv import load_dotenv
from src.simple_search import load_knowledge_base, get_relevant_context

# Carregar variáveis de ambiente
load_dotenv()

# Configuração da chave da API OpenAI (via variável de ambiente)
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "")
OPENAI_MODEL = os.environ.get("OPENAI_MODEL", "gpt-4o-mini")  # Modelo a ser utilizado

# Definir o caminho da base de conhecimento
KNOWLEDGE_BASE_DIR = os.path.join(os.path.dirname(__file__), 'knowledge_base')

# Carregar e processar a base de conhecimento
KNOWLEDGE_BASE_CHUNKS = load_knowledge_base(KNOWLEDGE_BASE_DIR)

def process_question(user_question):
    """Processa a pergunta do usuário e retorna a resposta do assistente."""
    if not KNOWLEDGE_BASE_CHUNKS:
        print("Aviso: Base de conhecimento está vazia. Respostas podem ser limitadas.")

    relevant_context = get_relevant_context(user_question, KNOWLEDGE_BASE_CHUNKS)

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
