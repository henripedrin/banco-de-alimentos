// Utilitário para fazer requisições à API com o token JWT
async function fetchAPI(endpoint, options = {}) {
    const token = localStorage.getItem('accessToken');
    
    // Configura os headers padrão, adicionando o token se existir
    const defaultHeaders = {
        'Content-Type': 'application/json',
    };

    if (token) {
        defaultHeaders['Authorization'] = `Bearer ${token}`;
    }

    const config = {
        ...options,
        headers: {
            ...defaultHeaders,
            ...options.headers,
        },
    };

    try {
        const response = await fetch(endpoint, config);

        // Se o token for inválido ou expirou (401), redireciona para o login
        if (response.status === 401) {
            localStorage.removeItem('accessToken');
            localStorage.removeItem('userProfile');
            window.location.href = '/login';
            throw new Error('Sessão expirada. Faça login novamente.');
        }

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.detail || `Erro na requisição: ${response.status}`);
        }

        return await response.json();
    } catch (error) {
        console.error('Erro na API:', error);
        throw error;
    }
}
