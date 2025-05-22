document.addEventListener('DOMContentLoaded', function () {
    const simularBtn = document.getElementById('s');

    simularBtn.addEventListener('click', async function (e) {
        e.preventDefault();

        // Coleta os dados do formulário
        const capitalInput = document.getElementById('capital').value.replace(/\D/g, '');
        const capital = parseFloat(capitalInput);
        const risco = document.getElementById('niveis').value.toLowerCase(); // "leve", "moderada", "grave"
        const empresa = document.getElementById('empresa').value.trim();

        if (!capital || capital <= 0) {
            alert('Por favor, insira um capital válido.');
            return;
        }

        const payload = {
            capital: capital,
            risk_profile: risco,
            tickers: [empresa]
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
                console.log('Resultado da simulação:', data);

                alert(
                    `Simulação realizada!\n\n` +
                    `Empresa: ${empresa}\n` +
                    `Peso: ${data.allocation[empresa].peso}%\n` +
                    `Valor investido: R$${data.allocation[empresa].valor}\n` +
                    `Retorno esperado: ${data.expected_return}%\n` +
                    `Risco: ${data.risk}%`
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
