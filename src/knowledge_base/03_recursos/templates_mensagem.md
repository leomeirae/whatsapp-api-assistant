# Templates de Mensagem na API do WhatsApp Business

Os templates de mensagem são um recurso fundamental da API do WhatsApp Business, permitindo que empresas enviem mensagens proativas para seus clientes, mesmo fora da janela de 24 horas. Este guia detalha como criar, gerenciar e enviar templates de mensagem eficazes.

## O que são Templates de Mensagem?

Templates de mensagem são formatos pré-aprovados de mensagens que podem ser enviados a qualquer momento, mesmo quando não há uma conversa ativa nas últimas 24 horas. Eles são essenciais para iniciar conversas com clientes e enviar notificações importantes.

## Categorias de Templates

Os templates são classificados em três categorias principais, cada uma com regras e casos de uso específicos:

### 1. Utilitário (Utility)

**Descrição**: Mensagens transacionais e de serviço que fornecem informações essenciais solicitadas pelo cliente.

**Casos de uso**:
- Confirmações de pedido
- Atualizações de envio
- Confirmações de reserva
- Recibos
- Atualizações de status de serviço
- Lembretes de compromisso

**Exemplo**:
```
Olá {{1}}, sua reserva no restaurante Sabores Gourmet está confirmada para {{2}} às {{3}}. Seu código de confirmação é {{4}}. Para alterar ou cancelar, responda a esta mensagem.
```

### 2. Marketing

**Descrição**: Mensagens promocionais, ofertas e conteúdo não solicitado pelo cliente.

**Casos de uso**:
- Promoções e ofertas
- Anúncios de novos produtos
- Convites para eventos
- Programas de fidelidade
- Pesquisas de satisfação
- Conteúdo informativo

**Exemplo**:
```
Olá {{1}}! Nossa {{2}} está acontecendo agora! Compre até {{3}} e use o código {{4}} para obter {{5}} de desconto em todos os produtos. Visite nossa loja: example.com/promo
```

### 3. Autenticação (Authentication)

**Descrição**: Mensagens contendo códigos de verificação para autenticação.

**Casos de uso**:
- Códigos de verificação em duas etapas
- Códigos de login
- Redefinição de senha
- Verificação de conta

**Exemplo**:
```
Seu código de verificação é {{1}}. Este código expira em {{2}} minutos. Não compartilhe este código com ninguém.
```

## Componentes de Templates

Os templates podem incluir vários componentes para criar mensagens ricas e interativas:

### 1. Cabeçalho (Header)

Pode ser um dos seguintes tipos:
- **Texto**: Título ou introdução da mensagem
- **Imagem**: Uma imagem relevante
- **Documento**: Um arquivo PDF ou outro documento
- **Vídeo**: Um vídeo curto

### 2. Corpo (Body)

O texto principal da mensagem, que pode incluir variáveis (parâmetros) que serão substituídas por valores específicos ao enviar a mensagem.

### 3. Rodapé (Footer)

Texto adicional exibido na parte inferior da mensagem, geralmente usado para informações de contato ou avisos legais.

### 4. Botões

Até três botões interativos que podem ser:
- **Resposta Rápida**: Botões que enviam uma resposta predefinida
- **URL**: Botões que abrem um link
- **Telefone**: Botões que iniciam uma chamada telefônica

## Criação de Templates

Os templates podem ser criados de duas formas:

### 1. Através do WhatsApp Business Manager

