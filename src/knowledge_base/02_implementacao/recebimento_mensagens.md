# Recebimento de Mensagens com a API do WhatsApp Business

Este guia detalha como receber e processar mensagens enviadas pelos usuários através da API do WhatsApp Business, incluindo a configuração de webhooks, processamento de diferentes tipos de mensagens e melhores práticas.

## Visão Geral

O recebimento de mensagens na API do WhatsApp Business é baseado em webhooks. Quando um usuário envia uma mensagem para o seu número do WhatsApp Business, a plataforma envia uma notificação para um endpoint HTTPS configurado em sua aplicação.

## Configuração de Webhooks

### 1. Criar um Endpoint para Webhooks

Primeiro, você precisa criar um endpoint HTTPS em seu servidor para receber as notificações:

#### Node.js (Express)

```javascript
const express = require('express');
const app = express();

// Configurar middleware para processar JSON
app.use(express.json());

// Endpoint para verificação do webhook
app.get('/webhook', (req, res) => {
  // Verificação do webhook
  const mode = req.query['hub.mode'];
  const token = req.query['hub.verify_token'];
  const challenge = req.query['hub.challenge'];
  
  // Verifique se o token corresponde ao seu token de verificação
  if (mode === 'subscribe' && token === 'SEU_TOKEN_DE_VERIFICACAO') {
    // Responda com o desafio para confirmar o endpoint
    res.status(200).send(challenge);
  } else {
    // Responda com erro se o token não corresponder
    res.sendStatus(403);
  }
});

// Endpoint para receber notificações
app.post('/webhook', (req, res) => {
  // Responda rapidamente para confirmar o recebimento
  res.status(200).send('EVENT_RECEIVED');
  
  // Processe a solicitação de forma assíncrona
  const body = req.body;
  
  if (body.object === 'whatsapp_business_account') {
    // Processe os dados recebidos
    processWebhookEvent(body).catch(console.error);
  }
});

// Função para processar eventos de webhook
async function processWebhookEvent(body) {
  try {
    // Extrair dados relevantes
    const entries = body.entry || [];
    
    for (const entry of entries) {
      const changes = entry.changes || [];
      
      for (const change of changes) {
        if (change.field === 'messages') {
          const value = change.value;
          
          if (!value || !value.messages || !value.messages.length) {
            continue;
          }
          
          const metadata = value.metadata;
          const phoneNumberId = metadata.phone_number_id;
          
          for (const message of value.messages) {
            const from = message.from; // Número do remetente
            const messageId = message.id; // ID da mensagem
            const timestamp = message.timestamp; // Timestamp da mensagem
            
            // Processar diferentes tipos de mensagens
            switch (message.type) {
              case 'text':
                await handleTextMessage(phoneNumberId, from, message.text.body, messageId);
                break;
              case 'image':
                await handleImageMessage(phoneNumberId, from, message.image, messageId);
                break;
              case 'audio':
                await handleAudioMessage(phoneNumberId, from, message.audio, messageId);
                break;
              case 'document':
                await handleDocumentMessage(phoneNumberId, from, message.document, messageId);
                break;
              case 'video':
                await handleVideoMessage(phoneNumberId, from, message.video, messageId);
                break;
              case 'location':
                await handleLocationMessage(phoneNumberId, from, message.location, messageId);
                break;
              case 'contacts':
                await handleContactsMessage(phoneNumberId, from, message.contacts, messageId);
                break;
              case 'button':
                await handleButtonMessage(phoneNumberId, from, message.button, messageId);
                break;
              case 'interactive':
                await handleInteractiveMessage(phoneNumberId, from, message.interactive, messageId);
                break;
              default:
                console.log(`Tipo de mensagem não suportado: ${message.type}`);
            }
          }
        }
      }
    }
  } catch (error) {
    console.error('Erro ao processar evento de webhook:', error);
  }
}

// Iniciar o servidor
const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
  console.log(`Servidor rodando na porta ${PORT}`);
});
```

#### Python (Flask)

