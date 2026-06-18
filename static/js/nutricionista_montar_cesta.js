// --- State Management ---
let allFoods = [];
let basket = {}; // Usar um objeto/map para acesso rápido: { foodId: { ...foodData, quantity: X } }
let allRecebedores = [];

// --- Modals ---
const reviewModal = new bootstrap.Modal(document.getElementById('reviewModal'));

// --- Event Listeners ---
document.addEventListener('DOMContentLoaded', () => {
    loadInitialData();
    document.getElementById('searchInput').addEventListener('input', () => renderAlimentosTable(allFoods));
    document.getElementById('filterCategoria').addEventListener('change', () => renderAlimentosTable(allFoods));
});

// --- API Calls & Data Loading ---

async function loadInitialData() {
    showLoading(true);
    try {
        // Carrega alimentos, recebedores e categorias em paralelo
        const [foods, users, categories] = await Promise.all([
            fetchAPI('/api/v1/alimentos/validade'),
            fetchAPI('/api/v1/usuarios/'),
            fetchAPI('/api/v1/categorias/')
        ]);

        allFoods = foods;
        allRecebedores = users.filter(u => u.categoria === 'RECEBEDOR' && u.ativo);
        
        populateCategoryFilter(categories);
        populateRecebedorSelect(allRecebedores);
        renderAlimentosTable(allFoods);

    } catch (error) {
        showAlert('Erro ao carregar dados iniciais. Tente recarregar a página.', 'danger');
    } finally {
        showLoading(false);
    }
}

async function submitBasket() {
    const recebedorId = document.getElementById('recebedorSelect').value;
    if (!recebedorId) {
        showAlert('Selecione uma organização recebedora.', 'warning');
        return;
    }
    if (Object.keys(basket).length === 0) {
        showAlert('A cesta está vazia.', 'warning');
        return;
    }

    // O backend espera o ID do nutricionista, que não temos no frontend.
    // O ideal seria o backend pegar o ID do usuário logado.
    // Como paliativo, vamos enviar um ID fixo (ex: 1) ou o ID do usuário logado se disponível.
    // A melhor solução é o backend extrair o ID do token. Por enquanto, vamos assumir que o backend faz isso.
    const payload = {
        cesta: {
            nutricionista_id: 0, // O backend deve substituir pelo ID do usuário logado
            recebedor_id: parseInt(recebedorId)
        },
        alimentos: Object.values(basket).map(item => ({
            alimento_id: item.id,
            quantidade_retirada: item.quantity
        }))
    };

    try {
        await fetchAPI('/api/v1/cestas/', {
            method: 'POST',
            body: JSON.stringify(payload)
        });
        
        reviewModal.hide();
        showAlert('Cesta básica criada com sucesso!', 'success');
        
        // Resetar o estado
        basket = {};
        loadInitialData(); // Recarrega os alimentos para atualizar o estoque
        renderBasket();

    } catch (error) {
        showAlert(error.message, 'danger');
    }
}

// --- Table & Filter Rendering ---

function populateCategoryFilter(categories) {
    const select = document.getElementById('filterCategoria');
    select.innerHTML = '<option value="">Todas as Categorias</option>';
    categories.forEach(cat => {
        select.innerHTML += `<option value="${cat.nome}">${cat.nome}</option>`;
    });
}

function populateRecebedorSelect(recebedores) {
    const select = document.getElementById('recebedorSelect');
    select.innerHTML = '<option value="">Selecione uma organização...</option>';
    recebedores.forEach(rec => {
        select.innerHTML += `<option value="${rec.id}">${rec.nome}</option>`;
    });
}

function renderAlimentosTable(foods) {
    const tbody = document.querySelector('#alimentosTable tbody');
    const searchTerm = document.getElementById('searchInput').value.toLowerCase();
    const categoryFilter = document.getElementById('filterCategoria').value;
    tbody.innerHTML = '';

    const filteredFoods = foods.filter(food => {
        const matchesSearch = food.nome.toLowerCase().includes(searchTerm);
        const matchesCategory = categoryFilter === "" || food.categoria_nome === categoryFilter;
        return matchesSearch && matchesCategory;
    });

    if (filteredFoods.length === 0) {
        tbody.innerHTML = '<tr><td colspan="6" class="text-center">Nenhum alimento encontrado.</td></tr>';
        return;
    }

    filteredFoods.forEach(food => {
        const tr = document.createElement('tr');
        const inBasketQty = basket[food.id] ? basket[food.id].quantity : 0;
        const availableQty = food.quantidade - inBasketQty;

        tr.innerHTML = `
            <td>${food.nome}</td>
            <td><span class="badge bg-secondary">${food.categoria_nome}</span></td>
            <td>${availableQty}</td>
            <td>${new Date(food.data_vencimento + 'T00:00:00').toLocaleDateString('pt-BR')}</td>
            <td>
                <input type="number" class="form-control form-control-sm" id="qty-input-${food.id}" min="1" max="${availableQty}" ${availableQty === 0 ? 'disabled' : ''}>
            </td>
            <td>
                <button class="btn btn-sm btn-success" onclick="addToBasket(${food.id})" ${availableQty === 0 ? 'disabled' : ''}>
                    <i class="bi bi-plus-lg"></i>
                </button>
            </td>
        `;
        tbody.appendChild(tr);
    });
}

