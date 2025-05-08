# Autenticação na API do WhatsApp Business

A autenticação é um componente crítico para garantir a segurança e o acesso adequado à API do WhatsApp Business. Este documento detalha os métodos de autenticação, boas práticas e soluções para problemas comuns.

## Visão Geral da Autenticação

A API do WhatsApp Business utiliza o padrão OAuth 2.0 para autenticação, com tokens de acesso sendo o principal método para autorizar solicitações. Todas as chamadas à API devem incluir um token de acesso válido.

## Tipos de Tokens de Acesso

### 1. Token de Acesso Temporário

- **Duração**: 24 horas
- **Uso recomendado**: Desenvolvimento e testes iniciais
- **Como obter**: Disponível na interface do desenvolvedor do aplicativo Meta

### 2. Token de Acesso de Longa Duração (User Access Token)

- **Duração**: 60 dias
- **Uso recomendado**: Desenvolvimento avançado e testes prolongados
- **Como obter**: Através do processo de login OAuth com permissões adequadas

### 3. Token de Acesso do Sistema (System User Access Token)

- **Duração**: Permanente (até ser revogado)
- **Uso recomendado**: Ambientes de produção
- **Como obter**: Criando um usuário do sistema no Business Manager e gerando um token para esse usuário

## Obtenção de Tokens de Acesso

### 1. Token Temporário (Console do Desenvolvedor)

1. Acesse o [Meta for Developers](https://developers.facebook.com/)
2. Navegue até seu aplicativo
3. Selecione "WhatsApp" > "Começar"
4. Na seção "Tokens de acesso", você encontrará o token temporário

### 2. Token de Sistema (Recomendado para Produção)

#### 2.1. Criar um Usuário do Sistema

1. No Business Manager, acesse "Configurações da empresa"
2. Selecione "Usuários" > "Usuários do sistema"
3. Clique em "Adicionar" e forneça um nome para o usuário do sistema
4. Atribua as permissões necessárias:
   - `whatsapp_business_messaging` (obrigatória)
   - `whatsapp_business_management` (para gerenciar templates)

#### 2.2. Gerar Token para o Usuário do Sistema

1. Selecione o usuário do sistema criado
2. Clique em "Adicionar ativos" e selecione seu aplicativo Meta
3. Atribua as permissões necessárias ao aplicativo
4. Clique em "Gerar novo token"
5. Selecione o aplicativo e as permissões
6. Clique em "Gerar token"
7. **IMPORTANTE**: Copie e armazene o token com segurança, pois ele não será mostrado novamente

## Uso do Token na API

### Formato do Cabeçalho de Autorização

Todas as solicitações à API devem incluir o token de acesso no cabeçalho `Authorization`:

```http
Authorization: Bearer YOUR_ACCESS_TOKEN
```

### Exemplos de Uso

#### cURL

```bash
curl -X POST \
  'https://graph.facebook.com/v17.0/PHONE_NUMBER_ID/messages' \
  -H 'Authorization: Bearer YOUR_ACCESS_TOKEN' \
  -H 'Content-Type: application/json' \
  -d '{
    "messaging_product": "whatsapp",
    "to": "RECIPIENT_PHONE_NUMBER",
    "type": "text",
    "text": {
      "body": "Olá, esta é uma mensagem de teste!"
    }
  }'
```

#### Node.js (Axios)

```javascript
const axios = require('axios');

async function sendWhatsAppMessage() {
  try {
    const response = await axios.post(
      `https://graph.facebook.com/v17.0/PHONE_NUMBER_ID/messages`,
      {
        messaging_product: "whatsapp",
        to: "RECIPIENT_PHONE_NUMBER",
        type: "text",
        text: {
          body: "Olá, esta é uma mensagem de teste!"
        }
      },
      {
        headers: {
          'Authorization': `Bearer YOUR_ACCESS_TOKEN`,
          'Content-Type': 'application/json'
        }
      }
    );
    
    console.log('Mensagem enviada:', response.data);
    return response.data;
  } catch (error) {
    console.error('Erro ao enviar mensagem:', error.response?.data || error.message);
    throw error;
  }
}
```

#### Python (Requests)

```python
import requests
import json

