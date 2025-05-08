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

4.  **Configure a Chave da API Gemini:**
    *   Você precisará de uma chave da API Gemini. A chave fornecida durante o desenvolvimento foi `AIzaSyC--ZpEAGpmeC55Bi1lWHzdTfn56KRW7OA`.
    *   A aplicação tentará ler a chave da variável de ambiente `GEMINI_API_KEY`. Configure esta variável de ambiente no seu sistema:
        *   **No macOS/Linux (temporário para a sessão do terminal):**
            ```bash
            export GEMINI_API_KEY="SUA_CHAVE_API_AQUI"
            ```
        *   **No Windows (temporário para a sessão do prompt de comando):**
            ```bash
            set GEMINI_API_KEY=SUA_CHAVE_API_AQUI
            ```
        *   Para configuração permanente, consulte a documentação do seu sistema operacional sobre como definir variáveis de ambiente.
    *   Alternativamente, se você não configurar a variável de ambiente, a aplicação usará a chave `AIzaSyC--ZpEAGpmeC55Bi1lWHzdTfn56KRW7OA` que está como fallback no código (`src/main.py`). **Para uso em produção ou se a chave fornecida for sensível, é altamente recomendável usar variáveis de ambiente.**

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

