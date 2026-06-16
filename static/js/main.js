document.addEventListener('DOMContentLoaded', () => {
    const sidebarToggle = document.getElementById('sidebarToggle');
    const sidebar = document.getElementById('sidebar');
    const mainContent = document.getElementById('mainContent');
    const logoutButton = document.getElementById('logoutButton');

    // Toggle da Sidebar em telas menores
    if (sidebarToggle) {
        sidebarToggle.addEventListener('click', () => {
            sidebar.classList.toggle('active');
        });
    }

    // Lógica de Logout
    if (logoutButton) {
        logoutButton.addEventListener('click', (e) => {
            e.preventDefault();
            localStorage.removeItem('accessToken');
            localStorage.removeItem('userProfile');
            window.location.href = '/login';
        });
    }

    // Exibir nome do usuário (simulação, idealmente viria de uma API)
    const userName = document.getElementById('userName');
    if (userName) {
        // Em um caso real, você faria um fetch para /api/v1/users/me para obter os dados do usuário
        const userProfile = localStorage.getItem('userProfile');
        userName.textContent = userProfile ? userProfile.charAt(0).toUpperCase() + userProfile.slice(1) : 'Usuário';
    }
});
