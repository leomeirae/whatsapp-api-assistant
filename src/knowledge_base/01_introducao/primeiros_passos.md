# Primeiros Passos com a API do WhatsApp Business

Este guia apresenta os passos essenciais para começar a utilizar a API do WhatsApp Business (Cloud API), desde a criação da conta até o envio da primeira mensagem.

## 1. Requisitos Iniciais

Antes de começar, você precisará:

- **Conta comercial no Facebook Business Manager**
- **Número de telefone dedicado** (que não esteja sendo usado em outro aplicativo WhatsApp)
- **Conhecimentos básicos de API REST** (para implementação direta)
- **Documentos comerciais** para verificação da empresa

## 2. Criação da Conta WhatsApp Business

### 2.1. Criar uma conta no Facebook Business Manager

1. Acesse [business.facebook.com](https://business.facebook.com/)
2. Clique em "Criar conta"
3. Siga as instruções para configurar sua empresa

### 2.2. Criar uma Conta WhatsApp Business (WABA)

1. No Business Manager, navegue até "Configurações da empresa"
2. Selecione "Contas" e depois "Contas do WhatsApp"
3. Clique em "Adicionar" e siga as instruções
4. Escolha entre criar uma conta própria ou trabalhar com um parceiro de negócios

### 2.3. Verificação da Empresa

A verificação da empresa é um processo obrigatório para usar a API do WhatsApp Business:

1. No Business Manager, acesse "Segurança" e depois "Verificação de negócios"
2. Forneça as informações solicitadas (nome legal, endereço, documentos comerciais)
3. Aguarde a aprovação (pode levar alguns dias)

## 3. Configuração da API

### 3.1. Criar um Aplicativo Meta

1. Acesse [developers.facebook.com](https://developers.facebook.com/)
2. Clique em "Meus Aplicativos" e depois "Criar Aplicativo"
3. Selecione "Empresa" como tipo de aplicativo
4. Preencha as informações solicitadas

### 3.2. Adicionar o Produto WhatsApp ao Aplicativo

1. Na página do seu aplicativo, clique em "Adicionar produtos"
2. Selecione "WhatsApp" na lista de produtos
3. Siga as instruções para configurar o produto

### 3.3. Configurar um Número de Telefone

1. Na seção WhatsApp do seu aplicativo, clique em "Começar"
2. Selecione "Adicionar número de telefone"
3. Escolha entre usar um novo número ou migrar um número existente
4. Siga o processo de verificação do número

## 4. Obtenção de Credenciais de Acesso

### 4.1. Gerar Token de Acesso

1. Na seção WhatsApp do seu aplicativo, acesse "Configuração da API"
2. Gere um token de acesso temporário ou permanente
3. Guarde este token com segurança - ele será usado em todas as chamadas à API

### 4.2. Identificar o ID do Número de Telefone

1. Na seção de números de telefone, localize o ID do seu número
2. Este ID será usado nas chamadas à API para identificar o remetente

## 5. Configuração de Webhooks

Os webhooks são essenciais para receber mensagens e atualizações de status:

1. Configure um endpoint HTTPS em seu servidor para receber notificações
2. Na seção de webhooks do seu aplicativo, adicione este endpoint
3. Configure os campos que deseja receber (mensagens, status de entrega, etc.)
4. Verifique o endpoint usando o desafio de verificação

## 6. Criação de Modelos de Mensagem

Para enviar mensagens proativas (fora da janela de 24 horas), você precisará de modelos aprovados:

1. Na seção "Gerenciamento de modelos", clique em "Criar modelo"
2. Escolha o tipo de modelo (transacional, marketing, etc.)
3. Crie o conteúdo seguindo as diretrizes do WhatsApp
4. Envie para aprovação (pode levar até 24 horas)

## 7. Envio da Primeira Mensagem

### 7.1. Mensagem de Texto Simples (dentro da janela de 24h)

```http
POST https://graph.facebook.com/v17.0/PHONE_NUMBER_ID/messages
Content-Type: application/json
Authorization: Bearer YOUR_ACCESS_TOKEN

{
  "messaging_product": "whatsapp",
  "recipient_type": "individual",
  "to": "RECIPIENT_PHONE_NUMBER",
  "type": "text",
  "text": {
    "body": "Olá! Esta é minha primeira mensagem via API do WhatsApp Business."
  }
}
```

### 7.2. Mensagem de Template (pode ser enviada a qualquer momento)

```http
POST https://graph.facebook.com/v17.0/PHONE_NUMBER_ID/messages
Content-Type: application/json
Authorization: Bearer YOUR_ACCESS_TOKEN

{
  "messaging_product": "whatsapp",
  "recipient_type": "individual",
  "to": "RECIPIENT_PHONE_NUMBER",
  "type": "template",
  "template": {
    "name": "hello_world",
    "language": {
      "code": "pt_BR"
    }
  }
}
```

## 8. Recebimento de Mensagens

Quando um usuário responde, você receberá uma notificação no webhook configurado:

1. Processe o payload JSON recebido
2. Extraia o número do remetente, o conteúdo da mensagem e outros dados relevantes
3. Implemente a lógica de negócio para responder adequadamente

## 9. Próximos Passos

Após configurar com sucesso a API e enviar/receber mensagens básicas, considere:

- Implementar um sistema de gerenciamento de conversas
- Criar fluxos automatizados para casos de uso comuns
- Desenvolver integrações com seus sistemas existentes (CRM, e-commerce, etc.)
- Explorar recursos avançados como botões interativos, listas e mídia

## 10. Recursos Adicionais

- [Documentação oficial da Cloud API](https://developers.facebook.com/docs/whatsapp/cloud-api)
- [Guia de modelos de mensagem](https://developers.facebook.com/docs/whatsapp/message-templates)
- [Políticas de negócios do WhatsApp](https://www.whatsapp.com/legal/business-policy)
- [Fórum de desenvolvedores](https://developers.facebook.com/community/)
