document.addEventListener('DOMContentLoaded', function() {
    // Definição das taxas em dólares
    const rates = {
        marketing: 0.0625,
        utility: 0.008,
        auth: 0.0315
    };

    // Taxa de câmbio do dólar para real (atualizada diariamente)
    let exchangeRate = 5.50; // Valor padrão

    // Tentar obter a taxa de câmbio atual via API
    fetch('https://open.er-api.com/v6/latest/USD')
        .then(response => response.json())
        .then(data => {
            if (data.rates && data.rates.BRL) {
                exchangeRate = data.rates.BRL;
                console.log('Taxa de câmbio atualizada: $1 = R$' + exchangeRate.toFixed(2));
                updateAllTotals(); // Atualiza todos os totais com a nova taxa
            }
        })
        .catch(error => {
            console.error('Erro ao obter taxa de câmbio:', error);
        });

    // Elementos da calculadora
    const elements = {
        marketing: {
            slider: document.getElementById('marketing-slider'),
            input: document.getElementById('marketing-input'),
            total: document.getElementById('marketing-total'),
            decreaseBtn: document.querySelector('.decrease[data-type="marketing"]'),
            increaseBtn: document.querySelector('.increase[data-type="marketing"]')
        },
        utility: {
            slider: document.getElementById('utility-slider'),
            input: document.getElementById('utility-input'),
            total: document.getElementById('utility-total'),
            decreaseBtn: document.querySelector('.decrease[data-type="utility"]'),
            increaseBtn: document.querySelector('.increase[data-type="utility"]')
        },
        auth: {
            slider: document.getElementById('auth-slider'),
            input: document.getElementById('auth-input'),
            total: document.getElementById('auth-total'),
            decreaseBtn: document.querySelector('.decrease[data-type="auth"]'),
            increaseBtn: document.querySelector('.increase[data-type="auth"]')
        },
        grandTotal: document.getElementById('grand-total'),
        exportBtn: document.getElementById('export-btn')
    };

    // Função para calcular o total para um tipo específico
    function calculateTotal(type) {
        const quantity = parseInt(elements[type].input.value) || 0;
        const rateInDollars = rates[type];
        const totalInReais = quantity * rateInDollars * exchangeRate;
        return totalInReais;
    }

    // Função para atualizar o total exibido para um tipo específico
    function updateTotal(type) {
        const total = calculateTotal(type);
        elements[type].total.textContent = total.toFixed(2).replace('.', ',');
        updateGrandTotal();
    }

    // Função para atualizar todos os totais (usado quando a taxa de câmbio é atualizada)
    function updateAllTotals() {
        updateTotal('marketing');
        updateTotal('utility');
        updateTotal('auth');
    }

    // Função para atualizar o total geral
    function updateGrandTotal() {
        const marketingTotal = calculateTotal('marketing');
        const utilityTotal = calculateTotal('utility');
        const authTotal = calculateTotal('auth');

        const grandTotal = marketingTotal + utilityTotal + authTotal;
        elements.grandTotal.textContent = grandTotal.toFixed(2).replace('.', ',');
    }

    // Função para sincronizar slider e input
    function syncSliderAndInput(type, value) {
        elements[type].slider.value = value;
        elements[type].input.value = value;
        updateTotal(type);
    }

    // Adicionar event listeners para sliders
    Object.keys(elements).forEach(type => {
        if (type !== 'grandTotal' && type !== 'exportBtn' && type !== 'contactBtn') {
            // Event listener para o slider
            elements[type].slider.addEventListener('input', function() {
                syncSliderAndInput(type, this.value);
            });

            // Event listener para o input numérico
            elements[type].input.addEventListener('input', function() {
                let value = parseInt(this.value) || 0;

                // Limitar o valor máximo
                if (value > 10000) {
                    value = 10000;
                    this.value = 10000;
                }

                syncSliderAndInput(type, value);
            });

            // Event listeners para os botões de aumento e diminuição
            elements[type].decreaseBtn.addEventListener('click', function() {
                let currentValue = parseInt(elements[type].input.value) || 0;
                if (currentValue > 0) {
                    syncSliderAndInput(type, currentValue - 1);
                }
            });

            elements[type].increaseBtn.addEventListener('click', function() {
                let currentValue = parseInt(elements[type].input.value) || 0;
                if (currentValue < 10000) {
                    syncSliderAndInput(type, currentValue + 1);
                }
            });
        }
    });

    // Função para exportar o orçamento como PDF
    elements.exportBtn.addEventListener('click', function() {
        // Verificar se a biblioteca jsPDF está disponível
        if (typeof window.jspdf === 'undefined') {
            alert('A biblioteca de geração de PDF não está disponível. Por favor, tente novamente mais tarde.');
            return;
        }

        const { jsPDF } = window.jspdf;
        const doc = new jsPDF();

        // Adicionar título
        doc.setFontSize(20);
        doc.setTextColor(7, 94, 84); // Cor verde escura do WhatsApp
        doc.text('Orçamento API WhatsApp Business', 105, 20, { align: 'center' });

        // Adicionar data
        const today = new Date();
        const dateStr = today.toLocaleDateString('pt-BR');
        doc.setFontSize(10);
        doc.setTextColor(100, 100, 100);
        doc.text(`Data: ${dateStr}`, 20, 30);

        // Adicionar taxa de câmbio
        doc.text(`Taxa de câmbio: $1 = R$${exchangeRate.toFixed(2)}`, 20, 40);

        // Adicionar detalhes do orçamento
        doc.setFontSize(12);
        doc.setTextColor(0, 0, 0);

        let y = 60;

        // Cabeçalho da tabela
        doc.setFont(undefined, 'bold');
        doc.text('Tipo de Conversa', 20, y);
        doc.text('Quantidade', 100, y);
        doc.text('Valor (R$)', 150, y);
        doc.setFont(undefined, 'normal');

        y += 10;

        // Marketing
        const marketingQty = parseInt(elements.marketing.input.value) || 0;
        const marketingTotal = calculateTotal('marketing');
        doc.text('Marketing', 20, y);
        doc.text(marketingQty.toString(), 100, y);
        doc.text(marketingTotal.toFixed(2).replace('.', ','), 150, y);

        y += 10;

        // Utilitária
        const utilityQty = parseInt(elements.utility.input.value) || 0;
        const utilityTotal = calculateTotal('utility');
        doc.text('Utilitária', 20, y);
        doc.text(utilityQty.toString(), 100, y);
        doc.text(utilityTotal.toFixed(2).replace('.', ','), 150, y);

        y += 10;

        // Autenticação
        const authQty = parseInt(elements.auth.input.value) || 0;
        const authTotal = calculateTotal('auth');
        doc.text('Autenticação', 20, y);
        doc.text(authQty.toString(), 100, y);
        doc.text(authTotal.toFixed(2).replace('.', ','), 150, y);

        y += 15;

        // Total
        const grandTotal = marketingTotal + utilityTotal + authTotal;
        doc.setFont(undefined, 'bold');
        doc.text('Total:', 100, y);
        doc.text(`R$ ${grandTotal.toFixed(2).replace('.', ',')}`, 150, y);

        // Adicionar nota
        y += 30;
        doc.setFontSize(10);
        doc.setFont(undefined, 'normal');
        doc.setTextColor(100, 100, 100);
        doc.text('Nota: Este orçamento é uma estimativa baseada nos preços oficiais da Meta para o Brasil.', 20, y);
        doc.text('Os valores podem variar conforme alterações na política de preços da Meta.', 20, y + 5);

        // Salvar o PDF
        doc.save('orcamento-whatsapp-api.pdf');
    });

    // Não precisamos mais da função de contato via WhatsApp aqui
    // pois agora estamos usando um link direto no HTML
});