1. Acesse o [WhatsApp Manager](https://business.facebook.com/wa/manage/message-templates/)
2. Selecione sua conta do WhatsApp Business
3. Clique em "Criar template"
4. Siga as instruções para configurar os componentes do template
5. Envie para aprovação

### 2. Através da API (Business Management API)

```http
POST https://graph.facebook.com/v17.0/WHATSAPP_BUSINESS_ACCOUNT_ID/message_templates
Content-Type: application/json
Authorization: Bearer YOUR_ACCESS_TOKEN

{
  "name": "order_confirmation",
  "language": "pt_BR",
  "category": "UTILITY",
  "components": [
    {
      "type": "HEADER",
      "format": "TEXT",
      "text": "Confirmação de Pedido #{{1}}",
      "example": {
        "header_text": [
          "12345"
        ]
      }
    },
    {
      "type": "BODY",
      "text": "Olá {{1}}, seu pedido foi confirmado e está sendo processado. Valor total: R$ {{2}}. Previsão de entrega: {{3}}.",
      "example": {
        "body_text": [
          [
            "João Silva",
            "150,00",
            "22/05/2023"
          ]
        ]
      }
    },
    {
      "type": "FOOTER",
      "text": "Obrigado por comprar conosco!"
    },
    {
      "type": "BUTTONS",
      "buttons": [
        {
          "type": "URL",
          "text": "Rastrear Pedido",
          "url": "https://exemplo.com.br/rastrear?id={{1}}",
          "example": [
            "12345"
          ]
        },
        {
          "type": "PHONE_NUMBER",
          "text": "Falar com Atendimento",
          "phone_number": "+551199999999"
        }
      ]
    }
  ]
}
```

## Processo de Aprovação

Todos os templates passam por um processo de revisão antes de poderem ser usados:

1. **Submissão**: Você cria e envia o template para aprovação
2. **Revisão**: A Meta revisa o template para garantir que ele segue as políticas
3. **Aprovação/Rejeição**: O template é aprovado ou rejeitado com um motivo
4. **Uso**: Se aprovado, o template pode ser usado para enviar mensagens

O tempo de aprovação geralmente varia de algumas horas a 2 dias úteis.

## Envio de Mensagens de Template

Uma vez aprovado, você pode enviar o template usando a API:

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
    "name": "order_confirmation",
    "language": {
      "code": "pt_BR"
    },
    "components": [
      {
        "type": "header",
        "parameters": [
          {
            "type": "text",
            "text": "12345"
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
            "text": "150,00"
          },
          {
            "type": "text",
            "text": "22/05/2023"
          }
        ]
      },
      {
        "type": "button",
        "sub_type": "url",
        "index": "0",
        "parameters": [
          {
            "type": "text",
            "text": "12345"
          }
        ]
      }
    ]
  }
}
```

## Parâmetros de Template

Os templates podem incluir parâmetros (variáveis) que são substituídos por valores específicos ao enviar a mensagem. Existem dois formatos de parâmetros:

### 1. Parâmetros Posicionais

Usa números entre chaves duplas para indicar a posição do parâmetro:

```
Olá {{1}}, seu pedido {{2}} foi confirmado no valor de R$ {{3}}.
```

### 2. Parâmetros Nomeados

Usa nomes entre chaves duplas para indicar o parâmetro:

```
Olá {{nome}}, seu pedido {{numero_pedido}} foi confirmado no valor de R$ {{valor}}.
```

## Melhores Práticas

### 1. Criação de Templates Eficazes

- **Seja claro e conciso**: Mantenha as mensagens diretas e fáceis de entender
- **Personalize**: Use parâmetros para personalizar as mensagens
- **Forneça valor**: Certifique-se de que a mensagem é útil para o destinatário
- **Inclua call-to-action**: Use botões para incentivar a interação
- **Respeite a categoria**: Certifique-se de que o conteúdo corresponde à categoria selecionada

### 2. Aumentar as Taxas de Aprovação

- **Siga as diretrizes**: Familiarize-se com as [políticas do WhatsApp Business](https://www.whatsapp.com/legal/business-policy/)
- **Evite conteúdo promocional** em templates de Utilidade ou Autenticação
- **Forneça exemplos claros** para todos os parâmetros
- **Evite linguagem vaga** ou potencialmente enganosa
- **Não inclua links encurtados** ou redirecionamentos

### 3. Otimização de Desempenho

- **Teste diferentes formatos**: Experimente diferentes combinações de componentes
- **Monitore as métricas**: Acompanhe taxas de entrega, leitura e resposta
- **Segmente adequadamente**: Envie templates relevantes para os destinatários certos
- **Respeite as preferências**: Inclua opções de cancelamento de inscrição em templates de marketing

## Limitações e Considerações

- **Limite de templates**: O número máximo de templates depende da verificação da empresa
  - Empresas não verificadas: 250 templates por conta
  - Empresas verificadas: 6.000 templates por conta
- **Tamanho do texto**: Limites de caracteres por componente
  - Cabeçalho de texto: 60 caracteres
  - Corpo: 1.024 caracteres
  - Rodapé: 60 caracteres
  - Botões: 20 caracteres por botão
- **Edição de templates**: Templates podem ser editados até 10 vezes por mês
- **Tempo de aprovação**: Geralmente 1-2 dias úteis
- **Rejeições**: Templates rejeitados podem ser editados e reenviados

## Solução de Problemas Comuns

### 1. Template Rejeitado

**Possíveis causas:**
- Conteúdo não corresponde à categoria selecionada
- Conteúdo viola as políticas do WhatsApp
- Exemplos de parâmetros inadequados ou ausentes
- Linguagem promocional em templates de utilidade

**Soluções:**
- Revise o motivo da rejeição
- Ajuste o conteúdo ou a categoria
- Forneça exemplos claros para todos os parâmetros
- Reenvie o template para aprovação

### 2. Erro ao Enviar Template

**Possíveis causas:**
- Template não aprovado
- Parâmetros incorretos ou ausentes
- Nome ou idioma do template incorretos

**Soluções:**
- Verifique o status do template
- Confirme se todos os parâmetros obrigatórios estão incluídos
- Verifique o nome e o idioma do template

### 3. Baixa Taxa de Entrega

**Possíveis causas:**
- Número de telefone incorreto
- Usuário bloqueou mensagens comerciais
- Problemas de qualidade da conta

**Soluções:**
- Verifique os números de telefone
- Melhore a qualidade do conteúdo
- Monitore e melhore as métricas de qualidade da conta

## Recursos Adicionais

- [Documentação oficial de templates](https://developers.facebook.com/docs/whatsapp/business-management-api/message-templates)
- [Políticas de negócios do WhatsApp](https://www.whatsapp.com/legal/business-policy/)
- [Guia de categorização de templates](https://developers.facebook.com/docs/whatsapp/updates-to-pricing/new-template-guidelines)
