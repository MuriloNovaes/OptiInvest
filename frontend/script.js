document.addEventListener('DOMContentLoaded', function () {
    const simularBtn = document.getElementById('s');
    const capitalInput = document.getElementById('capital');

    capitalInput.addEventListener('input', function (e) {
        let rawValue = e.target.value.replace(/\D/g, '');

        if (rawValue.length > 8) rawValue = rawValue.slice(0, 8);
        let numericValue = parseInt(rawValue || '0', 10);

        if (numericValue > 10000000) numericValue = 10000000;

        let formatted = (numericValue / 100).toFixed(2) + '';
        formatted = formatted.replace('.', ',');
        formatted = formatted.replace(/\B(?=(\d{3})+(?!\d))/g, '.');
        e.target.value = 'R$ ' + formatted;
    });

    simularBtn.addEventListener('click', async function (e) {
        e.preventDefault();

        const capitalElement = document.getElementById('capital');
        const capitalRaw = capitalElement.value.replace(/\D/g, '');
        const capital = parseFloat(capitalRaw);
        const risco = document.getElementById('risk_profile').value.toLowerCase();

        if (!capital || capital <= 0) {
            alert('Por favor, insira um capital válido.');
            return;
        }

        const payload = {
            capital: capital,
            risk_profile: risco
        };

        try {
            const response = await fetch('http://127.0.0.1:5000/api/optimize', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(payload)
            });

            const data = await response.json();

            if (data.success) {
                const distribuicao = data.allocation.map(item =>
                    `${item.ticker}: ${item.peso_percentual}% (R$ ${item.valor_investido.toLocaleString('pt-BR', {minimumFractionDigits: 2, maximumFractionDigits: 2})})`
                ).join('\n');

                alert(
                    `Simulação realizada!\n\n` +
                    `Valor investido: ${capitalElement.value}\n` +
                    `Retorno esperado: ${data.expected_return}%\n` +
                    `Risco: ${data.risk}%\n\n` +
                    `Melhores ações: ${data.melhores_acoes.join(', ')}\n\n` +
                    `Distribuição:\n${distribuicao}`
                );
            } else {
                alert(`Erro: ${data.error}`);
            }
        } catch (error) {
            console.error('Erro na requisição:', error);
            alert('Erro ao conectar com o servidor.');
        }
    });
});