```python
from flask import Flask, request, jsonify
import os
import asyncio

app = Flask(__name__)

@app.route('/webhook', methods=['GET'])
def verify_webhook():
    # Verificação do webhook
    mode = request.args.get('hub.mode')
    token = request.args.get('hub.verify_token')
    challenge = request.args.get('hub.challenge')
    
    # Verifique se o token corresponde ao seu token de verificação
    if mode == 'subscribe' and token == 'SEU_TOKEN_DE_VERIFICACAO':
        # Responda com o desafio para confirmar o endpoint
        return challenge
    else:
        # Responda com erro se o token não corresponder
        return '', 403

@app.route('/webhook', methods=['POST'])
def receive_webhook():
    # Responda rapidamente para confirmar o recebimento
    data = request.json
    
    if data['object'] == 'whatsapp_business_account':
        # Processe os dados recebidos de forma assíncrona
        # Em produção, use uma fila de tarefas como Celery
        asyncio.run(process_webhook_event(data))
    
    return 'EVENT_RECEIVED', 200

async def process_webhook_event(body):
    try:
        # Extrair dados relevantes
        entries = body.get('entry', [])
        
        for entry in entries:
            changes = entry.get('changes', [])
            
            for change in changes:
                if change['field'] == 'messages':
                    value = change.get('value', {})
                    
                    if not value or 'messages' not in value or not value['messages']:
                        continue
                    
                    metadata = value.get('metadata', {})
                    phone_number_id = metadata.get('phone_number_id')
                    
                    for message in value['messages']:
                        from_number = message.get('from')  # Número do remetente
                        message_id = message.get('id')  # ID da mensagem
                        timestamp = message.get('timestamp')  # Timestamp da mensagem
                        
                        # Processar diferentes tipos de mensagens
                        message_type = message.get('type')
                        if message_type == 'text':
                            await handle_text_message(phone_number_id, from_number, message['text']['body'], message_id)
                        elif message_type == 'image':
                            await handle_image_message(phone_number_id, from_number, message['image'], message_id)
                        # Adicione handlers para outros tipos de mensagens
    
    except Exception as e:
        print(f'Erro ao processar evento de webhook: {e}')

if __name__ == '__main__':
    app.run(port=int(os.environ.get('PORT', 3000)))
```

### 2. Configurar o Webhook no Aplicativo Meta

