# Deploy do WhatsApp API Assistant no Vercel

Este guia fornece instruções para fazer o deploy do WhatsApp API Assistant no Vercel, contornando o limite de 250 MB para funções serverless.

## Pré-requisitos

- Conta no Vercel
- Repositório Git com o código do projeto
- Chave de API OpenAI

## Preparação para o Deploy

### 1. Configuração dos Arquivos

O projeto já está configurado com os seguintes arquivos otimizados para o Vercel:

- `vercel.json`: Configurações do Vercel
- `.vercelignore`: Lista de arquivos e diretórios a serem ignorados
- `requirements-vercel.txt`: Dependências mínimas necessárias
- `api/index.py`: Ponto de entrada para o Vercel

### 2. Configuração das Variáveis de Ambiente

No dashboard do Vercel, adicione as seguintes variáveis de ambiente:

- `OPENAI_API_KEY`: Sua chave de API OpenAI
- `OPENAI_MODEL`: Modelo a ser utilizado (ex: gpt-4o-mini)

### 3. Deploy no Vercel

#### Opção 1: Deploy via CLI do Vercel

1. Instale a CLI do Vercel:
   ```
   npm install -g vercel
   ```

2. Faça login na sua conta:
   ```
   vercel login
   ```

3. Execute o comando de deploy na raiz do projeto:
   ```
   vercel --prod
   ```

#### Opção 2: Deploy via Dashboard do Vercel

1. Faça login no [Dashboard do Vercel](https://vercel.com/dashboard)
2. Clique em "New Project"
3. Importe seu repositório Git
4. Configure as variáveis de ambiente
5. Clique em "Deploy"

## Solução para o Erro de Tamanho

Se você encontrar o erro `A Serverless Function has exceeded the unzipped maximum size of 250 MB`, siga estas etapas:

1. Verifique se está usando o arquivo `requirements-vercel.txt` para as dependências:
   ```
   pip install -r requirements-vercel.txt
   ```

2. Certifique-se de que o arquivo `.vercelignore` está excluindo pacotes pesados:
   ```
   # Ignorar pacotes não utilizados no Vercel
   scikit-learn/
   numpy/
   pandas/
   matplotlib/
   scipy/
   spacy/
   nltk/
   tensorflow/
   torch/
   transformers/
   ```

3. Verifique se o arquivo `vercel.json` está configurado corretamente:
   ```json
   {
     "version": 2,
     "builds": [
       {
         "src": "api/index.py",
         "use": "@vercel/python",
         "config": {
           "maxLambdaSize": "15mb",
           "runtime": "python3.9"
         }
       }
     ],
     "routes": [
       {
         "src": "/(.*)",
         "dest": "api/index.py"
       }
     ],
     "functions": {
       "api/index.py": {
         "memory": 1024,
         "maxDuration": 10,
         "excludeFiles": "{.next,*.cache,node_modules,public,app,venv,__pycache__,*.pyc,*.pyo,*.pyd,tests,images,*.jpg,*.jpeg,*.png,*.gif}/**"
       }
     }
   }
   ```

## Testando a Aplicação

Após o deploy, você pode testar a API com:

```bash
curl -X POST https://seu-app.vercel.app/api/ask \
  -H "Content-Type: application/json" \
  -d '{"question":"Como integrar a API do WhatsApp?"}'
```

## Solução Alternativa: Vercel Edge Functions

Se as soluções acima não funcionarem, considere migrar para [Vercel Edge Functions](https://vercel.com/docs/functions/edge-functions), que têm menos limitações de tamanho.

## Recursos Adicionais

- [Documentação do Vercel Python](https://vercel.com/docs/functions/serverless-functions/runtimes/python)
- [Limites do Vercel](https://vercel.com/docs/concepts/limits/overview)
