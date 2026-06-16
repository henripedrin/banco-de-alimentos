document.addEventListener('DOMContentLoaded', async () => {
    try {
        // Busca os dados dinâmicos da API
        const data = await fetchAPI('/api/v1/dashboards/admin');
        
        // Atualiza os cards de indicadores
        document.getElementById('total-users').textContent = data.total_users;
        document.getElementById('total-batches').textContent = data.total_doacoes; // Total de doações (antigo lotes)
        document.getElementById('total-orgs').textContent = data.total_recebedores; // Recebedores
        document.getElementById('total-baskets').textContent = data.total_cestas;

        // Opcional: Adicionar os novos cards ou atualizar os existentes com os totais por categoria
        // Por exemplo, você pode criar elementos HTML dinamicamente para exibir Nutricionistas, Agentes, etc.

        // Atualiza a tabela de atividades recentes
        const tableBody = document.querySelector('table tbody');
        tableBody.innerHTML = ''; // Limpa as linhas estáticas

        if (data.recent_activities && data.recent_activities.length > 0) {
            data.recent_activities.forEach(activity => {
                const tr = document.createElement('tr');
                
                // Formata a data
                const dateObj = new Date(activity.data);
                const formattedDate = dateObj.toLocaleDateString('pt-BR') + ' ' + dateObj.toLocaleTimeString('pt-BR', { hour: '2-digit', minute: '2-digit' });

                tr.innerHTML = `
                    <td>${activity.acao}</td>
                    <td>${activity.detalhe}</td>
                    <td>${formattedDate}</td>
                `;
                tableBody.appendChild(tr);
            });
        } else {
            tableBody.innerHTML = '<tr><td colspan="3" class="text-center">Nenhuma atividade recente.</td></tr>';
        }

        // Gráfico (Opcional - você precisará buscar dados específicos para o gráfico na API depois)
        // Por enquanto, vou deixar o gráfico vazio ou com os dados simulados
        
    } catch (error) {
        console.error("Falha ao carregar os dados do dashboard:", error);
        // Exibir mensagem de erro na tela se desejar
    }
});