def send_whatsapp_message():
    url = f"https://graph.facebook.com/v17.0/PHONE_NUMBER_ID/messages"
    
    headers = {
        "Authorization": f"Bearer YOUR_ACCESS_TOKEN",
        "Content-Type": "application/json"
    }
    
    data = {
        "messaging_product": "whatsapp",
        "to": "RECIPIENT_PHONE_NUMBER",
        "type": "text",
        "text": {
            "body": "Olá, esta é uma mensagem de teste!"
        }
    }
    
    response = requests.post(url, headers=headers, data=json.dumps(data))
    
    if response.status_code == 200:
        print("Mensagem enviada com sucesso:", response.json())
        return response.json()
    else:
        print("Erro ao enviar mensagem:", response.text)
        response.raise_for_status()
```

## Boas Práticas de Segurança

### 1. Armazenamento Seguro de Tokens

- **Nunca armazene tokens no código-fonte**
- Use variáveis de ambiente ou serviços de gerenciamento de segredos:
  - AWS Secrets Manager
  - Google Secret Manager
  - Azure Key Vault
  - HashiCorp Vault
  - Doppler
  - .env (apenas para desenvolvimento local)

### 2. Rotação de Tokens

- Implemente um processo para rotação periódica de tokens
- Automatize a rotação quando possível
- Mantenha um registro de tokens ativos

### 3. Princípio do Menor Privilégio

- Atribua apenas as permissões necessárias aos usuários do sistema
- Revise periodicamente as permissões concedidas

### 4. Monitoramento e Auditoria

- Monitore o uso de tokens para detectar atividades suspeitas
- Implemente alertas para falhas de autenticação repetidas
- Mantenha logs de todas as operações sensíveis

## Solução de Problemas Comuns

### 1. Erro "Invalid OAuth access token"

**Causas possíveis:**
- Token expirado
- Token inválido ou mal formatado
- Token sem as permissões necessárias

**Soluções:**
- Gere um novo token
- Verifique se o token está sendo enviado corretamente
- Confirme se o token tem as permissões necessárias

### 2. Erro "Permission denied"

**Causas possíveis:**
- Token sem as permissões necessárias
- Usuário do sistema sem acesso ao recurso
- Aplicativo sem as permissões necessárias

**Soluções:**
- Verifique as permissões do token
- Adicione as permissões necessárias ao usuário do sistema
- Solicite aprovação para as permissões necessárias

### 3. Erro "Expired access token"

**Causas possíveis:**
- Token temporário ou de usuário expirado

**Soluções:**
- Gere um novo token
- Implemente um sistema de renovação automática de tokens
- Migre para tokens de sistema para uso em produção

## Verificação de Webhooks

Além da autenticação para enviar solicitações à API, você também precisa verificar as solicitações recebidas em seus webhooks:

### 1. Verificação Inicial do Webhook

Quando você configura um webhook, a Meta envia uma solicitação GET com um desafio que você deve responder:

```javascript
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

### 2. Verificação de Solicitações de Webhook

Para solicitações POST recebidas em seu webhook, você deve:

1. Verificar se o corpo da solicitação é válido
2. Responder rapidamente com um status 200 para confirmar o recebimento
3. Processar a solicitação de forma assíncrona, se necessário

```javascript
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

## Recursos Adicionais

- [Documentação oficial de autenticação da Meta](https://developers.facebook.com/docs/facebook-login/guides/access-tokens)
- [Guia de segurança para desenvolvedores da Meta](https://developers.facebook.com/docs/facebook-login/security)
- [Documentação de webhooks](https://developers.facebook.com/docs/graph-api/webhooks/getting-started)
