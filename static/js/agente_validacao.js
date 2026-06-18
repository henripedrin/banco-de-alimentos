// --- State Management ---
let currentDonationId = null;

// --- Modals ---
const detailsModal = new bootstrap.Modal(document.getElementById('detailsModal'));
const rejectModal = new bootstrap.Modal(document.getElementById('rejectModal'));

// --- Event Listeners ---
document.addEventListener('DOMContentLoaded', () => {
    loadPendingDonations();
});

// --- API Calls & Data Loading ---

async function loadPendingDonations() {
    showLoading(true);
    try {
        const pendingDonations = await fetchAPI('/api/v1/doacoes/pendentes');
        renderTable(pendingDonations);
    } catch (error) {
        // A API retorna 404 se não houver pendentes, o que o fetchAPI trata como erro.
        // Verificamos se a mensagem é essa para limpar a tabela em vez de mostrar um erro vermelho.
        if (error.message.includes("Não há doações pendentes")) {
            renderTable([]);
        } else {
            showAlert('Erro ao carregar doações pendentes.', 'danger');
        }
    } finally {
        showLoading(false);
    }
}

async function showDetails(donationId) {
    currentDonationId = donationId;
    try {
        const details = await fetchAPI(`/api/v1/doacoes/${donationId}/detalhes`);
        
        // Preenche os detalhes do modal
        document.getElementById('detailId').textContent = `#${details.id}`;
        document.getElementById('detailDoador').textContent = details.doador_nome;
        document.getElementById('detailData').textContent = new Date(details.data_solicitacao).toLocaleString('pt-BR');
        
        const itemsTbody = document.querySelector('#itemsTable tbody');
        itemsTbody.innerHTML = '';
        details.itens.forEach(item => {
            const tr = document.createElement('tr');
            const avariaText = item.quantidade_avariada > 0 
                ? `<span class="badge bg-warning text-dark" title="${item.descricao_avaria}">${item.quantidade_avariada} un.</span>` 
                : 'Não';

            tr.innerHTML = `
                <td>${item.nome}</td>
                <td>${item.categoria_nome}</td>
                <td>${item.quantidade} ${item.unidade_medida}</td>
                <td>${new Date(item.data_vencimento + 'T00:00:00').toLocaleDateString('pt-BR')}</td>
                <td>${avariaText}</td>
            `;
            itemsTbody.appendChild(tr);
        });

        detailsModal.show();
    } catch (error) {
        showAlert('Erro ao carregar detalhes da doação.', 'danger');
    }
}

async function approveDonation() {
    if (!currentDonationId) return;
    if (!confirm(`Tem certeza que deseja APROVAR a doação #${currentDonationId}?`)) return;

    try {
        await fetchAPI(`/api/v1/doacoes/${currentDonationId}/aprovar`, { method: 'PUT' });
        showAlert('Doação aprovada com sucesso!', 'success');
        detailsModal.hide();
        loadPendingDonations(); // Recarrega a lista
    } catch (error) {
        showAlert(error.message, 'danger');
    }
}

function openRejectModal() {
    if (!currentDonationId) return;
    document.getElementById('rejectDonationId').textContent = `#${currentDonationId}`;
    document.getElementById('rejectForm').reset();
    rejectModal.show();
}

async function confirmRejection() {
    const form = document.getElementById('rejectForm');
    if (!form.checkValidity()) {
        form.reportValidity();
        return;
    }

    const motivo = document.getElementById('rejectionReason').value;
    const payload = { motivo: motivo };

    try {
        await fetchAPI(`/api/v1/doacoes/${currentDonationId}/rejeitar`, {
            method: 'PUT',
            body: JSON.stringify(payload)
        });
        showAlert('Doação rejeitada com sucesso!', 'success');
        rejectModal.hide();
        detailsModal.hide();
        loadPendingDonations(); // Recarrega a lista
    } catch (error) {
        showAlert(error.message, 'danger');
    }
}

// --- UI Rendering ---

function renderTable(donations) {
    const tbody = document.querySelector('#pendingDonationsTable tbody');
    tbody.innerHTML = '';

    if (donations.length === 0) {
        tbody.innerHTML = '<tr><td colspan="5" class="text-center">Nenhuma doação pendente no momento.</td></tr>';
        return;
    }

    donations.forEach(donation => {
        const tr = document.createElement('tr');
        const date = new Date(donation.data_solicitacao).toLocaleDateString('pt-BR');
        
        tr.innerHTML = `
            <td>#${donation.id}</td>
            <td>${date}</td>
            <td>${donation.doador_nome}</td>
            <td><span class="badge bg-warning text-dark">${donation.status}</span></td>
            <td class="text-end">
                <button class="btn btn-sm btn-primary" onclick="showDetails(${donation.id})">
                    <i class="bi bi-search me-1"></i> Ver Detalhes
                </button>
            </td>
        `;
        tbody.appendChild(tr);
    });
}

function showLoading(isLoading) {
    document.getElementById('tableLoading').classList.toggle('d-none', !isLoading);
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
