# Mensagens Interativas na API do WhatsApp Business

As mensagens interativas permitem criar experiências de conversação mais ricas e engajadoras no WhatsApp, facilitando a interação dos usuários com sua empresa. Este guia detalha os diferentes tipos de mensagens interativas disponíveis, como implementá-las e as melhores práticas para seu uso.

## Visão Geral

As mensagens interativas na API do WhatsApp Business incluem elementos como botões, listas e outros componentes que permitem aos usuários interagir com sua empresa de forma mais intuitiva, sem precisar digitar respostas completas.

## Tipos de Mensagens Interativas

### 1. Botões de Resposta Rápida

Os botões de resposta rápida permitem que os usuários respondam a uma mensagem com um simples toque, sem precisar digitar.

#### Características:
- Até 3 botões por mensagem
- Cada botão pode ter até 20 caracteres
- Quando o usuário toca em um botão, o texto do botão é enviado como resposta

#### Exemplo de Implementação:

```json
{
  "messaging_product": "whatsapp",
  "recipient_type": "individual",
  "to": "5511999999999",
  "type": "interactive",
  "interactive": {
    "type": "button",
    "body": {
      "text": "Você gostaria de confirmar seu agendamento para amanhã às 14h?"
    },
    "action": {
      "buttons": [
        {
          "type": "reply",
          "reply": {
            "id": "confirm_appointment",
            "title": "Confirmar"
          }
        },
        {
          "type": "reply",
          "reply": {
            "id": "reschedule_appointment",
            "title": "Reagendar"
          }
        },
        {
          "type": "reply",
          "reply": {
            "id": "cancel_appointment",
            "title": "Cancelar"
          }
        }
      ]
    }
  }
}
```

### 2. Listas

As listas permitem apresentar múltiplas opções organizadas em seções, facilitando a escolha entre várias alternativas.

#### Características:
- Até 10 seções
- Até 10 itens por seção
- Total máximo de 100 itens
- Cada item tem título, ID opcional e descrição opcional

