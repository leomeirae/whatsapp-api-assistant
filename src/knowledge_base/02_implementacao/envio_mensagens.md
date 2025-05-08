# Envio de Mensagens com a API do WhatsApp Business

Este guia detalha os diferentes tipos de mensagens que podem ser enviados através da API do WhatsApp Business, incluindo exemplos de código e melhores práticas.

## Conceitos Fundamentais

### Janela de Atendimento ao Cliente (Customer Service Window)

- **Duração**: 24 horas após a última mensagem do cliente
- **Importância**: Dentro desta janela, você pode enviar qualquer tipo de mensagem
- **Fora da janela**: Apenas mensagens de template podem ser enviadas

### Endpoint para Envio de Mensagens

Todas as mensagens são enviadas para o mesmo endpoint:

```
POST https://graph.facebook.com/v17.0/PHONE_NUMBER_ID/messages
```

### Estrutura Básica da Solicitação

```json
{
  "messaging_product": "whatsapp",
  "recipient_type": "individual",
  "to": "RECIPIENT_PHONE_NUMBER",
  "type": "TYPE_OF_MESSAGE",
  "TYPE_OF_MESSAGE": {
    // Conteúdo específico do tipo de mensagem
  }
}
```

## Tipos de Mensagens

### 1. Mensagens de Texto

As mensagens de texto são o tipo mais básico e podem incluir links que serão exibidos com pré-visualização.

#### Exemplo de Solicitação

```json
{
  "messaging_product": "whatsapp",
  "recipient_type": "individual",
  "to": "5511999999999",
  "type": "text",
  "text": {
    "preview_url": true,
    "body": "Olá! Confira nosso site: https://www.exemplo.com.br"
  }
}
```

#### Parâmetros

- `preview_url`: Quando `true`, links no texto serão exibidos com pré-visualização
- `body`: O conteúdo da mensagem (até 4096 caracteres)

### 2. Mensagens de Mídia

A API suporta vários tipos de mídia: imagens, documentos, áudio, vídeo e adesivos.

#### 2.1. Imagens

```json
{
  "messaging_product": "whatsapp",
  "recipient_type": "individual",
  "to": "5511999999999",
  "type": "image",
  "image": {
    "link": "https://www.exemplo.com.br/imagem.jpg",
    "caption": "Descrição opcional da imagem"
  }
}
```

Alternativamente, você pode usar um ID de mídia previamente carregado:

```json
{
  "messaging_product": "whatsapp",
  "recipient_type": "individual",
  "to": "5511999999999",
  "type": "image",
  "image": {
    "id": "MEDIA_OBJECT_ID",
    "caption": "Descrição opcional da imagem"
  }
}
```

#### 2.2. Documentos

```json
{
  "messaging_product": "whatsapp",
  "recipient_type": "individual",
  "to": "5511999999999",
  "type": "document",
  "document": {
    "link": "https://www.exemplo.com.br/documento.pdf",
    "caption": "Relatório Mensal",
    "filename": "relatorio-mensal.pdf"
  }
}
```

#### 2.3. Áudio

```json
{
  "messaging_product": "whatsapp",
  "recipient_type": "individual",
  "to": "5511999999999",
  "type": "audio",
  "audio": {
    "link": "https://www.exemplo.com.br/audio.mp3"
  }
}
```

#### 2.4. Vídeo

```json
{
  "messaging_product": "whatsapp",
  "recipient_type": "individual",
  "to": "5511999999999",
  "type": "video",
  "video": {
    "link": "https://www.exemplo.com.br/video.mp4",
    "caption": "Vídeo demonstrativo do produto"
  }
}
```

#### 2.5. Adesivos (Stickers)

```json
{
  "messaging_product": "whatsapp",
  "recipient_type": "individual",
  "to": "5511999999999",
  "type": "sticker",
  "sticker": {
    "link": "https://www.exemplo.com.br/sticker.webp"
  }
}
```

### 3. Mensagens Interativas

#### 3.1. Botões de Resposta Rápida

