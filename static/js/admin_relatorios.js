document.addEventListener('DOMContentLoaded', () => {
    loadReports();
});

async function loadReports() {
    showLoading(true);
    try {
        const reports = await fetchAPI('/api/v1/relatorios/');
        renderTable(reports);
    } catch (error) {
        showAlert('Erro ao carregar a lista de relatórios.', 'danger');
        renderTable([]);
    } finally {
        showLoading(false);
    }
}

function renderTable(reports) {
    const tbody = document.querySelector('#reportsTable tbody');
    tbody.innerHTML = '';

    if (!reports || reports.length === 0) {
        tbody.innerHTML = '<tr><td colspan="4" class="text-center">Nenhum relatório gerado ainda.</td></tr>';
        return;
    }

    reports.forEach(report => {
        const tr = document.createElement('tr');
        const generationDate = new Date(report.generation_date).toLocaleString('pt-BR');
        
        tr.innerHTML = `
            <td>${report.reference_month}</td>
            <td>${generationDate}</td>
            <td>${report.file_name}</td>
            <td class="text-end">
                <button class="btn btn-sm btn-primary" onclick="downloadReport('${report.file_name}', this)">
                    <i class="bi bi-download me-1"></i> Download
                </button>
            </td>
        `;
        tbody.appendChild(tr);
    });
}

async function downloadReport(fileName, buttonElement) {
    const originalButtonHtml = buttonElement.innerHTML;
    buttonElement.disabled = true;
    buttonElement.innerHTML = `<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> Baixando...`;

    try {
        const token = localStorage.getItem('accessToken');
        if (!token) {
            throw new Error('Sessão não encontrada ou expirada. Faça login novamente.');
        }

        const response = await fetch(`/api/v1/relatorios/download/${fileName}`, {
            headers: { 'Authorization': `Bearer ${token}` }
        });

        if (!response.ok) {
            const errorData = await response.json().catch(() => ({}));
            throw new Error(errorData.detail || `Erro no servidor (${response.status})`);
        }

        const blob = await response.blob();
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.style.display = 'none';
        a.href = url;
        a.download = fileName;
        document.body.appendChild(a);
        a.click();
        window.URL.revokeObjectURL(url);
        document.body.removeChild(a);

    } catch (error) {
        showAlert(error.message, 'danger');
    } finally {
        buttonElement.disabled = false;
        buttonElement.innerHTML = originalButtonHtml;
    }
}

async function generateManualReport() {
    const startDate = document.getElementById('startDate').value;
    const endDate = document.getElementById('endDate').value;

    if (!startDate || !endDate) {
        showAlert('Por favor, selecione as datas de início e fim.', 'warning');
        return;
    }

    if (new Date(endDate) < new Date(startDate)) {
        showAlert('A data final não pode ser anterior à data inicial.', 'warning');
        return;
    }

    const payload = { start_date: startDate, end_date: endDate };

    try {
        const response = await fetchAPI('/api/v1/relatorios/gerar', {
            method: 'POST',
            body: JSON.stringify(payload)
        });
        
        showAlert(response.message, 'info');
        
        // Aguarda um pouco para o backend processar e depois atualiza a lista
        setTimeout(() => {
            loadReports();
        }, 5000); // Aumentado para 5 segundos para dar tempo de gerar o PDF

    } catch (error) {
        showAlert(error.message, 'danger');
    }
}

function setPresetDate(period) {
    const today = new Date();
    const year = today.getFullYear();
    const month = today.getMonth(); // 0-11

    let startDate, endDate;

    if (period === 'last_month') {
        startDate = new Date(year, month - 1, 1);
        endDate = new Date(year, month, 0);
    } else if (period === 'this_month') {
        startDate = new Date(year, month, 1);
        endDate = today;
    }

    document.getElementById('startDate').value = startDate.toISOString().split('T')[0];
    document.getElementById('endDate').value = endDate.toISOString().split('T')[0];
}

function showLoading(isLoading) {
    const loader = document.getElementById('tableLoading');
    const table = document.getElementById('reportsTable');
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
