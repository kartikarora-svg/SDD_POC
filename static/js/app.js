/**
 * Finalytics Frontend Application
 * Main JavaScript for client-side routing and API interactions
 */

// Application state
const app = {
    currentUser: null,
    apiBase: '/api',
};

// Utility: API call wrapper
async function apiCall(endpoint, options = {}) {
    const url = `${app.apiBase}${endpoint}`;
    
    // Get token from localStorage
    const token = localStorage.getItem('access_token');
    
    const defaultOptions = {
        headers: {
            'Content-Type': 'application/json',
        },
        credentials: 'include', // Include cookies for JWT
    };
    
    // Add Authorization header if token exists
    if (token && !endpoint.includes('/auth/login') && !endpoint.includes('/auth/register')) {
        defaultOptions.headers['Authorization'] = `Bearer ${token}`;
    }

    const response = await fetch(url, { ...defaultOptions, ...options });
    
    if (!response.ok) {
        const error = await response.json().catch(() => ({ detail: 'An error occurred' }));
        throw new Error(error.detail || `HTTP ${response.status}`);
    }
    
    return response.json();
}

// Router: Handle navigation
function navigate(pageName) {
    // Hide all pages
    document.querySelectorAll('.page').forEach(page => {
        page.classList.remove('active');
    });

    // Show target page
    const targetPage = document.getElementById(`${pageName}-page`);
    if (targetPage) {
        targetPage.classList.add('active');
        
        // Load dynamic page content if needed
        if (pageName === 'login' && typeof showLoginPage === 'function') {
            showLoginPage();
        } else if (pageName === 'register' && typeof showRegisterPage === 'function') {
            showRegisterPage();
        } else if (pageName === 'documents' && typeof showDocumentsPage === 'function') {
            showDocumentsPage();
        } else if (pageName === 'news' && typeof showNewsPage === 'function') {
            showNewsPage();
        } else if (pageName === 'stocks' && typeof showStocksPage === 'function') {
            showStocksPage();
        } else if (pageName === 'compare' && typeof showComparePage === 'function') {
            showComparePage();
        }
    }

    // Update nav links
    document.querySelectorAll('.nav-link').forEach(link => {
        link.classList.remove('active');
        if (link.dataset.page === pageName) {
            link.classList.add('active');
        }
    });
}

// Navigate to feature from home page cards
function navigateToFeature(featureName) {
    // Check if user is authenticated for protected features
    if (!app.currentUser && ['documents', 'stocks', 'compare'].includes(featureName)) {
        // Redirect to login if not authenticated
        alert('Please login to access this feature');
        navigate('login');
        window.location.hash = 'login';
        return;
    }
    
    // Navigate to the feature page
    navigate(featureName);
    window.location.hash = featureName;
}

// Initialize navigation
function initNavigation() {
    document.querySelectorAll('.nav-link').forEach(link => {
        link.addEventListener('click', (e) => {
            e.preventDefault();
            const pageName = link.dataset.page;
            navigate(pageName);
            window.location.hash = pageName;
        });
    });

    // Handle browser back/forward
    window.addEventListener('hashchange', () => {
        const pageName = window.location.hash.slice(1) || 'home';
        navigate(pageName);
    });

    // Load initial page
    const initialPage = window.location.hash.slice(1) || 'home';
    navigate(initialPage);
}

// Check authentication status
async function checkAuth() {
    try {
        // Get token from localStorage
        const token = localStorage.getItem('access_token');
        if (!token) {
            throw new Error('No token');
        }
        
        const user = await apiCall('/auth/me');
        app.currentUser = user;
        updateAuthUI(true);
        return true;
    } catch (error) {
        app.currentUser = null;
        updateAuthUI(false);
        localStorage.removeItem('access_token');
        return false;
    }
}

// Update UI based on auth status
function updateAuthUI(isAuthenticated) {
    const authNav = document.getElementById('auth-nav');
    if (isAuthenticated && app.currentUser) {
        authNav.innerHTML = `
            <span class="nav-link">Welcome, ${app.currentUser.email}</span>
            <a href="#" class="nav-link" id="logout-link">Logout</a>
        `;
        document.getElementById('logout-link').addEventListener('click', logout);
    } else {
        authNav.innerHTML = `
            <a href="#login" class="nav-link" data-page="login">Login</a>
        `;
    }
}

// Logout function
async function logout(e) {
    e.preventDefault();
    try {
        await apiCall('/auth/logout', { method: 'POST' });
        app.currentUser = null;
        localStorage.removeItem('access_token');
        updateAuthUI(false);
        navigate('home');
    } catch (error) {
        console.error('Logout failed:', error);
        // Force logout even if API call fails
        app.currentUser = null;
        localStorage.removeItem('access_token');
        updateAuthUI(false);
        navigate('home');
    }
}

// Show loading spinner
function showLoading(container) {
    container.innerHTML = '<div class="spinner"></div>';
}

// Show error message
function showError(container, message) {
    container.innerHTML = `
        <div class="error-message text-error text-center">
            <p>${message}</p>
        </div>
    `;
}

// Initialize application
document.addEventListener('DOMContentLoaded', () => {
    initNavigation();
    checkAuth();

    // Health check on load
    apiCall('/health')
        .then(data => console.log('API Health:', data))
        .catch(err => console.error('API Health check failed:', err));
});

// Export for use in other modules
window.app = app;
window.apiCall = apiCall;
window.navigate = navigate;
window.navigateToFeature = navigateToFeature;
window.showLoading = showLoading;
window.showError = showError;

