// --- State Management ---
let donationItems = []; // Lista temporária de itens a serem doados
let categories = []; // Cache das categorias de alimentos

// --- Modals ---
const itemModal = new bootstrap.Modal(document.getElementById('donationItemModal'));
const reviewModal = new bootstrap.Modal(document.getElementById('reviewDonationModal'));

// --- Event Listeners ---
document.addEventListener('DOMContentLoaded', () => {
    loadHistory();
    loadCategories();

    // Listener para o checkbox de avaria
    document.getElementById('possuiAvaria').addEventListener('change', (e) => {
        const avariaFields = document.getElementById('avariaFields');
        avariaFields.classList.toggle('d-none', !e.target.checked);
    });

    // Limpa o formulário ao fechar o modal de item
    document.getElementById('donationItemModal').addEventListener('hidden.bs.modal', () => {
        document.getElementById('donationItemForm').reset();
        document.getElementById('avariaFields').classList.add('d-none');
    });
});

// --- API Calls & Data Loading ---

async function loadHistory() {
    showLoading(true);
    try {
        const history = await fetchAPI('/api/v1/doacoes/'); // Endpoint corrigido
        renderHistoryTable(history);
    } catch (error) {
        showAlert('Erro ao carregar o histórico de doações.', 'danger');
    } finally {
        showLoading(false);
    }
}

async function loadCategories() {
    try {
        categories = await fetchAPI('/api/v1/categorias/');
        const select = document.getElementById('alimentoCategoria');
        select.innerHTML = '<option value="">Selecione...</option>'; // Limpa o "Carregando..."
        categories.forEach(cat => {
            select.innerHTML += `<option value="${cat.id}">${cat.nome}</option>`;
        });
    } catch (error) {
        showAlert('Erro ao carregar as categorias de alimentos.', 'danger');
    }
}

async function confirmDonation() {
    if (donationItems.length === 0) {
        showAlert('Adicione pelo menos um item à doação.', 'warning');
        return;
    }

    const payload = {
        itens_solicitacao: donationItems
    };

    try {
        const response = await fetchAPI('/api/v1/doacoes/', { // Endpoint corrigido
            method: 'POST',
            body: JSON.stringify(payload)
        });
        
        reviewModal.hide();
        showAlert(response.mensagem, 'success');
        donationItems = []; // Limpa a lista
        updateItemCount();
        loadHistory(); // Atualiza o histórico

    } catch (error) {
        showAlert(error.message, 'danger');
    }
}

// --- Form & Item Logic ---

function addItemToList() {
    const form = document.getElementById('donationItemForm');
    if (!form.checkValidity()) {
        form.reportValidity();
        return;
    }

    const possuiAvaria = document.getElementById('possuiAvaria').checked;
    const quantidade = parseInt(document.getElementById('alimentoQtd').value);
    const qtdAvariada = parseInt(document.getElementById('alimentoQtdAvariada').value);

    // Validações extras
    if (possuiAvaria) {
        if (isNaN(qtdAvariada) || qtdAvariada <= 0) {
            showAlert('A quantidade avariada deve ser um número maior que zero.', 'warning');
            return;
        }
        if (qtdAvariada > quantidade) {
            showAlert('A quantidade avariada não pode ser maior que a quantidade total.', 'warning');
            return;
        }
        if (!document.getElementById('alimentoDescAvaria').value) {
            showAlert('A descrição da avaria é obrigatória.', 'warning');
            return;
        }
    }

    const newItem = {
        nome: document.getElementById('alimentoNome').value,
        categoria_id: parseInt(document.getElementById('alimentoCategoria').value),
        quantidade: quantidade,
        unidade_medida: document.getElementById('alimentoUnidade').value,
        data_vencimento: document.getElementById('alimentoVencimento').value,
        possui_avaria: possuiAvaria,
        quantidade_avariada: possuiAvaria ? qtdAvariada : null,
        descricao_avaria: possuiAvaria ? document.getElementById('alimentoDescAvaria').value : null,
    };

    donationItems.push(newItem);
    updateItemCount();
    form.reset();
    document.getElementById('avariaFields').classList.add('d-none');
    document.getElementById('alimentoNome').focus(); // Foca no primeiro campo para o próximo item
    showAlert(`'${newItem.nome}' adicionado à lista!`, 'info');
}

