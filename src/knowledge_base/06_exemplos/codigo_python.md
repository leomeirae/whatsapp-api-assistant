# Exemplos de Código em Python para a API do WhatsApp Business

Este guia apresenta exemplos práticos de código em Python para implementar as principais funcionalidades da API do WhatsApp Business, desde a configuração básica até recursos avançados.

## Configuração Inicial

### Instalação de Dependências

```bash
pip install requests python-dotenv flask
```

### Configuração de Variáveis de Ambiente

Crie um arquivo `.env`:

```
WHATSAPP_TOKEN=seu_token_de_acesso
WHATSAPP_PHONE_NUMBER_ID=seu_phone_number_id
VERIFY_TOKEN=seu_token_de_verificacao_webhook
```

### Estrutura Básica do Projeto

```
whatsapp_api_project/
├── .env
├── app.py
├── whatsapp_client.py
├── webhook_handler.py
└── templates/
    └── message_templates.py
```

## Cliente Básico da API

Arquivo `whatsapp_client.py`:

```python
import os
import requests
import json
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()

class WhatsAppClient:
    def __init__(self):
        self.token = os.getenv("WHATSAPP_TOKEN")
        self.phone_number_id = os.getenv("WHATSAPP_PHONE_NUMBER_ID")
        self.api_version = "v17.0"
        self.base_url = f"https://graph.facebook.com/{self.api_version}/{self.phone_number_id}"
        self.headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }
    
    def send_message(self, data):
        """
        Envia uma mensagem usando a API do WhatsApp
        """
        url = f"{self.base_url}/messages"
        response = requests.post(url, headers=self.headers, data=json.dumps(data))
        
        if response.status_code == 200:
            return response.json()
        else:
            error = response.json().get("error", {})
            print(f"Erro ao enviar mensagem: {error.get('message')} (Código: {error.get('code')})")
            raise Exception(f"Erro na API: {response.text}")
    
    def get_media_url(self, media_id):
        """
        Obtém a URL de um arquivo de mídia
        """
        url = f"https://graph.facebook.com/{self.api_version}/{media_id}"
        response = requests.get(url, headers=self.headers)
        
        if response.status_code == 200:
            return response.json()
        else:
            error = response.json().get("error", {})
            print(f"Erro ao obter URL da mídia: {error.get('message')} (Código: {error.get('code')})")
            raise Exception(f"Erro na API: {response.text}")
    
    def download_media(self, media_id, output_path):
        """
        Baixa um arquivo de mídia
        """
        # Obter a URL da mídia
        media_info = self.get_media_url(media_id)
        media_url = media_info.get("url")
        
        # Baixar o arquivo
        response = requests.get(media_url, headers=self.headers)
        
        if response.status_code == 200:
            with open(output_path, "wb") as f:
                f.write(response.content)
            return output_path
        else:
            print(f"Erro ao baixar mídia: {response.text}")
            raise Exception(f"Erro ao baixar mídia: {response.text}")
    
    def upload_media(self, file_path, mime_type):
        """
        Faz upload de um arquivo de mídia
        """
        url = f"{self.base_url}/media"
        
        with open(file_path, "rb") as f:
            files = {
                "file": (os.path.basename(file_path), f, mime_type)
            }
            data = {
                "messaging_product": "whatsapp"
            }
            
            headers = {
                "Authorization": f"Bearer {self.token}"
            }
            
            response = requests.post(url, headers=headers, data=data, files=files)
            
            if response.status_code == 200:
                return response.json()
            else:
                error = response.json().get("error", {})
                print(f"Erro ao fazer upload de mídia: {error.get('message')} (Código: {error.get('code')})")
                raise Exception(f"Erro na API: {response.text}")
```

## Envio de Diferentes Tipos de Mensagens

Exemplos de como enviar diferentes tipos de mensagens:

