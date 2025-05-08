# Mídia e Arquivos na API do WhatsApp Business

A API do WhatsApp Business permite o envio e recebimento de diversos tipos de mídia, enriquecendo a comunicação com seus clientes. Este guia detalha como trabalhar com imagens, documentos, áudio, vídeo e outros tipos de mídia.

## Tipos de Mídia Suportados

A API do WhatsApp Business suporta os seguintes tipos de mídia:

### 1. Imagens
- Formatos: JPG, JPEG, PNG
- Tamanho máximo: 5 MB
- Resolução recomendada: 800x800 pixels

### 2. Documentos
- Formatos: PDF, DOC, DOCX, XLS, XLSX, PPT, PPTX, TXT, RTF, ZIP
- Tamanho máximo: 100 MB

### 3. Áudio
- Formatos: AAC, MP4, MPEG, AMR, OGG (com codificação OPUS)
- Tamanho máximo: 16 MB
- Duração máxima: 16 minutos

### 4. Vídeo
- Formatos: MP4, 3GPP
- Codecs: H.264, MPEG4
- Tamanho máximo: 16 MB
- Duração máxima: 3 minutos

### 5. Adesivos (Stickers)
- Formato: WebP
- Tamanho máximo: 100 KB
- Dimensões: 512x512 pixels

## Envio de Mídia

Existem duas maneiras de enviar mídia através da API:

### 1. Usando URLs Públicas

Você pode enviar mídia referenciando uma URL pública acessível:

#### Exemplo: Envio de Imagem via URL

```json
{
  "messaging_product": "whatsapp",
  "recipient_type": "individual",
  "to": "5511999999999",
  "type": "image",
  "image": {
    "link": "https://www.exemplo.com.br/imagens/produto.jpg",
    "caption": "Nosso novo produto lançado esta semana!"
  }
}
```

#### Exemplo: Envio de Documento via URL

```json
{
  "messaging_product": "whatsapp",
  "recipient_type": "individual",
  "to": "5511999999999",
  "type": "document",
  "document": {
    "link": "https://www.exemplo.com.br/documentos/manual.pdf",
    "caption": "Manual do Usuário",
    "filename": "manual-do-usuario.pdf"
  }
}
```

#### Exemplo: Envio de Áudio via URL

```json
{
  "messaging_product": "whatsapp",
  "recipient_type": "individual",
  "to": "5511999999999",
  "type": "audio",
  "audio": {
    "link": "https://www.exemplo.com.br/audio/mensagem.mp3"
  }
}
```

#### Exemplo: Envio de Vídeo via URL

```json
{
  "messaging_product": "whatsapp",
  "recipient_type": "individual",
  "to": "5511999999999",
  "type": "video",
  "video": {
    "link": "https://www.exemplo.com.br/videos/demonstracao.mp4",
    "caption": "Veja como usar nosso produto"
  }
}
```

### 2. Usando IDs de Mídia (Upload Prévio)

Para maior segurança e confiabilidade, você pode fazer upload da mídia previamente e depois referenciá-la pelo ID:

#### Passo 1: Upload da Mídia

```http
POST https://graph.facebook.com/v17.0/PHONE_NUMBER_ID/media
Content-Type: multipart/form-data
Authorization: Bearer YOUR_ACCESS_TOKEN

--boundary
Content-Disposition: form-data; name="messaging_product"

whatsapp
--boundary
Content-Disposition: form-data; name="file"; filename="produto.jpg"
Content-Type: image/jpeg

[BINARY_DATA]
--boundary--
```

#### Passo 2: Receber o ID da Mídia

```json
{
  "id": "123456789012345"
}
```

#### Passo 3: Enviar Mensagem com o ID da Mídia

```json
{
  "messaging_product": "whatsapp",
  "recipient_type": "individual",
  "to": "5511999999999",
  "type": "image",
  "image": {
    "id": "123456789012345",
    "caption": "Nosso novo produto lançado esta semana!"
  }
}
```

## Recebimento de Mídia

Quando um usuário envia mídia para o seu número do WhatsApp Business, você recebe uma notificação em seu webhook:

