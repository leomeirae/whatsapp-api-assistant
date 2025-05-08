# Erros Comuns na API do WhatsApp Business e Como Resolvê-los

Este guia detalha os erros mais frequentes encontrados ao trabalhar com a API do WhatsApp Business, suas causas e soluções práticas para resolvê-los.

## Erros de Autenticação

### 1. "Invalid OAuth access token"

**Descrição**: O token de acesso fornecido é inválido ou expirou.

**Causas comuns**:
- Token expirado (tokens temporários duram apenas 24 horas)
- Token mal formatado ou corrompido
- Token sem as permissões necessárias
- Token revogado

**Soluções**:
- Gere um novo token de acesso
- Verifique se o token tem as permissões corretas (`whatsapp_business_messaging`)
- Para ambientes de produção, use tokens de sistema (permanentes)
- Implemente um sistema de renovação automática de tokens

**Exemplo de resposta de erro**:
```json
{
  "error": {
    "message": "Invalid OAuth access token.",
    "type": "OAuthException",
    "code": 190,
    "fbtrace_id": "AbCdEfGhIjKlMnO"
  }
}
```

### 2. "Permission denied"

**Descrição**: O token não tem permissão para realizar a operação solicitada.

**Causas comuns**:
- Permissões insuficientes no token
- Aplicativo não aprovado para as permissões necessárias
- Usuário do sistema sem acesso ao recurso

**Soluções**:
- Verifique as permissões do token
- Solicite aprovação para as permissões necessárias
- Atribua as permissões corretas ao usuário do sistema

**Exemplo de resposta de erro**:
```json
{
  "error": {
    "message": "Permission denied",
    "type": "OAuthException",
    "code": 200,
    "fbtrace_id": "AbCdEfGhIjKlMnO"
  }
}
```

## Erros de Envio de Mensagens

### 1. "Message failed to send because more than 24 hours have passed since the customer last replied to this number"

**Descrição**: Tentativa de enviar uma mensagem fora da janela de 24 horas sem usar um template.

**Causas comuns**:
- Envio de mensagem regular (não template) após 24 horas sem interação do usuário
- Cálculo incorreto da janela de 24 horas

**Soluções**:
- Use templates de mensagem para comunicações fora da janela de 24 horas
- Implemente um sistema para rastrear a janela de 24 horas
- Envie mensagens proativas apenas via templates aprovados

**Exemplo de resposta de erro**:
```json
{
  "error": {
    "message": "Message failed to send because more than 24 hours have passed since the customer last replied to this number",
    "type": "OAuthException",
    "code": 131047,
    "error_subcode": 2494013,
    "fbtrace_id": "AbCdEfGhIjKlMnO"
  }
}
```

### 2. "Parameter 'to' is not a valid WhatsApp ID"

**Descrição**: O número de telefone do destinatário está em formato inválido ou não é um número do WhatsApp.

**Causas comuns**:
- Formato incorreto do número (faltando código do país ou com caracteres inválidos)
- Número não registrado no WhatsApp
- Número em formato local sem código do país

**Soluções**:
- Use o formato internacional completo com código do país (ex: +5511999999999)
- Remova caracteres especiais como parênteses, hífens e espaços
- Verifique se o número está ativo no WhatsApp antes de enviar

**Exemplo de resposta de erro**:
```json
{
  "error": {
    "message": "Parameter 'to' is not a valid WhatsApp ID",
    "type": "OAuthException",
    "code": 100,
    "error_subcode": 2494047,
    "fbtrace_id": "AbCdEfGhIjKlMnO"
  }
}
```

### 3. "Template not found"

**Descrição**: O template especificado não existe ou não está aprovado.

**Causas comuns**:
- Nome do template incorreto
- Template não aprovado ou rejeitado
- Template em idioma diferente do especificado
- Template pertence a outra conta do WhatsApp Business

**Soluções**:
- Verifique o nome exato do template (sensível a maiúsculas/minúsculas)
- Confirme o status de aprovação do template
- Verifique se o código do idioma está correto
- Confirme que o template pertence à conta que está sendo usada

**Exemplo de resposta de erro**:
```json
{
  "error": {
    "message": "Template not found",
    "type": "OAuthException",
    "code": 100,
    "error_subcode": 2494048,
    "fbtrace_id": "AbCdEfGhIjKlMnO"
  }
}
```

### 4. "Media upload error"

**Descrição**: Falha ao enviar mídia (imagem, vídeo, documento, etc.).

**Causas comuns**:
- URL da mídia não é acessível publicamente
- Formato de arquivo não suportado
- Arquivo excede o tamanho máximo permitido
- Problemas de rede durante o upload