```python
from whatsapp_client import WhatsAppClient

client = WhatsAppClient()

def send_text_message(to, message):
    """
    Envia uma mensagem de texto simples
    """
    data = {
        "messaging_product": "whatsapp",
        "recipient_type": "individual",
        "to": to,
        "type": "text",
        "text": {
            "preview_url": True,
            "body": message
        }
    }
    
    return client.send_message(data)

def send_image_message(to, image_url=None, image_id=None, caption=None):
    """
    Envia uma mensagem com imagem
    """
    data = {
        "messaging_product": "whatsapp",
        "recipient_type": "individual",
        "to": to,
        "type": "image",
        "image": {}
    }
    
    if image_url:
        data["image"]["link"] = image_url
    elif image_id:
        data["image"]["id"] = image_id
    else:
        raise ValueError("É necessário fornecer image_url ou image_id")
    
    if caption:
        data["image"]["caption"] = caption
    
    return client.send_message(data)

def send_document_message(to, document_url=None, document_id=None, caption=None, filename=None):
    """
    Envia uma mensagem com documento
    """
    data = {
        "messaging_product": "whatsapp",
        "recipient_type": "individual",
        "to": to,
        "type": "document",
        "document": {}
    }
    
    if document_url:
        data["document"]["link"] = document_url
    elif document_id:
        data["document"]["id"] = document_id
    else:
        raise ValueError("É necessário fornecer document_url ou document_id")
    
    if caption:
        data["document"]["caption"] = caption
    
    if filename:
        data["document"]["filename"] = filename
    
    return client.send_message(data)

def send_template_message(to, template_name, language_code, components=None):
    """
    Envia uma mensagem de template
    """
    data = {
        "messaging_product": "whatsapp",
        "recipient_type": "individual",
        "to": to,
        "type": "template",
        "template": {
            "name": template_name,
            "language": {
                "code": language_code
            }
        }
    }
    
    if components:
        data["template"]["components"] = components
    
    return client.send_message(data)

def send_interactive_buttons(to, body_text, buttons):
    """
    Envia uma mensagem interativa com botões
    """
    data = {
        "messaging_product": "whatsapp",
        "recipient_type": "individual",
        "to": to,
        "type": "interactive",
        "interactive": {
            "type": "button",
            "body": {
                "text": body_text
            },
            "action": {
                "buttons": buttons
            }
        }
    }
    
    return client.send_message(data)

def send_interactive_list(to, body_text, button_text, sections):
    """
    Envia uma mensagem interativa com lista
    """
    data = {
        "messaging_product": "whatsapp",
        "recipient_type": "individual",
        "to": to,
        "type": "interactive",
        "interactive": {
            "type": "list",
            "body": {
                "text": body_text
            },
            "action": {
                "button": button_text,
                "sections": sections
            }
        }
    }
    
    return client.send_message(data)

# Exemplos de uso

# Enviar mensagem de texto
send_text_message("5511999999999", "Olá! Esta é uma mensagem de teste.")

# Enviar imagem
send_image_message(
    "5511999999999", 
    image_url="https://exemplo.com.br/imagem.jpg", 
    caption="Imagem de exemplo"
)

# Enviar documento
send_document_message(
    "5511999999999",
    document_url="https://exemplo.com.br/documento.pdf",
    caption="Documento importante",
    filename="relatorio.pdf"
)

# Enviar template
components = [
    {
        "type": "body",
        "parameters": [
            {
                "type": "text",
                "text": "João Silva"
            },
            {
                "type": "text",
                "text": "123456"
            }
        ]
    }
]
send_template_message("5511999999999", "confirmacao_pedido", "pt_BR", components)

# Enviar botões interativos
buttons = [
    {
        "type": "reply",
        "reply": {
            "id": "sim-pedido",
            "title": "Sim"
        }
    },
    {
        "type": "reply",
        "reply": {
            "id": "nao-pedido",
            "title": "Não"
        }
    }
]
send_interactive_buttons("5511999999999", "Deseja confirmar seu pedido?", buttons)

# Enviar lista interativa
sections = [
    {
        "title": "Categorias",
        "rows": [
            {
                "id": "cat-produtos",
                "title": "Produtos",
                "description": "Ver todos os produtos"
            },
            {
                "id": "cat-servicos",
                "title": "Serviços",
                "description": "Ver todos os serviços"
            }
        ]
    }
]
send_interactive_list("5511999999999", "Escolha uma opção:", "Ver opções", sections)
```

## Configuração de Webhook com Flask

Arquivo `webhook_handler.py`:

```python
from flask import Flask, request, jsonify
import os
import json
from dotenv import load_dotenv
from whatsapp_client import WhatsAppClient

# Carregar variáveis de ambiente
load_dotenv()

app = Flask(__name__)
client = WhatsAppClient()

@app.route('/webhook', methods=['GET'])
def verify_webhook():
    """
    Endpoint para verificação do webhook
    """
    # Verificação do webhook
    mode = request.args.get('hub.mode')
    token = request.args.get('hub.verify_token')
    challenge = request.args.get('hub.challenge')
    
    verify_token = os.getenv("VERIFY_TOKEN")
    
    # Verificar se o token corresponde ao token de verificação
    if mode == 'subscribe' and token == verify_token:
        # Responder com o desafio para confirmar o endpoint
        return challenge
    else:
        # Responder com erro se o token não corresponder
        return jsonify({"error": "Verification failed"}), 403

@app.route('/webhook', methods=['POST'])
def receive_webhook():
    """
    Endpoint para receber notificações de webhook
    """
    # Responder rapidamente para confirmar o recebimento
    data = request.json
    
    # Verificar se é uma notificação válida
    if data.get('object') == 'whatsapp_business_account':
        try:
            # Processar os dados recebidos de forma assíncrona
            # Em produção, use uma fila de tarefas como Celery
            process_webhook_event(data)
            return 'EVENT_RECEIVED', 200
        except Exception as e:
            print(f"Erro ao processar webhook: {str(e)}")
            return 'EVENT_RECEIVED', 200
    else:
        return jsonify({"error": "Invalid request"}), 404

def process_webhook_event(body):
    """
    Processa eventos de webhook
    """
    try:
        # Extrair dados relevantes
        entries = body.get('entry', [])
        
        for entry in entries:
            changes = entry.get('changes', [])
            
            for change in changes:
                if change.get('field') == 'messages':
                    value = change.get('value', {})
                    
                    # Processar mensagens recebidas
                    if 'messages' in value:
                        process_messages(value)
                    
                    # Processar atualizações de status
                    if 'statuses' in value:
                        process_statuses(value)
    except Exception as e:
        print(f"Erro ao processar evento de webhook: {str(e)}")
        raise

def process_messages(value):
    """
    Processa mensagens recebidas
    """
    metadata = value.get('metadata', {})
    phone_number_id = metadata.get('phone_number_id')
    
    for message in value.get('messages', []):
        from_number = message.get('from')
        message_id = message.get('id')
        message_type = message.get('type')
        
        print(f"Mensagem recebida de {from_number}, tipo: {message_type}")
        
        # Processar diferentes tipos de mensagens
        if message_type == 'text':
            text = message.get('text', {}).get('body', '')
            handle_text_message(phone_number_id, from_number, text, message_id)
        elif message_type == 'image':
            handle_image_message(phone_number_id, from_number, message.get('image'), message_id)
        elif message_type == 'interactive':
            handle_interactive_message(phone_number_id, from_number, message.get('interactive'), message_id)
        # Adicione handlers para outros tipos de mensagens

def process_statuses(value):
    """
    Processa atualizações de status
    """
    for status in value.get('statuses', []):
        message_id = status.get('id')
        status_value = status.get('status')
        recipient_id = status.get('recipient_id')
        
        print(f"Status atualizado para mensagem {message_id}: {status_value}")
        
        # Atualizar o status da mensagem no banco de dados
        # update_message_status(message_id, status_value)

def handle_text_message(phone_number_id, from_number, text, message_id):
    """
    Processa mensagens de texto
    """
    print(f"Mensagem de texto de {from_number}: {text}")
    
    # Exemplo: responder à mensagem
    response = f"Você disse: {text}"
    send_text_message(from_number, response)

def handle_image_message(phone_number_id, from_number, image_data, message_id):
    """
    Processa mensagens de imagem
    """
    print(f"Imagem recebida de {from_number}")
    
    # Baixar a imagem
    media_id = image_data.get('id')
    output_path = f"media/{media_id}.jpg"
    
    try:
        client.download_media(media_id, output_path)
        print(f"Imagem salva em {output_path}")
        
        # Responder ao usuário
        send_text_message(from_number, "Recebemos sua imagem!")
    except Exception as e:
        print(f"Erro ao baixar imagem: {str(e)}")
        send_text_message(from_number, "Não foi possível processar sua imagem.")

def handle_interactive_message(phone_number_id, from_number, interactive_data, message_id):
    """
    Processa mensagens interativas
    """
    interactive_type = interactive_data.get('type')
    
    if interactive_type == 'button_reply':
        button_id = interactive_data.get('button_reply', {}).get('id')
        button_text = interactive_data.get('button_reply', {}).get('title')
        
        print(f"Usuário {from_number} clicou no botão: {button_text} (ID: {button_id})")
        
        # Processar a resposta do botão
        if button_id == 'sim-pedido':
            send_text_message(from_number, "Pedido confirmado! Obrigado.")
        elif button_id == 'nao-pedido':
            send_text_message(from_number, "Pedido cancelado. Podemos ajudar com mais alguma coisa?")
    
    elif interactive_type == 'list_reply':
        list_id = interactive_data.get('list_reply', {}).get('id')
        list_title = interactive_data.get('list_reply', {}).get('title')
        
        print(f"Usuário {from_number} selecionou da lista: {list_title} (ID: {list_id})")
        
        # Processar a seleção da lista
        if list_id.startswith('cat-'):
            category = list_id.replace('cat-', '')
            send_text_message(from_number, f"Você selecionou a categoria: {category}")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
```

