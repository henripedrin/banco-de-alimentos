let allUsers = []; // Cache dos usuários para paginação e busca local
let currentPage = 1;
const itemsPerPage = 10;
let currentModalMode = 'create'; // 'create', 'edit', 'view'

const userModal = new bootstrap.Modal(document.getElementById('userModal'));
const deleteModal = new bootstrap.Modal(document.getElementById('deleteModal'));

document.addEventListener('DOMContentLoaded', () => {
    loadUsers();

    // Listeners para filtros
    document.getElementById('searchInput').addEventListener('input', filterUsers);
    document.getElementById('filterCategoria').addEventListener('change', filterUsers);
});

// --- API Calls ---

async function loadUsers() {
    showLoading(true);
    try {
        allUsers = await fetchAPI('/api/v1/usuarios/');
        renderTable(allUsers);
    } catch (error) {
        showAlert('Erro ao carregar usuários.', 'danger');
    } finally {
        showLoading(false);
    }
}

async function saveUser() {
    const form = document.getElementById('userForm');
    if (!form.checkValidity()) {
        form.reportValidity();
        return;
    }

    const userId = document.getElementById('userId').value;
    const userData = {
        nome: document.getElementById('nome').value,
        username: document.getElementById('username').value,
        categoria: document.getElementById('categoria').value,
    };

    const senhaValue = document.getElementById('senha').value;
    if (senhaValue) {
        userData.senha = senhaValue;
    }
    
    if (currentModalMode === 'edit') {
        userData.ativo = document.getElementById('ativo').checked;
    }

    try {
        const btnSave = document.getElementById('btnSaveUser');
        btnSave.disabled = true;
        btnSave.innerHTML = '<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> Salvando...';

        if (currentModalMode === 'create') {
            await fetchAPI('/api/v1/usuarios/', {
                method: 'POST',
                body: JSON.stringify(userData)
            });
            showAlert('Usuário criado com sucesso!', 'success');
        } else if (currentModalMode === 'edit') {
            await fetchAPI(`/api/v1/usuarios/${userId}`, {
                method: 'PUT',
                body: JSON.stringify(userData)
            });
            showAlert('Usuário atualizado com sucesso!', 'success');
        }

        userModal.hide();
        loadUsers(); // Recarrega a tabela
        
        // Atualiza indicadores do dashboard se estiver na mesma página (opcional, dependendo de como a UI é estruturada)
        // updateDashboardIndicators();
        
    } catch (error) {
        showAlert(error.message, 'danger');
    } finally {
        const btnSave = document.getElementById('btnSaveUser');
        btnSave.disabled = false;
        btnSave.textContent = 'Salvar';
    }
}

async function confirmDelete() {
    const userId = document.getElementById('deleteUserId').value;
    try {
        await fetchAPI(`/api/v1/usuarios/${userId}`, { method: 'DELETE' });
        showAlert('Usuário excluído com sucesso!', 'success');
        deleteModal.hide();
        loadUsers();
    } catch (error) {
        showAlert(error.message, 'danger');
        deleteModal.hide();
    }
}

// --- Renderização e UI ---

function renderTable(users) {
    const tbody = document.querySelector('#usersTable tbody');
    tbody.innerHTML = '';

    if (users.length === 0) {
        tbody.innerHTML = '<tr><td colspan="6" class="text-center">Nenhum usuário encontrado.</td></tr>';
        renderPagination(0);
        return;
    }

    // Paginação simples no frontend
    const startIndex = (currentPage - 1) * itemsPerPage;
    const endIndex = startIndex + itemsPerPage;
    const paginatedUsers = users.slice(startIndex, endIndex);

    paginatedUsers.forEach(user => {
        const tr = document.createElement('tr');
        
        // Determina a cor do badge de categoria
        let catBadge = 'bg-secondary';
        if(user.categoria === 'ADMINISTRADOR') catBadge = 'bg-danger';
        else if(user.categoria === 'NUTRICIONISTA') catBadge = 'bg-info text-dark';
        else if(user.categoria === 'AGENTE_SANITARIO') catBadge = 'bg-warning text-dark';
        else if(user.categoria === 'DOADOR') catBadge = 'bg-success';
        
        const statusBadge = user.ativo ? '<span class="badge bg-success">Ativo</span>' : '<span class="badge bg-secondary">Inativo</span>';

        tr.innerHTML = `
            <td>#${user.id}</td>
            <td class="fw-bold">${user.nome}</td>
            <td>@${user.username}</td>
            <td><span class="badge ${catBadge}">${user.categoria}</span></td>
            <td>${statusBadge}</td>
            <td class="text-end">
                <button class="btn btn-sm btn-outline-secondary me-1" onclick="openViewModal(${user.id})" title="Visualizar">
                    <i class="bi bi-eye"></i>
                </button>
                <button class="btn btn-sm btn-outline-primary me-1" onclick="openEditModal(${user.id})" title="Editar">
                    <i class="bi bi-pencil"></i>
                </button>
                <button class="btn btn-sm btn-outline-danger" onclick="openDeleteModal(${user.id}, '${user.nome}')" title="Excluir">
                    <i class="bi bi-trash"></i>
                </button>
            </td>
        `;
        tbody.appendChild(tr);
    });

    renderPagination(users.length);
}