**Soluções**:
- Verifique se a URL é acessível sem autenticação
- Confirme se o formato do arquivo é suportado pelo WhatsApp
- Reduza o tamanho do arquivo (5MB para imagens, 16MB para vídeos, 100MB para documentos)
- Tente fazer upload prévio da mídia e use o ID em vez da URL

**Exemplo de resposta de erro**:
```json
{
  "error": {
    "message": "Media upload error",
    "type": "OAuthException",
    "code": 131053,
    "fbtrace_id": "AbCdEfGhIjKlMnO"
  }
}
```

## Erros de Webhook

### 1. "Webhook verification failed"

**Descrição**: Falha na verificação inicial do webhook.

**Causas comuns**:
- Token de verificação incorreto
- Endpoint não responde corretamente ao desafio
- Problemas de SSL/TLS no endpoint
- Endpoint não acessível publicamente

**Soluções**:
- Verifique se o token de verificação está correto
- Certifique-se de que o endpoint responde ao desafio com o valor exato
- Confirme que o certificado SSL é válido e não autoassinado
- Verifique se o endpoint é acessível publicamente

**Exemplo de log de erro**:
```
Webhook verification failed: Token mismatch or endpoint not responding correctly
```

### 2. "Webhook delivery failure"

**Descrição**: Falha ao entregar notificações de webhook ao endpoint configurado.

**Causas comuns**:
- Endpoint indisponível ou com tempo limite esgotado
- Endpoint retornando códigos de erro (não 200)
- Problemas de rede ou firewall
- Endpoint processando muito lentamente

**Soluções**:
- Verifique se o servidor está online e respondendo
- Configure o endpoint para responder rapidamente (status 200) e processar assincronamente
- Verifique configurações de firewall e rede
- Implemente monitoramento para detectar falhas no webhook

**Exemplo de log de erro**:
```
Webhook delivery failure: Endpoint returned status code 500
```

## Erros de Template

### 1. "Template rejected"

**Descrição**: O template submetido foi rejeitado durante o processo de aprovação.

**Causas comuns**:
- Conteúdo não corresponde à categoria selecionada
- Conteúdo viola as políticas do WhatsApp
- Exemplos de parâmetros inadequados ou ausentes
- Linguagem promocional em templates de utilidade

**Soluções**:
- Revise o motivo da rejeição no painel do WhatsApp Business
- Ajuste o conteúdo para corresponder à categoria selecionada
- Forneça exemplos claros e apropriados para todos os parâmetros
- Remova linguagem promocional de templates utilitários

**Exemplo de resposta de erro**:
```json
{
  "error": {
    "message": "Template rejected due to policy violation",
    "type": "OAuthException",
    "code": 131051,
    "fbtrace_id": "AbCdEfGhIjKlMnO"
  }
}
```

### 2. "Template parameters mismatch"

**Descrição**: Os parâmetros fornecidos não correspondem ao template.

**Causas comuns**:
- Número incorreto de parâmetros
- Parâmetros em ordem errada
- Tipos de parâmetros incorretos (texto vs. imagem vs. documento)
- Parâmetros ausentes para componentes obrigatórios

**Soluções**:
- Verifique o número exato de parâmetros necessários
- Confirme a ordem correta dos parâmetros
- Certifique-se de que os tipos de parâmetros correspondem ao template
- Forneça todos os parâmetros obrigatórios

**Exemplo de resposta de erro**:
```json
{
  "error": {
    "message": "Template parameters mismatch",
    "type": "OAuthException",
    "code": 131052,
    "fbtrace_id": "AbCdEfGhIjKlMnO"
  }
}
```

## Erros de Limite de Taxa (Rate Limiting)

### 1. "Too many requests"

**Descrição**: O limite de taxa da API foi excedido.

**Causas comuns**:
- Envio de muitas solicitações em um curto período
- Implementação sem controle de taxa adequado
- Picos de tráfego não gerenciados
- Múltiplas instâncias da aplicação enviando solicitações simultaneamente

**Soluções**:
- Implemente controle de taxa (rate limiting) em sua aplicação
- Use filas para distribuir solicitações ao longo do tempo
- Monitore o uso da API e ajuste conforme necessário
- Implemente retentativas com recuo exponencial

**Exemplo de resposta de erro**:
```json
{
  "error": {
    "message": "Too many requests",
    "type": "OAuthException",
    "code": 80004,
    "fbtrace_id": "AbCdEfGhIjKlMnO"
  }
}
```

## Erros de Qualidade de Conta

### 1. "Message sending blocked due to quality issues"

**Descrição**: Envio de mensagens bloqueado devido a problemas de qualidade da conta.