### Exemplo: Notificação de Imagem Recebida

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
                "type": "image",
                "image": {
                  "id": "MEDIA_ID",
                  "mime_type": "image/jpeg",
                  "sha256": "HASH",
                  "caption": "CAPTION_TEXT"
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

## Download de Mídia Recebida

Para acessar a mídia enviada pelos usuários, você precisa seguir um processo de dois passos:

### Passo 1: Obter a URL da Mídia

```http
GET https://graph.facebook.com/v17.0/MEDIA_ID
Authorization: Bearer YOUR_ACCESS_TOKEN
```

Resposta:
```json
{
  "messaging_product": "whatsapp",
  "url": "https://lookaside.fbsbx.com/whatsapp_business/attachments/?mid=MEDIA_ID&...",
  "mime_type": "image/jpeg",
  "sha256": "HASH",
  "file_size": 123456,
  "id": "MEDIA_ID"
}
```

### Passo 2: Baixar a Mídia

```http
GET URL_FROM_PREVIOUS_RESPONSE
Authorization: Bearer YOUR_ACCESS_TOKEN
```

## Implementação em Código

### Node.js: Upload de Mídia

```javascript
const axios = require('axios');
const FormData = require('form-data');
const fs = require('fs');

async function uploadMedia(phoneNumberId, filePath, mimeType) {
  try {
    const formData = new FormData();
    formData.append('messaging_product', 'whatsapp');
    formData.append('file', fs.createReadStream(filePath), {
      contentType: mimeType,
    });

    const response = await axios.post(
      `https://graph.facebook.com/v17.0/${phoneNumberId}/media`,
      formData,
      {
        headers: {
          ...formData.getHeaders(),
          'Authorization': `Bearer ${process.env.WHATSAPP_TOKEN}`,
        },
      }
    );

    return response.data.id;
  } catch (error) {
    console.error('Erro ao fazer upload de mídia:', error.response?.data || error.message);
    throw error;
  }
}
```

### Node.js: Download de Mídia

```javascript
const axios = require('axios');
const fs = require('fs');
const path = require('path');

async function downloadMedia(mediaId, outputDir) {
  try {
    // Passo 1: Obter a URL da mídia
    const mediaInfoResponse = await axios.get(
      `https://graph.facebook.com/v17.0/${mediaId}`,
      {
        headers: {
          'Authorization': `Bearer ${process.env.WHATSAPP_TOKEN}`
        }
      }
    );
    
    const mediaUrl = mediaInfoResponse.data.url;
    const mimeType = mediaInfoResponse.data.mime_type;
    
    // Determinar a extensão do arquivo com base no MIME type
    const extension = mimeType.split('/')[1];
    const outputPath = path.join(outputDir, `${mediaId}.${extension}`);
    
    // Passo 2: Baixar a mídia
    const mediaResponse = await axios.get(mediaUrl, {
      headers: {
        'Authorization': `Bearer ${process.env.WHATSAPP_TOKEN}`
      },
      responseType: 'arraybuffer'
    });
    
    // Salvar o arquivo
    fs.writeFileSync(outputPath, Buffer.from(mediaResponse.data));
    
    return {
      path: outputPath,
      mimeType: mimeType
    };
  } catch (error) {
    console.error('Erro ao baixar mídia:', error.response?.data || error.message);
    throw error;
  }
}
```

### Python: Upload de Mídia

```python
import requests
import os

def upload_media(phone_number_id, file_path, mime_type):
    try:
        url = f"https://graph.facebook.com/v17.0/{phone_number_id}/media"
        
        headers = {
            "Authorization": f"Bearer {os.environ.get('WHATSAPP_TOKEN')}"
        }
        
        with open(file_path, 'rb') as file:
            files = {
                'file': (os.path.basename(file_path), file, mime_type)
            }
            
            data = {
                'messaging_product': 'whatsapp'
            }
            
            response = requests.post(url, headers=headers, data=data, files=files)
            response.raise_for_status()
            
            return response.json()['id']
    except Exception as e:
        print(f"Erro ao fazer upload de mídia: {str(e)}")
        raise
```

### Python: Download de Mídia

```python
import requests
import os
import mimetypes