function filterUsers() {
    const searchTerm = document.getElementById('searchInput').value.toLowerCase();
    const categoryFilter = document.getElementById('filterCategoria').value;

    const filtered = allUsers.filter(user => {
        const matchesSearch = user.nome.toLowerCase().includes(searchTerm) || user.username.toLowerCase().includes(searchTerm);
        const matchesCategory = categoryFilter === "" || user.categoria === categoryFilter;
        return matchesSearch && matchesCategory;
    });

    currentPage = 1; // Reseta para a primeira página ao filtrar
    renderTable(filtered);
}

function renderPagination(totalItems) {
    const totalPages = Math.ceil(totalItems / itemsPerPage);
    const pagination = document.getElementById('pagination');
    pagination.innerHTML = '';

    if (totalPages <= 1) return;

    // Anterior
    pagination.innerHTML += `
        <li class="page-item ${currentPage === 1 ? 'disabled' : ''}">
            <a class="page-link" href="#" onclick="changePage(${currentPage - 1}, event)">Anterior</a>
        </li>
    `;

    // Páginas
    for (let i = 1; i <= totalPages; i++) {
        pagination.innerHTML += `
            <li class="page-item ${currentPage === i ? 'active' : ''}">
                <a class="page-link" href="#" onclick="changePage(${i}, event)">${i}</a>
            </li>
        `;
    }

    // Próximo
    pagination.innerHTML += `
        <li class="page-item ${currentPage === totalPages ? 'disabled' : ''}">
            <a class="page-link" href="#" onclick="changePage(${currentPage + 1}, event)">Próximo</a>
        </li>
    `;
}

function changePage(page, event) {
    if (event) event.preventDefault();
    currentPage = page;
    filterUsers(); // Re-aplica filtros e renderiza a nova página
}

// --- Modais ---

function resetForm() {
    document.getElementById('userForm').reset();
    document.getElementById('userId').value = '';
    const inputs = document.querySelectorAll('#userForm input, #userForm select');
    inputs.forEach(input => input.disabled = false);
    document.getElementById('btnSaveUser').style.display = 'block';
    document.getElementById('btnCancelModal').textContent = 'Cancelar';
}

function openCreateModal() {
    currentModalMode = 'create';
    resetForm();
    document.getElementById('userModalLabel').textContent = 'Novo Usuário';
    
    // Configurações específicas para Create
    document.getElementById('senha').required = true;
    document.getElementById('senhaLabel').innerHTML = 'Senha <span class="text-danger">*</span>';
    document.getElementById('senhaHelp').classList.add('d-none');
    document.getElementById('statusContainer').style.display = 'none'; // Não mostra status na criação (default true)
}

function openEditModal(id) {
    currentModalMode = 'edit';
    resetForm();
    const user = allUsers.find(u => u.id === id);
    if (!user) return;

    document.getElementById('userModalLabel').textContent = 'Editar Usuário';
    
    // Preenche dados
    document.getElementById('userId').value = user.id;
    document.getElementById('nome').value = user.nome;
    document.getElementById('username').value = user.username;
    document.getElementById('categoria').value = user.categoria;
    document.getElementById('ativo').checked = user.ativo;

    // Configurações específicas para Edit
    document.getElementById('senha').required = false;
    document.getElementById('senhaLabel').innerHTML = 'Senha';
    document.getElementById('senhaHelp').classList.remove('d-none');
    document.getElementById('statusContainer').style.display = 'block';

    userModal.show();
}

function openViewModal(id) {
    currentModalMode = 'view';
    resetForm();
    const user = allUsers.find(u => u.id === id);
    if (!user) return;

    document.getElementById('userModalLabel').textContent = 'Visualizar Usuário';
    
    // Preenche dados
    document.getElementById('nome').value = user.nome;
    document.getElementById('username').value = user.username;
    document.getElementById('categoria').value = user.categoria;
    document.getElementById('ativo').checked = user.ativo;

    // Desabilita campos
    const inputs = document.querySelectorAll('#userForm input, #userForm select');
    inputs.forEach(input => input.disabled = true);
    
    // Esconde botões desnecessários
    document.getElementById('btnSaveUser').style.display = 'none';
    document.getElementById('btnCancelModal').textContent = 'Fechar';
    document.getElementById('statusContainer').style.display = 'block';
    
    // Esconde campo de senha
    document.getElementById('senha').parentElement.style.display = 'none';

    userModal.show();
}

function openDeleteModal(id, nome) {
    document.getElementById('deleteUserId').value = id;
    document.getElementById('deleteUserName').textContent = nome;
    deleteModal.show();
}

// --- Utilitários ---

function showLoading(show) {
    const loader = document.getElementById('tableLoading');
    const table = document.getElementById('usersTable');
    if (show) {
        loader.classList.remove('d-none');
        table.classList.add('opacity-50');
    } else {
        loader.classList.add('d-none');
        table.classList.remove('opacity-50');
    }
}

function showAlert(message, type = 'success') {
    const alertHtml = `
        <div class="alert alert-${type} alert-dismissible fade show" role="alert">
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
        </div>
    `;
    const container = document.getElementById('alertContainer');
    container.innerHTML = alertHtml;
    
    // Auto-remover após 5 segundos
    setTimeout(() => {
        const alertNode = document.querySelector('.alert');
        if (alertNode) {
            const bsAlert = new bootstrap.Alert(alertNode);
            bsAlert.close();
        }
    }, 5000);
}