1. Acesse o [Meta for Developers](https://developers.facebook.com/)
2. Navegue até seu aplicativo
3. Selecione "Webhooks" no menu lateral
4. Clique em "Adicionar assinatura"
5. Selecione "WhatsApp Business Account"
6. Insira a URL do seu endpoint (deve ser HTTPS)
7. Defina um token de verificação (string aleatória segura)
8. Selecione os campos a serem recebidos:
   - `messages`: para receber mensagens dos usuários
   - `message_status`: para receber atualizações de status de mensagens

## Tipos de Notificações de Webhook

### 1. Mensagens Recebidas

Quando um usuário envia uma mensagem para o seu número do WhatsApp Business, você receberá uma notificação com a seguinte estrutura:

```json
{
  "object": "whatsapp_business_account",
  "entry": [
    {
      "id": "WHATSAPP_BUSINESS_ACCOUNT_ID",
      "changes": [
        {
          "value": {
            "messaging_product": "whatsapp",
            "metadata": {
              "display_phone_number": "DISPLAY_PHONE_NUMBER",
              "phone_number_id": "PHONE_NUMBER_ID"
            },
            "contacts": [
              {
                "profile": {
                  "name": "CONTACT_NAME"
                },
                "wa_id": "WHATSAPP_ID"
              }
            ],
            "messages": [
              {
                "from": "SENDER_WHATSAPP_ID",
                "id": "MESSAGE_ID",
                "timestamp": "TIMESTAMP",
                "type": "MESSAGE_TYPE",
                // Conteúdo específico do tipo de mensagem
              }
            ]
          },
          "field": "messages"
        }
      ]
    }
  ]
}
```

### 2. Status de Mensagens

Você também receberá notificações sobre o status das mensagens que você enviou:

```json
{
  "object": "whatsapp_business_account",
  "entry": [
    {
      "id": "WHATSAPP_BUSINESS_ACCOUNT_ID",
      "changes": [
        {
          "value": {
            "messaging_product": "whatsapp",
            "metadata": {
              "display_phone_number": "DISPLAY_PHONE_NUMBER",
              "phone_number_id": "PHONE_NUMBER_ID"
            },
            "statuses": [
              {
                "id": "MESSAGE_ID",
                "recipient_id": "RECIPIENT_WHATSAPP_ID",
                "status": "STATUS",
                "timestamp": "TIMESTAMP",
                "conversation": {
                  "id": "CONVERSATION_ID",
                  "origin": {
                    "type": "CONVERSATION_ORIGIN_TYPE"
                  }
                },
                "pricing": {
                  "billable": true,
                  "pricing_model": "PRICING_MODEL",
                  "category": "PRICING_CATEGORY"
                }
              }
            ]
          },
          "field": "messages"
        }
      ]
    }
  ]
}
```

Os valores possíveis para `status` são:
- `sent`: A mensagem foi enviada
- `delivered`: A mensagem foi entregue ao dispositivo do destinatário
- `read`: A mensagem foi lida pelo destinatário
- `failed`: A mensagem falhou ao ser enviada

## Processamento de Diferentes Tipos de Mensagens

### 1. Mensagens de Texto

```javascript
async function handleTextMessage(phoneNumberId, from, text, messageId) {
  console.log(`Mensagem de texto recebida de ${from}: ${text}`);
  
  // Exemplo: responder à mensagem
  await sendWhatsAppMessage(phoneNumberId, from, `Você disse: ${text}`);
}
```

### 2. Mensagens de Imagem

```javascript
async function handleImageMessage(phoneNumberId, from, image, messageId) {
  console.log(`Imagem recebida de ${from}`);
  
  // A imagem pode ser acessada de duas formas:
  // 1. Através do ID da mídia
  const mediaId = image.id;
  
  // 2. Através da URL da mídia (requer download)
  if (image.caption) {
    console.log(`Legenda da imagem: ${image.caption}`);
  }
  
  // Baixar a mídia usando o ID
  const mediaUrl = await downloadMedia(mediaId);
  
  // Processar a imagem conforme necessário
  // ...
  
  // Responder ao usuário
  await sendWhatsAppMessage(phoneNumberId, from, "Recebemos sua imagem!");
}
```

### 3. Mensagens Interativas (Botões e Listas)

```javascript
async function handleInteractiveMessage(phoneNumberId, from, interactive, messageId) {
  console.log(`Mensagem interativa recebida de ${from}`);
  
  const interactiveType = interactive.type;
  
  if (interactiveType === 'button_reply') {
    const buttonId = interactive.button_reply.id;
    const buttonText = interactive.button_reply.title;
    
    console.log(`Usuário clicou no botão: ${buttonText} (ID: ${buttonId})`);
    
    // Processar a resposta do botão
    // ...
  } 
  else if (interactiveType === 'list_reply') {
    const listId = interactive.list_reply.id;
    const listTitle = interactive.list_reply.title;
    
    console.log(`Usuário selecionou da lista: ${listTitle} (ID: ${listId})`);
    
    // Processar a seleção da lista
    // ...
  }
  
  // Responder ao usuário
  await sendWhatsAppMessage(phoneNumberId, from, `Você selecionou: ${buttonText || listTitle}`);
}
```

## Download de Mídia

Para acessar mídia enviada pelos usuários, você precisa fazer o download usando o ID da mídia:

```javascript
async function downloadMedia(mediaId) {
  try {
    // 1. Obter a URL da mídia
    const mediaUrlResponse = await axios.get(
      `https://graph.facebook.com/v17.0/${mediaId}`,
      {
        headers: {
          'Authorization': `Bearer ${process.env.WHATSAPP_TOKEN}`
        }
      }
    );
    
    const mediaUrl = mediaUrlResponse.data.url;
    
    // 2. Baixar a mídia
    const mediaResponse = await axios.get(mediaUrl, {
      headers: {
        'Authorization': `Bearer ${process.env.WHATSAPP_TOKEN}`
      },
      responseType: 'arraybuffer'
    });
    
    // 3. Processar ou salvar a mídia
    // Exemplo: salvar em disco
    const mediaBuffer = Buffer.from(mediaResponse.data);
    const filePath = `./media/${mediaId}.jpg`; // Ajuste a extensão conforme o tipo de mídia
    
    fs.writeFileSync(filePath, mediaBuffer);
    
    return filePath;
  } catch (error) {
    console.error('Erro ao baixar mídia:', error);
    throw error;
  }
}
```

## Melhores Práticas

### 1. Resposta Rápida ao Webhook

- Responda imediatamente às solicitações de webhook com status 200
- Processe as mensagens de forma assíncrona para não bloquear a resposta
- Use filas de tarefas para processamento em segundo plano (Redis, RabbitMQ, etc.)

### 2. Tratamento de Erros

- Implemente tratamento de erros robusto
- Registre erros para análise posterior
- Implemente retentativas para operações que falharem

### 3. Segurança

- Valide todas as solicitações recebidas
- Use HTTPS com certificados válidos
- Implemente limitação de taxa (rate limiting)
- Considere o uso de WAF (Web Application Firewall)

### 4. Escalabilidade

- Projete seu sistema para lidar com picos de tráfego
- Use balanceamento de carga se necessário
- Considere arquiteturas sem servidor (serverless) para escalabilidade automática

### 5. Monitoramento

- Implemente logs detalhados
- Configure alertas para falhas
- Monitore tempos de resposta e taxas de erro

## Solução de Problemas Comuns

### 1. Webhook não está recebendo notificações

**Possíveis causas:**
- URL do webhook incorreta
- Certificado SSL inválido ou expirado
- Firewall bloqueando solicitações
- Campos de assinatura incorretos

**Soluções:**
- Verifique a URL do webhook no painel do desenvolvedor
- Confirme que o certificado SSL é válido
- Verifique as configurações de firewall
- Confirme que você assinou os campos corretos

### 2. Erro ao baixar mídia

**Possíveis causas:**
- Token de acesso inválido ou expirado
- ID de mídia incorreto
- Mídia expirada (disponível por apenas 30 dias)

**Soluções:**
- Verifique o token de acesso
- Confirme o ID da mídia
- Baixe e armazene a mídia o mais rápido possível após recebê-la

### 3. Mensagens duplicadas

**Possíveis causas:**
- Retentativas de webhook devido a falhas anteriores
- Múltiplas assinaturas para o mesmo evento

**Soluções:**
- Implemente idempotência usando IDs de mensagem
- Verifique as assinaturas de webhook no painel do desenvolvedor

## Recursos Adicionais

- [Documentação oficial de webhooks](https://developers.facebook.com/docs/whatsapp/cloud-api/webhooks)
- [Exemplos de payload de webhook](https://developers.facebook.com/docs/whatsapp/cloud-api/webhooks/payload-examples)
- [Guia de solução de problemas de webhook](https://developers.facebook.com/docs/whatsapp/cloud-api/support/troubleshooting)
