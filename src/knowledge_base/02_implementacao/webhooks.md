# Webhooks na API do WhatsApp Business

Os webhooks são um componente fundamental da API do WhatsApp Business, permitindo que sua aplicação receba notificações em tempo real sobre mensagens recebidas, status de entrega e outros eventos importantes. Este guia detalha como configurar, gerenciar e solucionar problemas com webhooks.

## O que são Webhooks?

Webhooks são callbacks HTTP que são acionados por eventos específicos. No contexto da API do WhatsApp Business, quando ocorre um evento (como o recebimento de uma mensagem), a plataforma envia uma notificação HTTP POST para um endpoint configurado em sua aplicação.

## Tipos de Notificações

A API do WhatsApp Business envia dois tipos principais de notificações via webhook:

1. **Mensagens recebidas**: Notificações quando um usuário envia uma mensagem para o seu número do WhatsApp Business.
2. **Status de mensagens**: Atualizações sobre o status das mensagens que você enviou (enviada, entregue, lida, falha).

## Configuração de Webhooks

### 1. Requisitos Técnicos

Para configurar webhooks, você precisa:

- Um servidor web acessível publicamente
- Um endpoint HTTPS com certificado SSL válido (certificados autoassinados não são aceitos)
- Capacidade de processar solicitações HTTP POST e responder com status 200

### 2. Criar um Endpoint para Webhooks

Seu endpoint deve ser capaz de lidar com dois tipos de solicitações:

#### 2.1. Verificação do Webhook (GET)

Quando você configura um webhook, a Meta envia uma solicitação GET para verificar se o endpoint é válido:

```javascript
// Node.js (Express)
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
```

```python
# Python (Flask)
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
```

#### 2.2. Recebimento de Notificações (POST)

Quando ocorre um evento, a Meta envia uma solicitação POST para o seu endpoint:

```javascript
// Node.js (Express)
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
```

```python
# Python (Flask)
@app.route('/webhook', methods=['POST'])
def receive_webhook():
    # Responda rapidamente para confirmar o recebimento
    data = request.json
    
    if data['object'] == 'whatsapp_business_account':
        # Processe os dados recebidos de forma assíncrona
        # Em produção, use uma fila de tarefas como Celery
        process_webhook_event(data)
    
    return 'EVENT_RECEIVED', 200
```

### 3. Configurar o Webhook no Aplicativo Meta

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

## Estrutura das Notificações

### 1. Estrutura Geral

