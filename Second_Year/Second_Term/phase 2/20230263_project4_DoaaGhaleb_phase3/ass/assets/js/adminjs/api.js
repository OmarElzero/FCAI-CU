const API_BASE = 'http://localhost:8000/api/';

async function apiRequest(endpoint, options = {}) {
    try {
        if (!options.headers) {
            options.headers = { 'Content-Type': 'application/json' };
        }
        if (!options.hasOwnProperty('credentials')) {
            options.credentials = 'include';
        }
        const response = await fetch(`${API_BASE}${endpoint}`, options);
        if (!response.ok) {
            throw new Error(`API error: ${response.status}`);
        }
        if (response.status === 204) {
            return null;
        }
        return await response.json();
    } catch (error) {
        console.error(`API request failed: ${error.message}`);
        return null;
    }
}
async function getCurrentUser() {
    try {
        const response = await apiRequest('users/current/');
        return response;
    } catch (error) {
        console.error('Failed to get current user:', error);
        return null;
    }
}
export { apiRequest, getCurrentUser };
