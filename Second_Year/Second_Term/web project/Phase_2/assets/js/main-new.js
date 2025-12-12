// Simplified JobSearch Main JavaScript
const API_BASE = 'http://localhost:8000/api/';

// =====================
// CORE FUNCTIONS
// =====================

// Get current user from backend
async function getCurrentUser() {
    try {
        const response = await fetch(`${API_BASE}users/current/`, {
            credentials: 'include'
        });
        
        if (!response.ok) {
            return null;
        }
        
        const user = await response.json();
        console.log('📱 Current user loaded:', user);
        return user;
    } catch (error) {
        console.error('❌ Failed to get current user:', error);
        return null;
    }
}

// Login function
async function loginUser(username, password) {
    try {
        const response = await fetch(`${API_BASE}users/login/`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            credentials: 'include',
            body: JSON.stringify({ username, password })
        });
        
        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.error || 'Login failed');
        }
        
        const user = await response.json();
        console.log('✅ Login successful:', user);
        return user;
    } catch (error) {
        console.error('❌ Login failed:', error);
        throw error;
    }
}

// Register function
async function registerUser(userData) {
    try {
        const response = await fetch(`${API_BASE}users/register/`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            credentials: 'include',
            body: JSON.stringify(userData)
        });
        
        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.error || 'Registration failed');
        }
        
        const user = await response.json();
        console.log('✅ Registration successful:', user);
        return user;
    } catch (error) {
        console.error('❌ Registration failed:', error);
        throw error;
    }
}

// Logout function
async function logoutUser() {
    try {
        await fetch(`${API_BASE}users/logout/`, {
            method: 'POST',
            credentials: 'include'
        });
        
        console.log('✅ Logout successful');
        // Redirect to home page
        window.location.href = getBasePath() + 'index.html';
    } catch (error) {
        console.error('❌ Logout failed:', error);
        // Still redirect even if API fails
        window.location.href = getBasePath() + 'index.html';
    }
}

// =====================
// NAVBAR FUNCTIONS
// =====================

// Get base path for current page
function getBasePath() {
    const path = window.location.pathname;
    if (path.includes('/features/')) {
        return '../../';
    } else if (path.includes('/components/')) {
        return '../';
    }
    return '';
}

// Load navbar
async function loadNavbar() {
    const navbarContainer = document.getElementById('navbar-container');
    if (!navbarContainer) return;
    
    try {
        const basePath = getBasePath();
        const response = await fetch(`${basePath}components/navbar.html`);
        const html = await response.text();
        
        navbarContainer.innerHTML = html;
        
        // Fix navbar links
        fixNavbarLinks();
        
        // Setup navbar functionality
        setupNavbar();
        
        // Update navbar based on user
        await updateNavbar();
        
        console.log('📊 Navbar loaded successfully');
    } catch (error) {
        console.error('❌ Failed to load navbar:', error);
    }
}

// Fix navbar links based on current page location
function fixNavbarLinks() {
    const basePath = getBasePath();
    
    // Fix all navbar links
    const links = document.querySelectorAll('.navbar a[href]');
    links.forEach(link => {
        const href = link.getAttribute('href');
        if (href && !href.startsWith('http') && !href.startsWith('/') && href !== '#') {
            link.setAttribute('href', basePath + href);
        }
    });
}

// Setup navbar event listeners
function setupNavbar() {
    // Mobile menu toggle
    const burger = document.getElementById('navbar-burger');
    const menu = document.getElementById('navbar-menu');
    
    if (burger && menu) {
        burger.addEventListener('click', () => {
            burger.classList.toggle('is-active');
            menu.classList.toggle('active');
        });
    }
    
    // Logout button
    const logoutLink = document.getElementById('logout-link');
    if (logoutLink) {
        logoutLink.addEventListener('click', (e) => {
            e.preventDefault();
            logoutUser();
        });
    }
}

// Update navbar based on current user
async function updateNavbar() {
    const user = await getCurrentUser();
    
    console.log('🔄 Updating navbar for user:', user);
    
    // Get navbar elements
    const userOnlyElements = document.querySelectorAll('.user-only');
    const adminOnlyElements = document.querySelectorAll('.admin-only');
    const loggedInElements = document.querySelectorAll('.logged-in-only');
    const loggedOutElements = document.querySelectorAll('.logged-out-only');
    const usernameDisplay = document.getElementById('username-display');
    
    if (user) {
        // User is logged in
        console.log(`👤 User logged in: ${user.username} (Company: ${user.is_company})`);
        
        // Show logged in elements
        loggedInElements.forEach(el => el.style.display = 'block');
        loggedOutElements.forEach(el => el.style.display = 'none');
        
        // Update username
        if (usernameDisplay) {
            usernameDisplay.textContent = user.username;
        }
        
        // Show appropriate menu items based on user type
        if (user.is_company) {
            console.log('🏢 Showing admin menu');
            adminOnlyElements.forEach(el => el.style.display = 'block');
            userOnlyElements.forEach(el => el.style.display = 'none');
        } else {
            console.log('👨‍💼 Showing user menu');
            adminOnlyElements.forEach(el => el.style.display = 'none');
            userOnlyElements.forEach(el => el.style.display = 'block');
        }
    } else {
        // User is not logged in
        console.log('👤 No user logged in');
        
        // Show logged out elements
        loggedInElements.forEach(el => el.style.display = 'none');
        loggedOutElements.forEach(el => el.style.display = 'block');
        
        // Hide all role-specific elements
        adminOnlyElements.forEach(el => el.style.display = 'none');
        userOnlyElements.forEach(el => el.style.display = 'block'); // Show for guests
    }
}