Todas as notificações de webhook seguem esta estrutura geral:

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
            // Conteúdo específico do tipo de notificação
          },
          "field": "messages"
        }
      ]
    }
  ]
}
```

### 2. Notificação de Mensagem Recebida

Quando um usuário envia uma mensagem para o seu número:

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
                "type": "text",
                "text": {
                  "body": "MESSAGE_BODY"
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

### 3. Notificação de Status de Mensagem

Quando o status de uma mensagem enviada muda:

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
                "status": "read", // sent, delivered, read, failed
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

## Processamento de Notificações

### 1. Processamento Assíncrono

É importante responder rapidamente às solicitações de webhook e processar os dados de forma assíncrona:

```javascript
// Node.js (Express)
async function processWebhookEvent(body) {
  try {
    // Extrair dados relevantes
    const entries = body.entry || [];
    
    for (const entry of entries) {
      const changes = entry.changes || [];
      
      for (const change of changes) {
        if (change.field === 'messages') {
          const value = change.value;
          
          // Processar mensagens recebidas
          if (value.messages) {
            await processMessages(value);
          }
          
          // Processar atualizações de status
          if (value.statuses) {
            await processStatuses(value);
          }
        }
      }
    }
  } catch (error) {
    console.error('Erro ao processar evento de webhook:', error);
  }
}
```

### 2. Processamento de Mensagens

```javascript
async function processMessages(value) {
  const metadata = value.metadata;
  const phoneNumberId = metadata.phone_number_id;
  
  for (const message of value.messages || []) {
    const from = message.from; // Número do remetente
    const messageId = message.id; // ID da mensagem
    
    // Processar diferentes tipos de mensagens
    switch (message.type) {
      case 'text':
        await handleTextMessage(phoneNumberId, from, message.text.body, messageId);
        break;
      case 'image':
        await handleImageMessage(phoneNumberId, from, message.image, messageId);
        break;
      // Adicione handlers para outros tipos de mensagens
    }
  }
}
```

### 3. Processamento de Status

```javascript
async function processStatuses(value) {
  for (const status of value.statuses || []) {
    const messageId = status.id;
    const recipientId = status.recipient_id;
    const statusValue = status.status;
    
    // Atualizar o status da mensagem no banco de dados
    await updateMessageStatus(messageId, statusValue);
    
    // Executar ações específicas com base no status
    switch (statusValue) {
      case 'sent':
        console.log(`Mensagem ${messageId} enviada para ${recipientId}`);
        break;
      case 'delivered':
        console.log(`Mensagem ${messageId} entregue para ${recipientId}`);
        break;
      case 'read':
        console.log(`Mensagem ${messageId} lida por ${recipientId}`);
        break;
      case 'failed':
        console.log(`Falha ao enviar mensagem ${messageId} para ${recipientId}`);
        // Implementar lógica de retentativa ou notificação
        break;
    }
  }
}
```

## Melhores Práticas

### 1. Resposta Rápida

- Responda imediatamente às solicitações de webhook com status 200
- Processe as notificações de forma assíncrona
- Use filas de tarefas para processamento em segundo plano

### 2. Idempotência

- Implemente idempotência para lidar com notificações duplicadas
- Use IDs de mensagem para evitar processamento duplicado
- Armazene IDs de mensagens processadas para verificação

### 3. Tratamento de Erros

- Implemente tratamento de erros robusto
- Registre erros para análise posterior
- Implemente retentativas para operações que falharem

### 4. Segurança

- Use um token de verificação forte e único
- Valide todas as solicitações recebidas
- Implemente limitação de taxa (rate limiting)
- Considere o uso de WAF (Web Application Firewall)

### 5. Monitoramento

- Implemente logs detalhados
- Configure alertas para falhas
- Monitore tempos de resposta e taxas de erro

## Falhas de Entrega de Webhook

Se a Meta não conseguir entregar uma notificação de webhook (por exemplo, se seu servidor estiver indisponível), ela tentará novamente com frequência decrescente por até 7 dias.

Isso pode resultar em notificações duplicadas, por isso é importante implementar idempotência.

## Endereços IP

A Meta envia notificações de webhook a partir de um conjunto específico de endereços IP. Se você estiver usando um firewall, pode permitir apenas esses endereços.

Para obter a lista atual de endereços IP, execute o seguinte comando:

```bash
whois -h whois.radb.net — '-i origin AS32934' | grep ^route | awk '{print $2}' | sort
```

Observe que esses endereços podem mudar periodicamente, então é recomendável atualizar sua lista regularmente.

## Solução de Problemas Comuns

### 1. Falha na Verificação do Webhook

**Possíveis causas:**
- URL do webhook incorreta
- Certificado SSL inválido ou expirado
- Token de verificação incorreto
- Endpoint não acessível publicamente

**Soluções:**
- Verifique a URL do webhook
- Confirme que o certificado SSL é válido
- Verifique o token de verificação
- Teste o endpoint com uma ferramenta como cURL ou Postman

### 2. Não Recebendo Notificações

**Possíveis causas:**
- Assinatura de webhook não configurada corretamente
- Campos não selecionados corretamente
- Problemas de rede ou firewall
- Endpoint retornando erros

**Soluções:**
- Verifique as assinaturas de webhook no painel do desenvolvedor
- Confirme que os campos corretos estão selecionados
- Verifique as configurações de rede e firewall
- Monitore os logs do servidor para erros

### 3. Notificações Duplicadas

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
