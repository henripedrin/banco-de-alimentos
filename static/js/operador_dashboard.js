document.addEventListener('DOMContentLoaded', async () => {
    try {
        // Busca os dados dinâmicos da API
        const data = await fetchAPI('/api/v1/dashboards/logistica');
        
        // Atualiza os cards de indicadores
        document.getElementById('entregas-pendentes').textContent = data.entregas_pendentes;
        document.getElementById('entregas-concluidas').textContent = data.entregas_concluidas;
        document.getElementById('transportes-em-andamento').textContent = data.transportes_em_andamento;

        // Atualiza a tabela de últimas entregas
        const tableBody = document.querySelector('#ultimasEntregasTable tbody');
        tableBody.innerHTML = ''; // Limpa as linhas estáticas

        if (data.ultimas_entregas && data.ultimas_entregas.length > 0) {
            data.ultimas_entregas.forEach(entrega => {
                const tr = document.createElement('tr');
                
                const dataEntrega = new Date(entrega.data_entrega).toLocaleString('pt-BR');

                tr.innerHTML = `
                    <td>#${entrega.cesta_id}</td>
                    <td>${entrega.recebedor_nome}</td>
                    <td>${dataEntrega}</td>
                    <td><span class="badge bg-success">${entrega.status}</span></td>
                `;
                tableBody.appendChild(tr);
            });
        } else {
            tableBody.innerHTML = '<tr><td colspan="4" class="text-center">Nenhuma entrega concluída recentemente.</td></tr>';
        }
        
    } catch (error) {
        console.error("Falha ao carregar os dados do dashboard:", error);
        // Você pode adicionar um alerta visual para o usuário aqui, se desejar
    }
});