## Aplicação Principal

Arquivo `app.py`:

```python
from flask import Flask, request, jsonify, render_template
import os
from dotenv import load_dotenv
from whatsapp_client import WhatsAppClient
from webhook_handler import app as webhook_app

# Carregar variáveis de ambiente
load_dotenv()

app = Flask(__name__)
client = WhatsAppClient()

# Registrar as rotas do webhook
app.register_blueprint(webhook_app)

@app.route('/')
def index():
    return "WhatsApp Business API Client"

@app.route('/send-message', methods=['POST'])
def send_message_api():
    """
    API para enviar mensagens
    """
    data = request.json
    
    if not data:
        return jsonify({"error": "No data provided"}), 400
    
    try:
        to = data.get('to')
        message_type = data.get('type', 'text')
        
        if not to:
            return jsonify({"error": "Recipient ('to') is required"}), 400
        
        if message_type == 'text':
            text = data.get('text')
            if not text:
                return jsonify({"error": "Text is required for text messages"}), 400
            
            result = send_text_message(to, text)
            return jsonify({"success": True, "result": result})
        
        elif message_type == 'template':
            template_name = data.get('template_name')
            language_code = data.get('language_code', 'pt_BR')
            components = data.get('components')
            
            if not template_name:
                return jsonify({"error": "Template name is required"}), 400
            
            result = send_template_message(to, template_name, language_code, components)
            return jsonify({"success": True, "result": result})
        
        else:
            return jsonify({"error": f"Unsupported message type: {message_type}"}), 400
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
```

## Tratamento de Erros e Retentativas

Exemplo de implementação de retentativas com recuo exponencial:

```python
import time
import random

def send_with_retry(func, *args, max_retries=3, base_delay=1, **kwargs):
    """
    Executa uma função com retentativas em caso de falha
    
    Args:
        func: Função a ser executada
        *args: Argumentos posicionais para a função
        max_retries: Número máximo de tentativas
        base_delay: Atraso base entre tentativas (em segundos)
        **kwargs: Argumentos nomeados para a função
    
    Returns:
        O resultado da função
    
    Raises:
        Exception: Se todas as tentativas falharem
    """
    last_exception = None
    
    for attempt in range(1, max_retries + 1):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            last_exception = e
            
            # Verificar se o erro é retentável
            if not is_retryable_error(e):
                raise
            
            # Calcular atraso com jitter para evitar tempestade de tráfego
            delay = base_delay * (2 ** (attempt - 1)) + random.uniform(0, 0.5)
            
            print(f"Tentativa {attempt} falhou: {str(e)}. Tentando novamente em {delay:.2f}s")
            time.sleep(delay)
    
    # Se chegou aqui, todas as tentativas falharam
    raise last_exception

def is_retryable_error(exception):
    """
    Verifica se um erro é retentável
    
    Args:
        exception: A exceção a ser verificada
    
    Returns:
        bool: True se o erro for retentável, False caso contrário
    """
    # Códigos de erro que podem ser tentados novamente
    retryable_codes = [80004, 131053, 1, 2]
    
    # Verificar se a exceção tem um código de erro
    if hasattr(exception, 'code'):
        return exception.code in retryable_codes
    
    # Verificar se a exceção é uma falha de rede
    if isinstance(exception, (requests.ConnectionError, requests.Timeout)):
        return True
    
    return False

# Exemplo de uso
try:
    result = send_with_retry(
        send_text_message,
        "5511999999999",
        "Esta mensagem será enviada com retentativas em caso de falha",
        max_retries=5,
        base_delay=2
    )
    print("Mensagem enviada com sucesso:", result)
except Exception as e:
    print("Falha ao enviar mensagem após várias tentativas:", str(e))
```

## Recursos Adicionais

- [Documentação oficial da API do WhatsApp Business](https://developers.facebook.com/docs/whatsapp/cloud-api)
- [Biblioteca Python WhatsApp Cloud API Client](https://github.com/david-lev/pywa)
- [Exemplos de código no GitHub](https://github.com/fbsamples/whatsapp-api-examples)
- [Fórum de desenvolvedores da Meta](https://developers.facebook.com/community/)
