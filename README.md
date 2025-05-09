# Chat Especialista API WhatsApp Business - Instruções para Execução Local

Este projeto implementa um Chat Especialista sobre a API Oficial do WhatsApp Business, utilizando Flask para o backend e a API Gemini como motor de IA para as respostas. Abaixo estão as instruções para configurar e executar a aplicação localmente.

## Pré-requisitos

-   Python 3.9 ou superior.
-   `pip` (gerenciador de pacotes Python).
-   Um navegador web moderno.

## Configuração do Ambiente

1.  **Clone ou Baixe o Projeto:**
    *   Se você recebeu os arquivos como um `.zip`, extraia-o para um diretório de sua preferência.

2.  **Crie e Ative um Ambiente Virtual (Recomendado):**
    *   Abra o terminal ou prompt de comando no diretório raiz do projeto (`whatsapp_expert_chat`).
    *   Execute os seguintes comandos:
        ```bash
        python3 -m venv venv
        # No Windows:
        # venv\Scripts\activate
        # No macOS/Linux:
        # source venv/bin/activate
        ```

3.  **Instale as Dependências:**
    *   Com o ambiente virtual ativado, instale as bibliotecas Python necessárias:
        ```bash
        pip install -r requirements.txt
        ```

4.  **Configure as Variáveis de Ambiente:**
    *   Crie um arquivo `.env` na raiz do projeto com as seguintes variáveis:
        ```
        # Configurações da API OpenAI
        OPENAI_API_KEY=sua_chave_api_aqui
        OPENAI_MODEL=gpt-4o-mini

        # Configurações do servidor Flask
        FLASK_ENV=development
        PORT=5000
        ```
    *   Substitua `sua_chave_api_aqui` pela sua chave da API OpenAI.
    *   **IMPORTANTE:** Nunca compartilhe ou cometa sua chave da API no controle de versão. O arquivo `.env` já está incluído no `.gitignore`.

## Executando a Aplicação

1.  **Navegue até o Diretório do Projeto:**
    *   Certifique-se de que você está no diretório raiz do projeto `whatsapp_expert_chat` no seu terminal e que o ambiente virtual está ativado.

2.  **Inicie o Servidor Flask:**
    *   Execute o seguinte comando:
        ```bash
        python src/main.py
        ```

3.  **Acesse a Aplicação no Navegador:**
    *   Após iniciar o servidor, você verá mensagens no terminal indicando que ele está rodando, geralmente em `http://127.0.0.1:5000/` ou `http://localhost:5000/`.
    *   Abra seu navegador web e acesse o endereço fornecido.

## Estrutura do Projeto

```
whatsapp_expert_chat/
├── venv/                   # Ambiente virtual Python
├── src/
│   ├── knowledge_base/     # Arquivos Markdown com a base de conhecimento
│   │   ├── base_conhecimento_whatsapp_api.md
│   │   └── estrategias_whatsapp_api.md
│   ├── static/             # Arquivos estáticos (CSS, JavaScript)
│   │   ├── script.js
│   │   └── style.css
│   ├── templates/          # Templates HTML
│   │   └── index.html
│   └── main.py             # Lógica principal da aplicação Flask e integração Gemini
└── requirements.txt        # Dependências Python
```

## Como Usar o Chat

1.  Abra a aplicação no seu navegador.
2.  Digite sua pergunta sobre a API do WhatsApp Business no campo de texto na parte inferior da tela.
3.  Clique no botão "Enviar" ou pressione Enter.
4.  Aguarde a resposta do assistente.

## Solução de Problemas Comuns

-   **`ModuleNotFoundError`:** Certifique-se de que o ambiente virtual está ativado e que você executou `pip install -r requirements.txt` para instalar todas as dependências.
-   **Erro ao conectar à API Gemini:** Verifique sua conexão com a internet e se a chave da API Gemini está configurada corretamente (seja como variável de ambiente ou no código, se você optou por essa via menos segura para teste).
-   **Porta 5000 já em uso:** Se você receber um erro indicando que a porta 5000 já está em uso, pode ser que outra aplicação (ou uma instância anterior desta) esteja utilizando essa porta. Você pode tentar parar o processo que está usando a porta ou modificar o arquivo `src/main.py` para usar uma porta diferente (ex: `app.run(host="0.0.0.0", port=5001)`).

Se encontrar outros problemas, verifique as mensagens de erro no terminal onde o servidor Flask está rodando para obter mais detalhes.

## Implantação em Produção

Este projeto está configurado para uma implantação dividida:
- **Frontend estático**: Hospedado no Vercel
- **Backend completo**: Hospedado no Render usando Docker

### Implantação no Vercel (Frontend)

O frontend estático está configurado para ser implantado no Vercel:

1. **Configuração Automática**:
   * O arquivo `vercel.json` já está configurado para implantação estática.
   * O arquivo `index.html` contém uma página de redirecionamento para o backend.

2. **Passos para Implantação**:
   * Conecte seu repositório GitHub ao Vercel.
   * O Vercel detectará automaticamente a configuração e implantará o frontend.
   * Não é necessário configurar variáveis de ambiente para o frontend.

### Implantação no Render (Backend)

O backend completo está configurado para ser implantado no Render usando Docker:

1. **Usando o arquivo render.yaml**:
   * O projeto inclui um arquivo `render.yaml` para configuração automática.
   * No painel do Render, selecione "Blueprint" e conecte seu repositório.
   * O Render detectará o arquivo `render.yaml` e configurará o serviço automaticamente.

2. **Configuração Manual**:
   * Conecte seu repositório GitHub ao Render.
   * Selecione "Web Service" e escolha "Docker" como ambiente.
   * Configure as variáveis de ambiente necessárias:
     - OPENAI_API_KEY
     - OPENAI_MODEL
     - SUPABASE_URL
     - SUPABASE_KEY
     - SUPABASE_SERVICE_KEY
     - SECRET_KEY

3. **Usando Docker Localmente**:
   * Para testar localmente antes de implantar:
     ```bash
     docker build -t whatsapp-api-assistant .
     docker run -p 8080:8080 --env-file .env whatsapp-api-assistant
     ```

### Considerações de Segurança

* Nunca armazene chaves de API diretamente no código.
* Use variáveis de ambiente para todas as credenciais.
* Configure HTTPS para proteger a comunicação (o Render e o Vercel já fazem isso automaticamente).
* O sistema já inclui autenticação de usuários usando Supabase.

Para mais informações sobre implantação, consulte a documentação do Flask e do Gunicorn.
