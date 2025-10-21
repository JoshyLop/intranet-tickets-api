/**
 * API Helper - Funciones para comunicarse con la API REST
 * 
 * Este archivo contiene todas las funciones para hacer peticiones
 * a tu API de Django desde JavaScript puro.
 */

// Configuración de la API
const API_BASE_URL = 'http://127.0.0.1:8000/api';

/**
 * Obtiene el token JWT guardado en localStorage
 */
function getToken() {
    return localStorage.getItem('access_token');
}

/**
 * Guarda el token en localStorage
 */
function saveToken(token) {
    localStorage.setItem('access_token', token);
}

/**
 * Elimina el token (logout)
 */
function clearToken() {
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
}

/**
 * Verifica si el usuario está autenticado
 */
function isAuthenticated() {
    return getToken() !== null;
}

/**
 * Función genérica para hacer peticiones a la API
 */
async function apiRequest(endpoint, options = {}) {
    const url = `${API_BASE_URL}${endpoint}`;
    
    // Headers por defecto
    const headers = {
        'Content-Type': 'application/json',
        ...options.headers
    };
    
    // Agregar token si existe
    const token = getToken();
    if (token) {
        headers['Authorization'] = `Bearer ${token}`;
    }
    
    // Configuración de la petición
    const config = {
        ...options,
        headers
    };
    
    try {
        const response = await fetch(url, config);
        
        // Si no está autorizado, redirigir al login
        if (response.status === 401) {
            clearToken();
            window.location.href = 'index.html';
            throw new Error('No autorizado');
        }
        
        // Si no es exitoso, lanzar error
        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(JSON.stringify(errorData));
        }
        
        // Devolver los datos en JSON
        return await response.json();
    } catch (error) {
        console.error('Error en la petición:', error);
        throw error;
    }
}

// ============================================
// AUTENTICACIÓN
// ============================================

/**
 * Login - Obtiene el token JWT
 */
async function login(username, password) {
    const response = await fetch(`${API_BASE_URL}/token/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ username, password })
    });
    
    if (!response.ok) {
        const error = await response.json();
        throw new Error(error.detail || 'Error al iniciar sesión');
    }
    
    const data = await response.json();
    saveToken(data.access);
    localStorage.setItem('refresh_token', data.refresh);
    return data;
}

/**
 * Logout - Limpia el token
 */
function logout() {
    clearToken();
    window.location.href = 'index.html';
}

// ============================================
// TICKETS
// ============================================

/**
 * Obtiene la lista de todos los tickets
 */
async function getTickets(filters = {}) {
    let endpoint = '/tickets/';
    
    // Agregar filtros a la URL
    const params = new URLSearchParams(filters);
    if (params.toString()) {
        endpoint += '?' + params.toString();
    }
    
    return await apiRequest(endpoint);
}

/**
 * Obtiene los tickets del usuario actual
 */
async function getMyTickets() {
    return await apiRequest('/tickets/my-tickets/');
}

/**
 * Obtiene los tickets asignados al usuario actual
 */
async function getAssignedTickets() {
    return await apiRequest('/tickets/assigned-to-me/');
}

/**
 * Obtiene un ticket específico por ID
 */
async function getTicket(id) {
    return await apiRequest(`/tickets/${id}/`);
}

/**
 * Crea un nuevo ticket
 */
async function createTicket(ticketData) {
    return await apiRequest('/tickets/', {
        method: 'POST',
        body: JSON.stringify(ticketData)
    });
}

/**
 * Actualiza un ticket
 */
async function updateTicket(id, ticketData) {
    return await apiRequest(`/tickets/${id}/`, {
        method: 'PATCH',
        body: JSON.stringify(ticketData)
    });
}

/**
 * Cierra un ticket
 */
async function closeTicket(id) {
    return await apiRequest(`/tickets/${id}/close/`, {
        method: 'POST'
    });
}

/**
 * Reabre un ticket
 */
async function reopenTicket(id) {
    return await apiRequest(`/tickets/${id}/reopen/`, {
        method: 'POST'
    });
}

// ============================================
// COMENTARIOS
// ============================================

/**
 * Obtiene los comentarios de un ticket
 */
async function getComments(ticketId) {
    return await apiRequest(`/comments/?ticket=${ticketId}`);
}

/**
 * Crea un nuevo comentario
 */
async function createComment(commentData) {
    return await apiRequest('/comments/', {
        method: 'POST',
        body: JSON.stringify(commentData)
    });
}

// ============================================
// USUARIOS Y PERFILES
// ============================================

/**
 * Obtiene el perfil del usuario actual
 */
async function getMyProfile() {
    return await apiRequest('/profiles/me/');
}

/**
 * Obtiene la lista de usuarios
 */
async function getUsers() {
    return await apiRequest('/users/');
}
