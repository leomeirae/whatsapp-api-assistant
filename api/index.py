from http.server import BaseHTTPRequestHandler
import json

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        """Handler para requisições GET"""
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

        # Página inicial
        if self.path == '/' or self.path == '':
            html = self.get_index_html()
        # Página da calculadora
        elif self.path == '/calculadora':
            html = self.get_calculadora_html()
        # Página não encontrada
        else:
            self.send_response(404)
            html = "Página não encontrada"

        self.wfile.write(html.encode())
        return

    def do_POST(self):
        """Handler para requisições POST"""
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()

        # Rota para processar perguntas
        if self.path == '/ask':
            # Ler o corpo da requisição
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)

            try:
                # Processar a pergunta
                data = json.loads(post_data.decode())
                question = data.get('question', '')

                if not question:
                    response = {'error': 'Nenhuma pergunta fornecida.'}
                else:
                    # Resposta temporária
                    response = {
                        'answer': 'Esta é uma resposta de teste do servidor Vercel. A integração com a API OpenAI será implementada em breve.'
                    }
            except Exception as e:
                response = {'error': f'Erro ao processar a pergunta: {str(e)}'}

            self.wfile.write(json.dumps(response).encode())
        else:
            self.send_response(404)
            self.wfile.write(json.dumps({'error': 'Endpoint não encontrado'}).encode())

        return

    def get_index_html(self):
        """Retorna o HTML da página inicial"""
        return """
        <!DOCTYPE html>
        <html>
        <head>
            <title>WhatsApp API Assistant</title>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <style>
                body { font-family: Arial, sans-serif; margin: 0; padding: 20px; line-height: 1.6; }
                .container { max-width: 800px; margin: 0 auto; padding: 20px; }
                h1 { color: #128C7E; }
                .chat-container { border: 1px solid #ddd; border-radius: 8px; padding: 20px; margin-top: 20px; }
                .message { margin-bottom: 10px; }
                .user-message { background-color: #DCF8C6; padding: 10px; border-radius: 8px; margin-left: 20%; }
                .bot-message { background-color: #F5F5F5; padding: 10px; border-radius: 8px; margin-right: 20%; }
                input[type="text"] { width: 80%; padding: 10px; border: 1px solid #ddd; border-radius: 4px; }
                button { background-color: #128C7E; color: white; border: none; padding: 10px 15px; border-radius: 4px; cursor: pointer; }
                button:hover { background-color: #075E54; }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>Assistente API do WhatsApp Business</h1>
                <p>Pergunte sobre a API, estratégias, custos e mais!</p>

                <div class="chat-container" id="chat">
                    <div class="message bot-message">
                        Olá! Sou o assistente especializado em API do WhatsApp Business. Como posso te ajudar hoje?
                    </div>
                </div>

                <div style="margin-top: 20px; display: flex;">
                    <input type="text" id="question" placeholder="Digite sua pergunta aqui...">
                    <button onclick="askQuestion()">Enviar</button>
                </div>
            </div>

            <script>
                function askQuestion() {
                    const question = document.getElementById('question').value;
                    if (!question) return;

                    // Adicionar mensagem do usuário
                    const userDiv = document.createElement('div');
                    userDiv.className = 'message user-message';
                    userDiv.textContent = question;
                    document.getElementById('chat').appendChild(userDiv);

                    // Limpar campo de entrada
                    document.getElementById('question').value = '';

                    // Fazer solicitação para a API
                    fetch('/ask', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                        },
                        body: JSON.stringify({ question: question }),
                    })
                    .then(response => response.json())
                    .then(data => {
                        // Adicionar resposta do assistente
                        const botDiv = document.createElement('div');
                        botDiv.className = 'message bot-message';
                        botDiv.textContent = data.answer || data.error || 'Desculpe, ocorreu um erro ao processar sua pergunta.';
                        document.getElementById('chat').appendChild(botDiv);
                    })
                    .catch(error => {
                        // Adicionar mensagem de erro
                        const errorDiv = document.createElement('div');
                        errorDiv.className = 'message bot-message';
                        errorDiv.textContent = 'Desculpe, ocorreu um erro: ' + error;
                        document.getElementById('chat').appendChild(errorDiv);
                    });
                }

                // Permitir enviar com Enter
                document.getElementById('question').addEventListener('keypress', function(e) {
                    if (e.key === 'Enter') {
                        askQuestion();
                    }
                });
            </script>
        </body>
        </html>
        """

    def get_calculadora_html(self):
        """Retorna o HTML da página da calculadora"""
        return """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Calculadora de Preços - WhatsApp API</title>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <style>
                body { font-family: Arial, sans-serif; margin: 0; padding: 20px; line-height: 1.6; }
                .container { max-width: 800px; margin: 0 auto; padding: 20px; }
                h1 { color: #128C7E; }
                .calculator { border: 1px solid #ddd; border-radius: 8px; padding: 20px; margin-top: 20px; }
                label { display: block; margin-top: 10px; font-weight: bold; }
                input, select { width: 100%; padding: 8px; margin-top: 5px; border: 1px solid #ddd; border-radius: 4px; }
                button { background-color: #128C7E; color: white; border: none; padding: 10px 15px; border-radius: 4px; cursor: pointer; margin-top: 20px; }
                button:hover { background-color: #075E54; }
                .result { margin-top: 20px; padding: 15px; background-color: #F5F5F5; border-radius: 8px; display: none; }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>Calculadora de Preços da API do WhatsApp</h1>
                <p>Estime os custos de uso da API do WhatsApp Business para sua empresa.</p>

                <div class="calculator">
                    <label for="conversations">Número estimado de conversas por mês:</label>
                    <input type="number" id="conversations" min="0" value="1000">

                    <label for="region">Região principal dos clientes:</label>
                    <select id="region">
                        <option value="br">Brasil</option>
                        <option value="us">Estados Unidos</option>
                        <option value="eu">Europa</option>
                        <option value="asia">Ásia</option>
                        <option value="other">Outras regiões</option>
                    </select>

                    <label for="businessType">Tipo de negócio:</label>
                    <select id="businessType">
                        <option value="ecommerce">E-commerce</option>
                        <option value="service">Serviços</option>
                        <option value="support">Suporte ao cliente</option>
                        <option value="marketing">Marketing</option>
                        <option value="other">Outro</option>
                    </select>

                    <button onclick="calculateCost()">Calcular Custo Estimado</button>
                </div>

                <div class="result" id="result">
                    <h2>Custo Estimado Mensal</h2>
                    <p id="costResult"></p>
                    <p id="disclaimer">Nota: Esta é apenas uma estimativa. Os preços reais podem variar de acordo com a política de preços da Meta e o uso específico da API.</p>
                </div>
            </div>

            <script>
                function calculateCost() {
                    const conversations = parseInt(document.getElementById('conversations').value);
                    const region = document.getElementById('region').value;
                    const businessType = document.getElementById('businessType').value;

                    // Preços base por região (em USD por 1000 conversas)
                    const basePrices = {
                        'br': 0.0315,
                        'us': 0.0160,
                        'eu': 0.0147,
                        'asia': 0.0172,
                        'other': 0.0200
                    };

                    // Multiplicadores por tipo de negócio
                    const businessMultipliers = {
                        'ecommerce': 1.0,
                        'service': 0.9,
                        'support': 1.1,
                        'marketing': 1.2,
                        'other': 1.0
                    };

                    // Cálculo do custo
                    const basePrice = basePrices[region];
                    const multiplier = businessMultipliers[businessType];
                    const cost = (conversations / 1000) * basePrice * multiplier;

                    // Exibir resultado
                    document.getElementById('costResult').textContent = `$${cost.toFixed(2)} USD por mês para aproximadamente ${conversations} conversas`;
                    document.getElementById('result').style.display = 'block';
                }
            </script>
        </body>
        </html>
        """