**Causas comuns**:
- Alta taxa de bloqueio por usuários
- Reclamações excessivas
- Violações de política
- Conteúdo inadequado ou spam

**Soluções**:
- Revise as métricas de qualidade no painel do WhatsApp Business
- Melhore a relevância e qualidade do conteúdo
- Obtenha opt-in explícito antes de enviar mensagens
- Respeite as preferências de comunicação dos usuários

**Exemplo de resposta de erro**:
```json
{
  "error": {
    "message": "Message sending blocked due to quality issues",
    "type": "OAuthException",
    "code": 131056,
    "fbtrace_id": "AbCdEfGhIjKlMnO"
  }
}
```

## Erros de Implementação

### 1. "Invalid request format"

**Descrição**: O formato da solicitação é inválido.

**Causas comuns**:
- JSON mal formatado
- Campos obrigatórios ausentes
- Tipos de dados incorretos
- Estrutura de solicitação incorreta

**Soluções**:
- Valide o JSON antes de enviar
- Verifique se todos os campos obrigatórios estão presentes
- Confirme os tipos de dados corretos para cada campo
- Compare com exemplos da documentação oficial

**Exemplo de resposta de erro**:
```json
{
  "error": {
    "message": "Invalid request format",
    "type": "OAuthException",
    "code": 100,
    "fbtrace_id": "AbCdEfGhIjKlMnO"
  }
}
```

### 2. "Unsupported message type"

**Descrição**: O tipo de mensagem não é suportado.

**Causas comuns**:
- Tentativa de usar um tipo de mensagem não suportado
- Erro de digitação no tipo de mensagem
- Uso de recursos em versão beta sem acesso

**Soluções**:
- Verifique os tipos de mensagem suportados na documentação
- Corrija erros de digitação no tipo de mensagem
- Solicite acesso a recursos beta se necessário

**Exemplo de resposta de erro**:
```json
{
  "error": {
    "message": "Unsupported message type",
    "type": "OAuthException",
    "code": 131050,
    "fbtrace_id": "AbCdEfGhIjKlMnO"
  }
}
```

## Melhores Práticas para Tratamento de Erros

### 1. Implementação de Retentativas

Implemente um sistema de retentativas para erros transitórios:

```javascript
async function sendWithRetry(data, maxRetries = 3, delay = 1000) {
  let lastError;
  
  for (let attempt = 1; attempt <= maxRetries; attempt++) {
    try {
      const response = await sendWhatsAppMessage(data);
      return response;
    } catch (error) {
      lastError = error;
      
      // Verificar se o erro é transitório e pode ser tentado novamente
      if (isRetryableError(error)) {
        console.log(`Tentativa ${attempt} falhou, tentando novamente em ${delay}ms`);
        await new Promise(resolve => setTimeout(resolve, delay));
        // Aumentar o delay para a próxima tentativa (recuo exponencial)
        delay *= 2;
      } else {
        // Erro não é retentável, falhar imediatamente
        throw error;
      }
    }
  }
  
  // Todas as tentativas falharam
  throw lastError;
}

function isRetryableError(error) {
  // Códigos de erro que podem ser tentados novamente
  const retryableCodes = [80004, 131053, 1, 2];
  return retryableCodes.includes(error.code);
}
```

### 2. Logging Abrangente

Implemente logging detalhado para facilitar a depuração:

```javascript
function logApiError(error, context) {
  const errorDetails = {
    timestamp: new Date().toISOString(),
    errorCode: error.code,
    errorSubcode: error.error_subcode,
    message: error.message,
    context: context,
    requestId: error.fbtrace_id
  };
  
  console.error('WhatsApp API Error:', JSON.stringify(errorDetails, null, 2));
  
  // Opcionalmente, envie para um serviço de monitoramento
  // sendToMonitoringService(errorDetails);
}
```

### 3. Monitoramento Proativo

Configure alertas para detectar problemas antes que afetem os usuários:

- **Monitore taxas de erro**: Configure alertas para aumentos súbitos em erros
- **Verifique tempos de resposta**: Detecte latência anormal na API
- **Acompanhe métricas de qualidade**: Monitore taxas de bloqueio e reclamações
- **Verifique status de webhooks**: Configure heartbeats para confirmar que os webhooks estão funcionando

## Recursos Adicionais

- [Documentação oficial de erros da API](https://developers.facebook.com/docs/whatsapp/cloud-api/support/error-codes)
- [Guia de solução de problemas](https://developers.facebook.com/docs/whatsapp/cloud-api/support/troubleshooting)
- [Fórum de desenvolvedores da Meta](https://developers.facebook.com/community/)
- [Status da plataforma Meta](https://developers.facebook.com/status/dashboard/)
