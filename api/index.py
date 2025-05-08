from src.main import app, process_question
import json
import os

# Vercel usa o WSGI para servir aplicativos Flask
# Este arquivo serve como ponto de entrada para a Vercel

def handler(event, context):
    """
    Handler para funções serverless da Vercel
    """
    path = event.get('path', '/')
    http_method = event.get('httpMethod', 'GET')

    # Roteamento básico
    if path == '/' or path == '':
        # Servir o arquivo HTML diretamente
        try:
            with open('src/templates/index_new.html', 'r') as f:
                html_content = f.read()
            return {
                'statusCode': 200,
                'headers': {'Content-Type': 'text/html'},
                'body': html_content
            }
        except Exception as e:
            return {
                'statusCode': 500,
                'headers': {'Content-Type': 'text/plain'},
                'body': f'Erro ao carregar a página: {str(e)}'
            }
    elif path == '/calculadora':
        # Servir o arquivo HTML diretamente
        try:
            with open('src/templates/calculadora_new.html', 'r') as f:
                html_content = f.read()
            return {
                'statusCode': 200,
                'headers': {'Content-Type': 'text/html'},
                'body': html_content
            }
        except Exception as e:
            return {
                'statusCode': 500,
                'headers': {'Content-Type': 'text/plain'},
                'body': f'Erro ao carregar a página: {str(e)}'
            }
    elif path == '/ask' and http_method == 'POST':
        try:
            # Processar a solicitação de API
            body = json.loads(event.get('body', '{}'))
            question = body.get('question', '')

            if not question:
                return {
                    'statusCode': 400,
                    'headers': {'Content-Type': 'application/json'},
                    'body': json.dumps({'error': 'Nenhuma pergunta fornecida.'})
                }

            # Chamar a função diretamente
            result = process_question(question)

            return {
                'statusCode': 200,
                'headers': {'Content-Type': 'application/json'},
                'body': json.dumps(result)
            }
        except Exception as e:
            return {
                'statusCode': 500,
                'headers': {'Content-Type': 'application/json'},
                'body': json.dumps({'error': f'Erro ao processar a pergunta: {str(e)}'})
            }
    else:
        return {
            'statusCode': 404,
            'headers': {'Content-Type': 'text/plain'},
            'body': 'Página não encontrada'
        }
