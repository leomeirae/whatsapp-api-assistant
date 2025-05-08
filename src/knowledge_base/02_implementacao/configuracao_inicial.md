# Configuração Inicial da API do WhatsApp Business

Este guia detalhado apresenta o passo a passo para configurar a API do WhatsApp Business (Cloud API) do zero, incluindo a criação de contas, configuração de aplicativos e preparação do ambiente técnico.

## 1. Configuração de Contas e Acesso

### 1.1. Criar uma Conta no Facebook Business Manager

1. Acesse [business.facebook.com](https://business.facebook.com/)
2. Clique em "Criar conta"
3. Preencha as informações da sua empresa
4. Adicione pessoas e contas de anúncios (se aplicável)

### 1.2. Criar uma Conta WhatsApp Business (WABA)

1. No Business Manager, navegue até "Configurações da empresa"
2. Selecione "Contas" e depois "Contas do WhatsApp"
3. Clique em "Adicionar" e siga as instruções
4. Escolha entre criar uma conta própria ou trabalhar com um parceiro de negócios

### 1.3. Verificação da Empresa

A verificação é obrigatória para usar a API:

1. No Business Manager, acesse "Segurança" e depois "Verificação de negócios"
2. Forneça as informações solicitadas:
   - Nome legal da empresa
   - Endereço comercial
   - Site da empresa
   - País de operação
   - Documentos comerciais (certificado de registro, documentos fiscais)
3. Aguarde a aprovação (geralmente 1-5 dias úteis)

### 1.4. Criar um Aplicativo Meta

1. Acesse [developers.facebook.com](https://developers.facebook.com/)
2. Clique em "Meus Aplicativos" e depois "Criar Aplicativo"
3. Selecione "Empresa" como tipo de aplicativo
4. Preencha as informações solicitadas:
   - Nome do aplicativo
   - E-mail de contato
   - Finalidade do aplicativo

## 2. Configuração do Aplicativo Meta

### 2.1. Adicionar o Produto WhatsApp ao Aplicativo

1. Na página do seu aplicativo, clique em "Adicionar produtos"
2. Selecione "WhatsApp" na lista de produtos
3. Você será direcionado para a página de configuração do WhatsApp

### 2.2. Configurar um Número de Telefone

1. Na seção WhatsApp do seu aplicativo, clique em "Começar"
2. Selecione "Adicionar número de telefone"
3. Escolha entre:
   - Usar um novo número
   - Migrar um número existente do WhatsApp Business App
   - Usar um número fornecido por um parceiro
4. Siga o processo de verificação do número:
   - Verificação por SMS: insira o código recebido
   - Verificação por chamada: atenda e anote o código fornecido

### 2.3. Obter Credenciais de Acesso

1. Na seção WhatsApp do seu aplicativo, acesse "Configuração da API"
2. Localize ou gere um token de acesso:
   - Token temporário (válido por 24 horas, para testes)
   - Token permanente (para uso em produção)
3. Anote o ID do número de telefone (Phone Number ID)
4. Anote o ID da conta WhatsApp Business (WABA ID)

## 3. Configuração Técnica

### 3.1. Preparar o Ambiente de Desenvolvimento

1. Escolha uma linguagem de programação e framework:
   - Node.js (Express, Nest.js)
   - Python (Flask, Django)
   - PHP (Laravel, Symfony)
   - Java (Spring)
   - .NET (ASP.NET Core)
2. Configure um servidor com HTTPS:
   - Servidor próprio com certificado SSL
   - Serviço de hospedagem com suporte a HTTPS
   - Serviços como AWS, Google Cloud, Azure, Heroku

### 3.2. Configurar Webhooks

Os webhooks são essenciais para receber mensagens e notificações:

1. Crie um endpoint em seu servidor para receber notificações:
   ```javascript
   // Exemplo em Node.js com Express
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
   
   app.post('/webhook', (req, res) => {
     // Processe as notificações recebidas
     const body = req.body;
     
     if (body.object === 'whatsapp_business_account') {
       // Processe os dados recebidos
       console.log('Notificação recebida:', JSON.stringify(body, null, 2));
       res.status(200).send('EVENT_RECEIVED');
     } else {
       // Responda com erro se o objeto não for reconhecido
       res.sendStatus(404);
     }
   });
   ```

2. Configure o webhook no aplicativo Meta:
   - Na seção "Webhooks" do seu aplicativo, clique em "Configurar webhooks"
   - Insira a URL do seu endpoint (deve ser HTTPS)
   - Defina um token de verificação (string aleatória segura)
   - Selecione os campos a serem recebidos:
     - `messages`: para receber mensagens dos usuários
     - `message_status`: para receber atualizações de status de mensagens
   - Clique em "Verificar e salvar"

### 3.3. Testar a Configuração

1. Envie uma mensagem de teste:
   ```bash
   curl -X POST \
     'https://graph.facebook.com/v17.0/SEU_PHONE_NUMBER_ID/messages' \
     -H 'Authorization: Bearer SEU_ACCESS_TOKEN' \
     -H 'Content-Type: application/json' \
     -d '{
       "messaging_product": "whatsapp",
       "recipient_type": "individual",
       "to": "NUMERO_DESTINATARIO",
       "type": "text",
       "text": {
         "body": "Olá! Esta é uma mensagem de teste da API do WhatsApp Business."
       }
     }'
   ```

2. Verifique se a mensagem foi entregue ao destinatário
3. Peça ao destinatário para responder e verifique se você recebe a notificação no webhook

## 4. Configuração de Modelos de Mensagem

Para enviar mensagens proativas (fora da janela de 24 horas), você precisará de modelos aprovados:

1. Na seção "Gerenciamento de modelos", clique em "Criar modelo"
2. Escolha o tipo de modelo:
   - **Utilitário**: para informações transacionais e de serviço
   - **Marketing**: para promoções e ofertas
   - **Autenticação**: para códigos de verificação
3. Selecione o idioma do modelo
4. Configure os componentes do modelo:
   - **Cabeçalho**: texto, imagem, documento ou vídeo
   - **Corpo**: texto principal com variáveis (se necessário)
   - **Rodapé**: texto adicional (opcional)
   - **Botões**: até 3 botões (opcional)
5. Forneça exemplos para as variáveis
6. Envie para aprovação (pode levar até 24 horas)

## 5. Configuração de Segurança

### 5.1. Gerenciamento de Tokens

1. Armazene tokens de forma segura:
   - Use variáveis de ambiente
   - Não inclua tokens no código-fonte
   - Considere o uso de cofres de segredos (AWS Secrets Manager, HashiCorp Vault)

2. Implemente rotação de tokens:
   - Crie um processo para atualizar tokens periodicamente
   - Tenha um plano para revogação de tokens comprometidos

### 5.2. Proteção de Webhooks

1. Valide todas as solicitações recebidas
2. Implemente limitação de taxa (rate limiting)
3. Considere o uso de WAF (Web Application Firewall)

## 6. Próximos Passos

Após a configuração inicial:

1. Desenvolva a lógica de negócio para processar mensagens
2. Implemente integrações com sistemas existentes
3. Configure monitoramento e alertas
4. Desenvolva fluxos de conversação automatizados
5. Teste exaustivamente antes de lançar em produção

## 7. Solução de Problemas Comuns

### 7.1. Problemas de Verificação de Número

- Certifique-se de que o número pode receber SMS ou chamadas
- Verifique se o número não está sendo usado em outro aplicativo WhatsApp
- Aguarde alguns minutos e tente novamente

### 7.2. Falhas no Webhook

- Verifique se o endpoint está acessível publicamente
- Confirme que o certificado SSL é válido
- Verifique se o token de verificação está correto
- Examine os logs do servidor para erros

### 7.3. Falhas no Envio de Mensagens

- Verifique se o token de acesso é válido e não expirou
- Confirme que o formato da solicitação está correto
- Verifique se o número do destinatário está no formato correto (com código do país)
- Examine a resposta da API para mensagens de erro específicas