// =====================
// FORM HANDLERS
// =====================

// Handle login form
async function handleLogin(e) {
    e.preventDefault();
    
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;
    const errorElement = document.getElementById('login-error');
    
    // Clear previous errors
    if (errorElement) {
        errorElement.textContent = '';
        errorElement.style.display = 'none';
    }
    
    // Validate
    if (!username || !password) {
        showError(errorElement, 'Please enter both username and password');
        return;
    }
    
    try {
        const user = await loginUser(username, password);
        
        // Update navbar
        await updateNavbar();
        
        // Redirect based on user type
        if (user.is_company) {
            window.location.href = getBasePath() + 'features/admin/dashboard.html';
        } else {
            window.location.href = getBasePath() + 'features/user/search_jobs.html';
        }
    } catch (error) {
        showError(errorElement, error.message);
    }
}

// Handle signup form
async function handleSignup(e) {
    e.preventDefault();
    
    const username = document.getElementById('username').value;
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;
    const confirmPassword = document.getElementById('confirm-password').value;
    const isCompany = document.getElementById('is-company').checked;
    const companyName = document.getElementById('company-name').value;
    const errorElement = document.getElementById('signup-error');
    
    // Clear previous errors
    if (errorElement) {
        errorElement.textContent = '';
        errorElement.style.display = 'none';
    }
    
    // Validate
    if (!username || !email || !password || !confirmPassword) {
        showError(errorElement, 'All fields are required');
        return;
    }
    
    if (password !== confirmPassword) {
        showError(errorElement, 'Passwords do not match');
        return;
    }
    
    if (isCompany && !companyName) {
        showError(errorElement, 'Company name is required');
        return;
    }
    
    try {
        const userData = {
            username,
            email,
            password,
            is_company: isCompany,
            company: companyName || null
        };
        
        const user = await registerUser(userData);
        
        // Update navbar
        await updateNavbar();
        
        // Redirect based on user type
        if (user.is_company) {
            window.location.href = getBasePath() + 'features/admin/dashboard.html';
        } else {
            window.location.href = getBasePath() + 'features/user/search_jobs.html';
        }
    } catch (error) {
        showError(errorElement, error.message);
    }
}

// =====================
// UTILITY FUNCTIONS
// =====================

// Show error message
function showError(element, message) {
    if (element) {
        element.textContent = message;
        element.style.display = 'block';
    }
}

// Clear error message
function clearError(element) {
    if (element) {
        element.textContent = '';
        element.style.display = 'none';
    }
}

// =====================
// INITIALIZATION
// =====================

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', async function() {
    console.log('🚀 JobSearch application initializing...');
    
    // Load navbar
    await loadNavbar();
    
    // Setup form handlers
    const loginForm = document.getElementById('login-form');
    if (loginForm) {
        loginForm.addEventListener('submit', handleLogin);
    }
    
    const signupForm = document.getElementById('signup-form');
    if (signupForm) {
        signupForm.addEventListener('submit', handleSignup);
        
        // Toggle company field
        const isCompanyCheckbox = document.getElementById('is-company');
        const companyField = document.getElementById('company-field');
        
        if (isCompanyCheckbox && companyField) {
            isCompanyCheckbox.addEventListener('change', function() {
                if (this.checked) {
                    companyField.classList.add('visible');
                } else {
                    companyField.classList.remove('visible');
                }
            });
        }
    }
    
    console.log('✅ JobSearch application initialized');
});

// Debug function for browser console
window.debugAuth = async function() {
    const user = await getCurrentUser();
    console.log('=== AUTH DEBUG ===');
    console.log('Current user:', user);
    if (user) {
        console.log('Username:', user.username);
        console.log('Is company:', user.is_company);
        console.log('Company name:', user.company);
    }
    console.log('==================');
    return user;
};

// Make functions available globally
window.getCurrentUser = getCurrentUser;
window.updateNavbar = updateNavbar;
