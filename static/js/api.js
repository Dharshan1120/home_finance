const API_BASE = '/api';

/**
 * Universal wrapper for Fetch API that automatically injects JWT Token
 * and handles generic errors like 401 Unauthorized.
 */
async function apiFetch(endpoint, options = {}) {
    const token = localStorage.getItem('jwtToken');
    
    // Set up standard headers
    const headers = {
        'Content-Type': 'application/json',
        ...(options.headers || {})
    };

    // Inject Auth Token
    if (token) {
        headers['Authorization'] = `Bearer ${token}`;
    }

    const config = {
        ...options,
        headers
    };

    try {
        const response = await fetch(`${API_BASE}${endpoint}`, config);
        
        // Return 204 No Content safely
        if (response.status === 204) return null;

        const data = await response.json().catch(() => null);

        if (!response.ok) {
            // Handle unauthorized globally
            if (response.status === 401 && !window.location.pathname.includes('/login')) {
                localStorage.removeItem('jwtToken');
                localStorage.removeItem('user');
                window.location.href = '/login';
                return;
            }
            throw new Error((data && data.error) || 'An unexpected error occurred');
        }

        return data;
    } catch (error) {
        console.error('API Error:', error.message);
        showToast(error.message, 'error');
        throw error;
    }
}

// Global UI Toast Function
function showToast(message, type = 'success') {
    const toast = document.getElementById('toast');
    if (!toast) return;
    
    toast.textContent = message;
    toast.className = `toast show ${type}`;
    
    setTimeout(() => {
        toast.classList.remove('show');
    }, 3000);
}