```json
{
  "messaging_product": "whatsapp",
  "recipient_type": "individual",
  "to": "5511999999999",
  "type": "interactive",
  "interactive": {
    "type": "button",
    "body": {
      "text": "Você gostaria de prosseguir com o pedido?"
    },
    "action": {
      "buttons": [
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
    }
  }
}
```

#### 3.2. Listas

```json
{
  "messaging_product": "whatsapp",
  "recipient_type": "individual",
  "to": "5511999999999",
  "type": "interactive",
  "interactive": {
    "type": "list",
    "header": {
      "type": "text",
      "text": "Opções de Atendimento"
    },
    "body": {
      "text": "Selecione uma das opções abaixo para continuar:"
    },
    "footer": {
      "text": "Atendimento 24h"
    },
    "action": {
      "button": "Ver Opções",
      "sections": [
        {
          "title": "Suporte Técnico",
          "rows": [
            {
              "id": "suporte-produto",
              "title": "Problemas com Produto",
              "description": "Suporte para problemas técnicos com o produto"
            },
            {
              "id": "suporte-instalacao",
              "title": "Ajuda com Instalação",
              "description": "Assistência para instalar o produto"
            }
          ]
        },
        {
          "title": "Vendas",
          "rows": [
            {
              "id": "vendas-novos",
              "title": "Novos Produtos",
              "description": "Informações sobre novos produtos"
            },
            {
              "id": "vendas-promocoes",
              "title": "Promoções",
              "description": "Ofertas e descontos especiais"
            }
          ]
        }
      ]
    }
  }
}
```

#### 3.3. Botões de URL

```json
{
  "messaging_product": "whatsapp",
  "recipient_type": "individual",
  "to": "5511999999999",
  "type": "interactive",
  "interactive": {
    "type": "cta_url",
    "body": {
      "text": "Visite nossa loja online para ver todos os produtos disponíveis."
    },
    "action": {
      "name": "cta_url",
      "parameters": {
        "display_text": "Visitar Loja",
        "url": "https://www.exemplo.com.br/loja"
      }
    }
  }
}
```

### 4. Mensagens de Template

As mensagens de template são o único tipo que pode ser enviado fora da janela de 24 horas. Elas devem ser criadas e aprovadas previamente.

```json
{
  "messaging_product": "whatsapp",
  "recipient_type": "individual",
  "to": "5511999999999",
  "type": "template",
  "template": {
    "name": "nome_do_template",
    "language": {
      "code": "pt_BR"
    },
    "components": [
      {
        "type": "header",
        "parameters": [
          {
            "type": "image",
            "image": {
              "link": "https://www.exemplo.com.br/imagem.jpg"
            }
          }
        ]
      },
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
  }
}
```

### 5. Mensagens de Localização

```json
{
  "messaging_product": "whatsapp",
  "recipient_type": "individual",
  "to": "5511999999999",
  "type": "location",
  "location": {
    "latitude": "-23.5505",
    "longitude": "-46.6333",
    "name": "Escritório Central",
    "address": "Av. Paulista, 1000 - São Paulo, SP"
  }
}
```

### 6. Mensagens de Contatos

```json
{
  "messaging_product": "whatsapp",
  "recipient_type": "individual",
  "to": "5511999999999",
  "type": "contacts",
  "contacts": [
    {
      "name": {
        "formatted_name": "João Silva",
        "first_name": "João",
        "last_name": "Silva"
      },
      "phones": [
        {
          "phone": "+5511988887777",
          "type": "CELL"
        }
      ],
      "emails": [
        {
          "email": "joao.silva@exemplo.com",
          "type": "WORK"
        }
      ]
    }
  ]
}
```

## Respostas Contextuais

Você pode responder a uma mensagem específica, criando um contexto de conversa:

```json
{
  "messaging_product": "whatsapp",
  "recipient_type": "individual",
  "to": "5511999999999",
  "context": {
    "message_id": "wamid.HBgLMTU1Mjc3..."
  },
  "type": "text",
  "text": {
    "body": "Esta é uma resposta à sua pergunta específica."
  }
}
```

## Indicadores de Digitação