function finishDonation() {
    if (donationItems.length === 0) {
        showAlert('Adicione pelo menos um item antes de finalizar.', 'warning');
        return;
    }
    itemModal.hide();
    renderReviewTable();
    reviewModal.show();
}

function cancelDonation() {
    if (confirm('Tem certeza que deseja cancelar esta doação? Todos os itens adicionados serão perdidos.')) {
        donationItems = [];
        updateItemCount();
        reviewModal.hide();
        showAlert('Doação cancelada.', 'secondary');
    }
}

// --- Review Table Logic ---

function renderReviewTable() {
    const tbody = document.querySelector('#reviewTable tbody');
    tbody.innerHTML = '';
    donationItems.forEach((item, index) => {
        const tr = document.createElement('tr');
        const vencimento = new Date(item.data_vencimento + 'T00:00:00').toLocaleDateString('pt-BR');
        const avariaText = item.possui_avaria ? `<span class="badge bg-warning text-dark">Sim</span>` : 'Não';

        tr.innerHTML = `
            <td>${item.nome}</td>
            <td>
                <div class="input-group input-group-sm" style="width: 120px;">
                    <button class="btn btn-outline-secondary" type="button" onclick="updateReviewItemQty(${index}, -1)">-</button>
                    <input type="text" class="form-control text-center" value="${item.quantidade}" readonly>
                    <button class="btn btn-outline-secondary" type="button" onclick="updateReviewItemQty(${index}, 1)">+</button>
                </div>
            </td>
            <td>${vencimento}</td>
            <td>${avariaText}</td>
            <td class="text-end">
                <button class="btn btn-sm btn-outline-danger" onclick="removeReviewItem(${index})">
                    <i class="bi bi-trash"></i> Remover
                </button>
            </td>
        `;
        tbody.appendChild(tr);
    });
}

function updateReviewItemQty(index, change) {
    if (donationItems[index].quantidade + change >= 1) {
        donationItems[index].quantidade += change;
        renderReviewTable();
    }
}

function removeReviewItem(index) {
    donationItems.splice(index, 1);
    renderReviewTable();
    updateItemCount();
    if (donationItems.length === 0) {
        reviewModal.hide();
    }
}

// --- UI Updates & Utilities ---

function renderHistoryTable(history) {
    const tbody = document.querySelector('#donationsTable tbody');
    tbody.innerHTML = '';

    if (history.length === 0) {
        tbody.innerHTML = '<tr><td colspan="5" class="text-center">Você ainda não fez nenhuma doação.</td></tr>';
        return;
    }

    history.forEach(donation => {
        const tr = document.createElement('tr');
        const date = new Date(donation.data_solicitacao).toLocaleDateString('pt-BR');
        
        let statusBadge = 'bg-secondary';
        if(donation.status === 'APROVADA') statusBadge = 'bg-success';
        else if(donation.status === 'REJEITADA') statusBadge = 'bg-danger';
        else if(donation.status === 'PENDENTE') statusBadge = 'bg-warning text-dark';

        const itemCount = donation.itens.reduce((sum, item) => sum + item.quantidade, 0);
        const itemSummary = donation.itens.length > 0 ? `${donation.itens.length} tipo(s) de item` : 'N/A';

        tr.innerHTML = `
            <td>#${donation.id}</td>
            <td>${date}</td>
            <td>${itemSummary}</td>
            <td><span class="badge ${statusBadge}">${donation.status}</span></td>
            <td>${donation.observacao_vigilante || '<em>Nenhuma</em>'}</td>
        `;
        tbody.appendChild(tr);
    });
}

function updateItemCount() {
    document.getElementById('itemCount').textContent = donationItems.length;
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
