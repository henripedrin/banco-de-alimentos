// --- Modals ---
const detailsModal = new bootstrap.Modal(document.getElementById('detailsModal'));
const confirmModal = new bootstrap.Modal(document.getElementById('confirmModal'));

// --- Event Listeners ---
document.addEventListener('DOMContentLoaded', () => {
    loadPendingDeliveries();
});

// --- API Calls & Data Loading ---

async function loadPendingDeliveries() {
    showLoading(true);
    try {
        const pendingDeliveries = await fetchAPI('/api/v1/entregas/pendentes');
        renderTable(pendingDeliveries);
    } catch (error) {
        if (error.message.includes("Not Found")) { // A API pode retornar 404 se não houver nada
            renderTable([]);
        } else {
            showAlert('Erro ao carregar entregas pendentes.', 'danger');
        }
    } finally {
        showLoading(false);
    }
}

async function showDetails(deliveryId) {
    try {
        const details = await fetchAPI(`/api/v1/entregas/${deliveryId}/detalhes`);
        
        // Preenche os detalhes do modal
        document.getElementById('detailId').textContent = `#${details.id}`;
        document.getElementById('detailCestaId').textContent = `#${details.cesta_id}`;
        document.getElementById('detailStatus').innerHTML = `<span class="badge bg-warning text-dark">${details.status}</span>`;
        document.getElementById('detailRecebedor').textContent = details.recebedor_nome;
        document.getElementById('detailOperador').textContent = details.operador_nome || 'Não atribuído';
        document.getElementById('detailDataCriacao').textContent = new Date(details.data_criacao).toLocaleString('pt-BR');
        document.getElementById('detailDataEntrega').textContent = details.data_entrega ? new Date(details.data_entrega).toLocaleString('pt-BR') : 'Pendente';

        const itemsTbody = document.getElementById('itemsTableBody');
        itemsTbody.innerHTML = '';
        if (details.itens_cesta.length > 0) {
            details.itens_cesta.forEach(item => {
                const tr = document.createElement('tr');
                tr.innerHTML = `
                    <td>${item.nome}</td>
                    <td>${item.quantidade_retirada}</td>
                `;
                itemsTbody.appendChild(tr);
            });
        } else {
            itemsTbody.innerHTML = '<tr><td colspan="2" class="text-center">Cesta vazia.</td></tr>';
        }

        detailsModal.show();
    } catch (error) {
        showAlert('Erro ao carregar detalhes da entrega.', 'danger');
    }
}

function openConfirmModal(deliveryId, recebedorNome) {
    document.getElementById('confirmDeliveryId').value = deliveryId;
    document.getElementById('confirmRecebedorNome').textContent = recebedorNome;
    confirmModal.show();
}

async function submitConfirmation() {
    const deliveryId = document.getElementById('confirmDeliveryId').value;
    if (!deliveryId) return;

    try {
        await fetchAPI(`/api/v1/entregas/${deliveryId}/confirmar`, { method: 'PUT' });
        showAlert('Entrega confirmada com sucesso!', 'success');
        confirmModal.hide();
        loadPendingDeliveries(); // Recarrega a lista
    } catch (error) {
        showAlert(error.message, 'danger');
    }
}

// --- UI Rendering ---

function renderTable(deliveries) {
    const tbody = document.querySelector('#deliveriesTable tbody');
    tbody.innerHTML = '';

    if (!deliveries || deliveries.length === 0) {
        tbody.innerHTML = '<tr><td colspan="6" class="text-center">Nenhuma entrega pendente encontrada.</td></tr>';
        return;
    }

    deliveries.forEach(delivery => {
        const tr = document.createElement('tr');
        const date = new Date(delivery.data_criacao).toLocaleDateString('pt-BR');
        
        tr.innerHTML = `
            <td>#${delivery.id}</td>
            <td>#${delivery.cesta_id}</td>
            <td>${delivery.recebedor_nome}</td>
            <td>${date}</td>
            <td><span class="badge bg-warning text-dark">${delivery.status}</span></td>
            <td class="text-end">
                <button class="btn btn-sm btn-outline-secondary me-1" onclick="showDetails(${delivery.id})" title="Ver Detalhes">
                    <i class="bi bi-eye"></i>
                </button>
                <button class="btn btn-sm btn-success" onclick="openConfirmModal(${delivery.id}, '${delivery.recebedor_nome}')" title="Confirmar Entrega">
                    <i class="bi bi-check-lg"></i>
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