#### Exemplo de Implementação:

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
      "text": "Menu de Opções"
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
          "title": "Atendimento",
          "rows": [
            {
              "id": "support_general",
              "title": "Suporte Geral",
              "description": "Dúvidas sobre produtos e serviços"
            },
            {
              "id": "support_technical",
              "title": "Suporte Técnico",
              "description": "Problemas técnicos com produtos"
            }
          ]
        },
        {
          "title": "Vendas",
          "rows": [
            {
              "id": "sales_new",
              "title": "Novos Produtos",
              "description": "Informações sobre lançamentos"
            },
            {
              "id": "sales_promotions",
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

### 3. Botões de URL (CTA URL)

Os botões de URL permitem direcionar os usuários para um site externo diretamente da conversa.

#### Características:
- Um único botão por mensagem
- O botão abre um link em um navegador
- Útil para direcionar usuários para páginas de produtos, formulários, etc.

#### Exemplo de Implementação:

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

### 4. Fluxos Interativos (Flows)

Os fluxos são experiências interativas mais complexas que permitem aos usuários realizar ações como agendar compromissos, navegar por catálogos ou preencher formulários.

#### Características:
- Experiências mais ricas e estruturadas
- Podem incluir múltiplas etapas
- Suportam diversos tipos de entrada (texto, seleção, etc.)
- Requerem configuração prévia no WhatsApp Business Manager

#### Exemplo de Implementação:

```json
{
  "messaging_product": "whatsapp",
  "recipient_type": "individual",
  "to": "5511999999999",
  "type": "interactive",
  "interactive": {
    "type": "flow",
    "header": {
      "type": "text",
      "text": "Agendamento de Serviço"
    },
    "body": {
      "text": "Agende seu serviço de forma rápida e fácil."
    },
    "footer": {
      "text": "Atendimento 24h"
    },
    "action": {
      "name": "flow",
      "parameters": {
        "flow_token": "flow_token_value",
        "flow_id": "flow_id_value",
        "flow_message_version": "3",
        "flow_token_refresh": false,
        "flow_action": "navigate"
      }
    }
  }
}
```

### 5. Solicitação de Localização

Este tipo de mensagem exibe um botão que, quando tocado, permite ao usuário compartilhar sua localização atual.

#### Características:
- Facilita o compartilhamento de localização
- Útil para serviços de entrega, agendamentos locais, etc.

#### Exemplo de Implementação:

```json
{
  "messaging_product": "whatsapp",
  "recipient_type": "individual",
  "to": "5511999999999",
  "type": "interactive",
  "interactive": {
    "type": "location_request_message",
    "body": {
      "text": "Para confirmarmos a entrega, precisamos do seu endereço atual."
    },
    "action": {
      "name": "send_location"
    }
  }
}
```

## Processamento de Respostas Interativas

Quando um usuário interage com uma mensagem interativa, você receberá uma notificação em seu webhook com os detalhes da interação.

### 1. Resposta de Botão

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
              "display_phone_number": "PHONE_NUMBER",
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
                "type": "interactive",
                "interactive": {
                  "type": "button_reply",
                  "button_reply": {
                    "id": "confirm_appointment",
                    "title": "Confirmar"
                  }
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

### 2. Resposta de Lista

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
              "display_phone_number": "PHONE_NUMBER",
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
                "type": "interactive",
                "interactive": {
                  "type": "list_reply",
                  "list_reply": {
                    "id": "support_technical",
                    "title": "Suporte Técnico",
                    "description": "Problemas técnicos com produtos"
                  }
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

## Processamento em Código

### Node.js (Express)

```javascript
// Função para processar mensagens interativas
async function handleInteractiveMessage(phoneNumberId, from, interactive, messageId) {
  console.log(`Mensagem interativa recebida de ${from}`);
  
  const interactiveType = interactive.type;
  
  if (interactiveType === 'button_reply') {
    const buttonId = interactive.button_reply.id;
    const buttonTitle = interactive.button_reply.title;
    
    console.log(`Usuário clicou no botão: ${buttonTitle} (ID: ${buttonId})`);
    
    // Processar a resposta do botão
    switch (buttonId) {
      case 'confirm_appointment':
        await confirmAppointment(phoneNumberId, from);
        break;
      case 'reschedule_appointment':
        await sendRescheduleOptions(phoneNumberId, from);
        break;
      case 'cancel_appointment':
        await cancelAppointment(phoneNumberId, from);
        break;
      default:
        await sendGenericResponse(phoneNumberId, from);
    }
  } 
  else if (interactiveType === 'list_reply') {
    const listId = interactive.list_reply.id;
    const listTitle = interactive.list_reply.title;
    
    console.log(`Usuário selecionou da lista: ${listTitle} (ID: ${listId})`);
    
    // Processar a seleção da lista
    if (listId.startsWith('support_')) {
      await handleSupportRequest(phoneNumberId, from, listId);
    } else if (listId.startsWith('sales_')) {
      await handleSalesRequest(phoneNumberId, from, listId);
    } else {
      await sendGenericResponse(phoneNumberId, from);
    }
  }
}
```

### Python (Flask)

```python
# Função para processar mensagens interativas
async def handle_interactive_message(phone_number_id, from_number, interactive, message_id):
    print(f"Mensagem interativa recebida de {from_number}")
    
    interactive_type = interactive.get('type')
    
    if interactive_type == 'button_reply':
        button_id = interactive['button_reply']['id']
        button_title = interactive['button_reply']['title']
        
        print(f"Usuário clicou no botão: {button_title} (ID: {button_id})")
        
        # Processar a resposta do botão
        if button_id == 'confirm_appointment':
            await confirm_appointment(phone_number_id, from_number)
        elif button_id == 'reschedule_appointment':
            await send_reschedule_options(phone_number_id, from_number)
        elif button_id == 'cancel_appointment':
            await cancel_appointment(phone_number_id, from_number)
        else:
            await send_generic_response(phone_number_id, from_number)
    
    elif interactive_type == 'list_reply':
        list_id = interactive['list_reply']['id']
        list_title = interactive['list_reply']['title']
        
        print(f"Usuário selecionou da lista: {list_title} (ID: {list_id})")
        
        # Processar a seleção da lista
        if list_id.startswith('support_'):
            await handle_support_request(phone_number_id, from_number, list_id)
        elif list_id.startswith('sales_'):
            await handle_sales_request(phone_number_id, from_number, list_id)
        else:
            await send_generic_response(phone_number_id, from_number)
```

## Melhores Práticas

### 1. Design de Interação

- **Mantenha simples**: Use textos claros e concisos
- **Limite as opções**: Não sobrecarregue o usuário com muitas escolhas
- **Organize logicamente**: Agrupe opções relacionadas em seções
- **Use descrições informativas**: Ajude o usuário a entender cada opção
- **Forneça feedback**: Confirme as ações do usuário após cada interação

### 2. Usabilidade

- **Nomes de botões intuitivos**: Use verbos de ação claros
- **Considere o contexto**: Adapte as opções ao contexto da conversa
- **Ofereça saídas**: Sempre permita que o usuário volte ou cancele
- **Teste em dispositivos reais**: Verifique como a interface aparece em diferentes telefones

### 3. Fluxo de Conversação

- **Planeje o fluxo completo**: Mapeie todas as possíveis interações
- **Mantenha o contexto**: Lembre-se das escolhas anteriores do usuário
- **Limite a profundidade**: Evite mais de 3-4 níveis de interação
- **Ofereça ajuda**: Inclua opções para falar com um atendente humano

## Limitações e Considerações

- **Compatibilidade**: Nem todos os recursos estão disponíveis em todas as versões do WhatsApp
- **Expiração**: Mensagens interativas expiram após 24 horas
- **Janela de serviço**: Só podem ser enviadas dentro da janela de 24 horas, a menos que sejam parte de um template
- **Limitações visuais**: O WhatsApp tem restrições de formatação e estilo
- **Tamanho do texto**: Existem limites de caracteres para cada componente

## Casos de Uso Comuns

### 1. Atendimento ao Cliente

- **Triagem inicial**: Categorizar o problema do cliente
- **FAQ interativo**: Permitir que o cliente navegue por perguntas frequentes
- **Escalação**: Oferecer opção para falar com um atendente humano

### 2. Vendas e Marketing

- **Catálogo de produtos**: Permitir que o cliente navegue por categorias
- **Qualificação de leads**: Fazer perguntas para qualificar o interesse
- **Agendamento de demonstrações**: Permitir que o cliente escolha horários disponíveis

### 3. Operações

- **Confirmação de pedidos**: Permitir que o cliente confirme ou modifique pedidos
- **Atualizações de status**: Oferecer opções para rastrear ou modificar entregas
- **Feedback**: Coletar avaliações e comentários de forma estruturada

## Recursos Adicionais

- [Documentação oficial de mensagens interativas](https://developers.facebook.com/docs/whatsapp/cloud-api/guides/send-messages#interactive-messages)
- [Guia de design para WhatsApp Business](https://developers.facebook.com/docs/whatsapp/guides/design)
- [Exemplos de implementação](https://developers.facebook.com/docs/whatsapp/cloud-api/reference/messages)