// --- Basket Logic ---

function addToBasket(foodId) {
    const input = document.getElementById(`qty-input-${foodId}`);
    const quantityToAdd = parseInt(input.value);
    const food = allFoods.find(f => f.id === foodId);

    if (!food || isNaN(quantityToAdd) || quantityToAdd <= 0) {
        showAlert('Por favor, insira uma quantidade válida.', 'warning');
        return;
    }

    const currentInBasket = basket[foodId] ? basket[foodId].quantity : 0;
    if (quantityToAdd > (food.quantidade - currentInBasket)) {
        showAlert('Quantidade a adicionar excede o estoque disponível.', 'warning');
        return;
    }

    if (basket[foodId]) {
        basket[foodId].quantity += quantityToAdd;
    } else {
        basket[foodId] = { ...food, quantity: quantityToAdd };
    }

    input.value = '';
    renderBasket();
    renderAlimentosTable(allFoods); // Re-renderiza para atualizar o estoque disponível
}

function renderBasket() {
    const list = document.getElementById('basketList');
    const emptyMsg = document.getElementById('emptyBasketMsg');
    const btnConfirm = document.getElementById('btnConfirmBasket');
    const itemCountSpan = document.getElementById('basketItemCount');
    list.innerHTML = '';

    const basketItems = Object.values(basket);

    if (basketItems.length === 0) {
        emptyMsg.style.display = 'block';
        btnConfirm.disabled = true;
    } else {
        emptyMsg.style.display = 'none';
        btnConfirm.disabled = false;
        basketItems.forEach((item, index) => {
            const li = document.createElement('li');
            li.className = 'list-group-item d-flex justify-content-between align-items-center';
            li.innerHTML = `
                <span>${item.nome}</span>
                <span class="badge bg-primary rounded-pill">${item.quantity}</span>
            `;
            list.appendChild(li);
        });
    }
    itemCountSpan.textContent = basketItems.length;
}

// --- Review Modal Logic ---

function openReviewModal() {
    const recebedorId = document.getElementById('recebedorSelect').value;
    if (!recebedorId) {
        showAlert('Por favor, selecione uma organização recebedora antes de confirmar.', 'warning');
        return;
    }
    const recebedor = allRecebedores.find(r => r.id == recebedorId);
    document.getElementById('reviewRecebedorNome').textContent = recebedor.nome;
    
    renderReviewTable();
    reviewModal.show();
}

function renderReviewTable() {
    const tbody = document.querySelector('#reviewTable tbody');
    tbody.innerHTML = '';
    Object.values(basket).forEach(item => {
        const tr = document.createElement('tr');
        tr.innerHTML = `
            <td>${item.nome}</td>
            <td>
                <div class="input-group input-group-sm" style="width: 120px;">
                    <button class="btn btn-outline-secondary" type="button" onclick="updateReviewQty(${item.id}, -1)">-</button>
                    <input type="text" class="form-control text-center" value="${item.quantity}" readonly>
                    <button class="btn btn-outline-secondary" type="button" onclick="updateReviewQty(${item.id}, 1)">+</button>
                </div>
            </td>
            <td>${new Date(item.data_vencimento + 'T00:00:00').toLocaleDateString('pt-BR')}</td>
            <td class="text-end">
                <button class="btn btn-sm btn-outline-danger" onclick="removeFromBasket(${item.id})">
                    <i class="bi bi-trash"></i>
                </button>
            </td>
        `;
        tbody.appendChild(tr);
    });
}

function updateReviewQty(foodId, change) {
    const food = allFoods.find(f => f.id === foodId);
    const newQty = basket[foodId].quantity + change;

    if (newQty >= 1 && newQty <= food.quantidade) {
        basket[foodId].quantity = newQty;
        renderReviewTable();
        renderBasket();
    } else if (newQty < 1) {
        removeFromBasket(foodId);
    } else {
        showAlert('Quantidade excede o estoque total disponível.', 'warning');
    }
}

function removeFromBasket(foodId) {
    delete basket[foodId];
    renderReviewTable();
    renderBasket();
    renderAlimentosTable(allFoods); // Re-renderiza para atualizar o estoque
    if (Object.keys(basket).length === 0) {
        reviewModal.hide();
    }
}

// --- UI Utilities ---

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