Você pode mostrar ao usuário que está "digitando" uma resposta:

```json
{
  "messaging_product": "whatsapp",
  "recipient_type": "individual",
  "to": "5511999999999",
  "type": "typing",
  "typing": {
    "state": "typing"
  }
}
```

Para parar de mostrar o indicador:

```json
{
  "messaging_product": "whatsapp",
  "recipient_type": "individual",
  "to": "5511999999999",
  "type": "typing",
  "typing": {
    "state": "paused"
  }
}
```

## Confirmações de Leitura

Você pode marcar uma mensagem como lida:

```json
{
  "messaging_product": "whatsapp",
  "status": "read",
  "message_id": "wamid.HBgLMTU1Mjc3..."
}
```

## Exemplos de Código

### Node.js (Axios)

```javascript
const axios = require('axios');

async function sendWhatsAppMessage(phoneNumberId, recipientNumber, message) {
  try {
    const response = await axios.post(
      `https://graph.facebook.com/v17.0/${phoneNumberId}/messages`,
      {
        messaging_product: "whatsapp",
        recipient_type: "individual",
        to: recipientNumber,
        type: "text",
        text: {
          body: message
        }
      },
      {
        headers: {
          'Authorization': `Bearer ${process.env.WHATSAPP_TOKEN}`,
          'Content-Type': 'application/json'
        }
      }
    );
    
    return response.data;
  } catch (error) {
    console.error('Erro ao enviar mensagem:', error.response?.data || error.message);
    throw error;
  }
}
```

### Python (Requests)

```python
import requests
import os

def send_whatsapp_message(phone_number_id, recipient_number, message):
    url = f"https://graph.facebook.com/v17.0/{phone_number_id}/messages"
    
    headers = {
        "Authorization": f"Bearer {os.environ.get('WHATSAPP_TOKEN')}",
        "Content-Type": "application/json"
    }
    
    data = {
        "messaging_product": "whatsapp",
        "recipient_type": "individual",
        "to": recipient_number,
        "type": "text",
        "text": {
            "body": message
        }
    }
    
    response = requests.post(url, headers=headers, json=data)
    
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Erro ao enviar mensagem: {response.text}")
```

## Melhores Práticas

### 1. Formatação de Números de Telefone

- Sempre inclua o código do país com o sinal de + (ex: +5511999999999)
- Remova quaisquer outros caracteres especiais (parênteses, hífens, espaços)

### 2. Tratamento de Erros

- Implemente tratamento de erros robusto
- Armazene mensagens que falharam para tentar novamente mais tarde
- Monitore taxas de erro para identificar problemas sistêmicos

### 3. Limitação de Taxa (Rate Limiting)

- Respeite os limites de taxa da API
- Implemente filas para mensagens em massa
- Adicione atrasos entre mensagens em lote

### 4. Monitoramento

- Acompanhe o status de entrega das mensagens através de webhooks
- Implemente métricas para taxas de entrega, leitura e resposta
- Configure alertas para falhas anormais

### 5. Conformidade

- Respeite a janela de 24 horas para mensagens não-template
- Obtenha opt-in explícito dos usuários antes de enviar mensagens
- Siga as políticas de uso do WhatsApp Business

## Solução de Problemas Comuns

### 1. Erro "Message failed to send because more than 24 hours have passed since the customer last replied to this number"

**Solução**: Use mensagens de template para comunicações fora da janela de 24 horas.

### 2. Erro "Media upload error"

**Soluções**:
- Verifique se a URL da mídia é acessível publicamente
- Confirme se o formato do arquivo é suportado
- Verifique o tamanho do arquivo (limites: 5MB para imagens, 100MB para documentos)

### 3. Erro "Parameter 'to' is not a valid WhatsApp ID"

**Soluções**:
- Verifique o formato do número (deve incluir código do país com +)
- Confirme se o número está ativo no WhatsApp

### 4. Erro "Template not found"

**Soluções**:
- Verifique se o nome do template está correto
- Confirme se o template foi aprovado
- Verifique se o código do idioma está correto
