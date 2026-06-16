document.addEventListener('DOMContentLoaded', () => {
    const loginForm = document.getElementById('loginForm');
    const errorMessage = document.getElementById('error-message');

    loginForm.addEventListener('submit', async (event) => {
        event.preventDefault();

        const username = loginForm.username.value;
        const password = loginForm.password.value;

        // Validação simples de campos
        if (!username || !password) {
            showError('Por favor, preencha todos os campos.');
            return;
        }

        // Usando FormData para compatibilidade com o backend FastAPI (OAuth2PasswordRequestForm)
        const formData = new FormData();
        formData.append('username', username);
        formData.append('password', password);

        try {
            const response = await fetch('/api/v1/auth/login', {
                method: 'POST',
                body: formData,
            });

            if (response.ok) {
                const data = await response.json();
                // Armazena o token e redireciona
                localStorage.setItem('accessToken', data.access_token);
                localStorage.setItem('userProfile', data.profile); // Armazena o perfil do usuário

                // Redireciona para o dashboard correto
                window.location.href = `/dashboard/${data.profile}`;
            } else {
                const errorData = await response.json();
                showError(errorData.detail || 'Nome de usuário ou senha inválidos.');
            }
        } catch (error) {
            console.error('Erro ao tentar fazer login:', error);
            showError('Não foi possível conectar ao servidor. Tente novamente mais tarde.');
        }
    });

    function showError(message) {
        errorMessage.textContent = message;
        errorMessage.classList.remove('d-none');
    }
});