def download_media(media_id, output_dir):
    try:
        # Passo 1: Obter a URL da mídia
        url = f"https://graph.facebook.com/v17.0/{media_id}"
        
        headers = {
            "Authorization": f"Bearer {os.environ.get('WHATSAPP_TOKEN')}"
        }
        
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        
        media_info = response.json()
        media_url = media_info['url']
        mime_type = media_info['mime_type']
        
        # Determinar a extensão do arquivo com base no MIME type
        extension = mimetypes.guess_extension(mime_type) or ''
        output_path = os.path.join(output_dir, f"{media_id}{extension}")
        
        # Passo 2: Baixar a mídia
        media_response = requests.get(media_url, headers=headers)
        media_response.raise_for_status()
        
        # Salvar o arquivo
        with open(output_path, 'wb') as f:
            f.write(media_response.content)
        
        return {
            'path': output_path,
            'mime_type': mime_type
        }
    except Exception as e:
        print(f"Erro ao baixar mídia: {str(e)}")
        raise
```

## Melhores Práticas

### 1. Upload e Armazenamento

- **Prefira upload prévio**: Para mídia usada frequentemente, faça upload uma vez e reutilize o ID
- **Armazene IDs**: Mantenha um registro dos IDs de mídia para reutilização
- **Otimize arquivos**: Comprima imagens e vídeos antes do upload
- **Verifique tamanhos**: Respeite os limites de tamanho para cada tipo de mídia

### 2. Segurança e Privacidade

- **Valide arquivos**: Verifique o tipo e conteúdo dos arquivos antes de processá-los
- **Escaneie para malware**: Implemente verificações de segurança para arquivos recebidos
- **Armazenamento seguro**: Armazene mídia em locais seguros e com acesso controlado
- **Política de retenção**: Implemente uma política clara para retenção e exclusão de mídia

### 3. Experiência do Usuário

- **Adicione legendas**: Use o campo `caption` para fornecer contexto
- **Otimize para mobile**: Considere como a mídia será exibida em dispositivos móveis
- **Forneça alternativas**: Ofereça opções de texto para usuários com conexões lentas
- **Respeite o contexto**: Envie mídia relevante para a conversa atual

## Limitações e Considerações

- **Tempo de vida da mídia**: A mídia recebida está disponível para download por apenas 30 dias
- **Cache de mídia**: A API armazena em cache mídia enviada via URL por 10 minutos
- **Ordem de entrega**: A ordem de entrega de múltiplas mensagens de mídia não é garantida
- **Compatibilidade**: Nem todos os dispositivos suportam todos os formatos de mídia
- **Qualidade**: O WhatsApp pode comprimir imagens e vídeos para otimizar a entrega

## Solução de Problemas Comuns

### 1. Erro "Media upload error"

**Possíveis causas:**
- URL da mídia não é acessível publicamente
- Formato de arquivo não suportado
- Arquivo excede o tamanho máximo

**Soluções:**
- Verifique se a URL é acessível sem autenticação
- Confirme se o formato do arquivo é suportado
- Reduza o tamanho do arquivo

### 2. Erro "Media download failed"

**Possíveis causas:**
- ID de mídia inválido ou expirado
- Token de acesso inválido
- Mídia não está mais disponível (após 30 dias)

**Soluções:**
- Verifique o ID da mídia
- Confirme se o token de acesso é válido
- Baixe e armazene a mídia o mais rápido possível após recebê-la

### 3. Mídia não é exibida corretamente

**Possíveis causas:**
- Formato não suportado pelo dispositivo do usuário
- Resolução ou codificação inadequada
- Problemas de conexão do usuário

**Soluções:**
- Use formatos amplamente suportados (JPG para imagens, MP4 para vídeos)
- Otimize a mídia para dispositivos móveis
- Forneça alternativas de texto quando apropriado

## Recursos Adicionais

- [Documentação oficial de mídia](https://developers.facebook.com/docs/whatsapp/cloud-api/reference/media)
- [Guia de otimização de mídia](https://developers.facebook.com/docs/whatsapp/guides/media-best-practices)
- [Políticas de conteúdo do WhatsApp](https://www.whatsapp.com/legal/commerce-policy)
