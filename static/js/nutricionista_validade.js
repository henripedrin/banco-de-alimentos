document.addEventListener('DOMContentLoaded', () => {
    loadValidadeData();
});

async function loadValidadeData() {
    showLoading(true);
    try {
        const alimentos = await fetchAPI('/api/v1/alimentos/validade');
        renderTable(alimentos);
    } catch (error) {
        showAlert('Erro ao carregar dados de validade.', 'danger');
        renderTable([]); // Renderiza a tabela vazia em caso de erro
    } finally {
        showLoading(false);
    }
}

function renderTable(alimentos) {
    const tbody = document.querySelector('#validadeTable tbody');
    tbody.innerHTML = '';

    if (!alimentos || alimentos.length === 0) {
        tbody.innerHTML = '<tr><td colspan="3" class="text-center">Nenhum alimento encontrado.</td></tr>';
        return;
    }

    const today = new Date();
    today.setHours(0, 0, 0, 0); // Zera a hora para comparações de data

    // Adiciona a diferença de dias e a classe de cor a cada objeto
    const alimentosComStatus = alimentos.map(alimento => {
        const vencimento = new Date(alimento.data_vencimento + 'T00:00:00');
        const diffTime = vencimento - today;
        const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));
        
        let rowClass = '';
        let priority = 3; // 1=Vencido, 2=Alerta, 3=OK

        if (diffDays < 0) {
            rowClass = 'table-danger'; // Vencido
            priority = 1;
        } else if (diffDays <= 2) {
            rowClass = 'table-warning'; // Vence em até 2 dias
            priority = 2;
        }
        
        return { ...alimento, rowClass, priority, vencimento };
    });

    // Ordena pela prioridade definida
    alimentosComStatus.sort((a, b) => a.priority - b.priority || a.vencimento - b.vencimento);

    // Renderiza as linhas da tabela
    alimentosComStatus.forEach(alimento => {
        const tr = document.createElement('tr');
        tr.className = alimento.rowClass;

        tr.innerHTML = `
            <td>${alimento.nome}</td>
            <td>${alimento.quantidade}</td>
            <td>${alimento.vencimento.toLocaleDateString('pt-BR')}</td>
        `;
        tbody.appendChild(tr);
    });
}

// --- Utilitários de UI ---

function showLoading(isLoading) {
    const loader = document.getElementById('tableLoading');
    const table = document.getElementById('validadeTable');
    if (isLoading) {
        loader.classList.remove('d-none');
        table.classList.add('opacity-50');
    } else {
        loader.classList.add('d-none');
        table.classList.remove('opacity-50');
    }
}

function showAlert(message, type = 'success') {
    const container = document.getElementById('alertContainer');
    const alertHtml = `
        <div class="alert alert-${type} alert-dismissible fade show" role="alert">
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
        </div>
    `;
    container.innerHTML = alertHtml;
    setTimeout(() => {
        const alertNode = container.querySelector('.alert');
        if (alertNode) new bootstrap.Alert(alertNode).close();
    }, 5000);
}
