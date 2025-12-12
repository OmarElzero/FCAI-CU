// Main JavaScript file for JobSearch Website

// BASE API URL
const API_BASE = 'http://localhost:8000/api/';

// DOM Content Loaded Event Listener
document.addEventListener('DOMContentLoaded', function() {
    // Load navbar
    loadNavbar();
    
    // Authentication check
    checkAuthStatus();
    
    // Setup event listeners for authentication forms
    setupAuthForms();
});

// Load the navbar component
function loadNavbar() {
    const navbarContainer = document.getElementById('navbar-container');
    if (navbarContainer) {
        // Get the correct relative path based on the current page location
        const basePath = getRelativePathToRoot();
        
        fetch(`${basePath}components/navbar.html`)
            .then(response => response.text())
            .then(html => {
                navbarContainer.innerHTML = html;
                // Fix links in the navbar after loading
                fixNavbarLinks();
                updateNavbarVisibility();
                setupNavbarEventListeners();
            })
            .catch(error => {
                console.error('Error loading navbar:', error);
            });
    }
}

// Get the relative path to the root directory based on the current page
function getRelativePathToRoot() {
    const path = window.location.pathname;
    let depth = 0;
    
    // Count how many directories deep we are
    if (path.includes('/features/')) {
        // For pages in features subdirectories (2 levels deep)
        depth = 2;
    } else if (path.includes('/components/')) {
        // For pages in components directory (1 level deep)
        depth = 1;
    }
    
    // Return appropriate relative path
    return depth === 0 ? '' : '../'.repeat(depth);
}

// Fix the links in navbar depending on the current page depth
function fixNavbarLinks() {
    const basePath = getRelativePathToRoot();
    
    // Update all links in the navbar
    const navbarLinks = document.querySelectorAll('.navbar-menu a');
    navbarLinks.forEach(link => {
        const href = link.getAttribute('href');
        
        // Skip links that are already absolute or external
        if (href && !href.startsWith('http') && !href.startsWith('/') && href !== '#') {
            // If it's a relative link, prepend the base path
            link.setAttribute('href', basePath + href);
        }
    });
    
    // Update the logo link
    const logoLink = document.querySelector('.logo');
    if (logoLink) {
        logoLink.setAttribute('href', basePath + 'index.html');
    }
}

// Check authentication status and update UI
async function checkAuthStatus() {
    const user = await getCurrentUser();
    const basePath = getRelativePathToRoot();
    updateNavbarVisibility();
    
    // Redirect if page requires authentication
    const requiresAuth = document.body.classList.contains('requires-auth');
    const requiresAdmin = document.body.classList.contains('requires-admin');
    
    if (requiresAuth && !user) {
        window.location.href = basePath + 'login.html?redirect=' + encodeURIComponent(window.location.pathname);
        return;
    }
    
    if (requiresAdmin && (!user || user.role !== 'admin')) {
        window.location.href = basePath + 'login.html';
        return;
    }
}

// Update navbar visibility based on authentication
async function updateNavbarVisibility() {
    const user = await getCurrentUser();
    
    // Wait for navbar to be loaded
    setTimeout(() => {
        const userOnlyElements = document.querySelectorAll('.user-only');
        const adminOnlyElements = document.querySelectorAll('.admin-only');
        const loggedInOnlyElements = document.querySelectorAll('.logged-in-only');
        const loggedOutOnlyElements = document.querySelectorAll('.logged-out-only');
        
        // Update username display if available
        const usernameDisplay = document.getElementById('username-display');
        if (usernameDisplay && user) {
            usernameDisplay.textContent = user.username;
        }
        
        // Show/hide elements based on login status
        if (user) {
            loggedInOnlyElements.forEach(el => el.style.display = 'block');
            loggedOutOnlyElements.forEach(el => el.style.display = 'none');
            
            if (user.role === 'admin') {
                adminOnlyElements.forEach(el => el.style.display = 'block');
                userOnlyElements.forEach(el => el.style.display = 'none');
            } else {
                adminOnlyElements.forEach(el => el.style.display = 'none');
                userOnlyElements.forEach(el => el.style.display = 'block');
            }
        } else {
            loggedInOnlyElements.forEach(el => el.style.display = 'none');
            loggedOutOnlyElements.forEach(el => el.style.display = 'block');
            adminOnlyElements.forEach(el => el.style.display = 'none');
            userOnlyElements.forEach(el => el.style.display = 'block'); // Show user-only buttons for guests
        }
    }, 100);
}

// Intercept user-only navbar clicks for guests
setTimeout(() => {
    getCurrentUser().then(user => {
        if (!user) {
            document.querySelectorAll('.user-only').forEach(el => {
                el.addEventListener('click', function(e) {
                    e.preventDefault();
                    window.location.href = getRelativePathToRoot() + 'login.html?redirect=' + encodeURIComponent(this.getAttribute('href'));
                });
            });
        }
    });
}, 500);

// Setup navbar event listeners
function setupNavbarEventListeners() {
    const basePath = getRelativePathToRoot();
    
    const navbarBurger = document.getElementById('navbar-burger');
    const navbarMenu = document.getElementById('navbar-menu');
    
    if (navbarBurger && navbarMenu) {
        navbarBurger.addEventListener('click', function() {
            navbarBurger.classList.toggle('is-active');
            navbarMenu.classList.toggle('active');
        });
    }
    
    const logoutLink = document.getElementById('logout-link');
    if (logoutLink) {
        logoutLink.addEventListener('click', function(e) {
            e.preventDefault();
            logoutUser();
        });
    }
    
    // Use relative paths for links
    const searchJobsLink = document.getElementById('search-jobs-link');
    if (searchJobsLink) {
        searchJobsLink.href = basePath + 'features/user/search_jobs.html';
    }
    
    const appliedJobsLink = document.getElementById('applied-jobs-link');
    if (appliedJobsLink) {
        appliedJobsLink.href = basePath + 'features/user/applied_jobs.html';
    }
    
    const dashboardLink = document.getElementById('dashboard-link');
    if (dashboardLink) {
        dashboardLink.href = basePath + 'features/admin/dashboard.html';
    }
    
    const addJobLink = document.getElementById('add-job-link');
    if (addJobLink) {
        addJobLink.href = basePath + 'features/admin/add_job.html';
    }
}

// Setup authentication forms (login, signup)
function setupAuthForms() {
    // We now handle form submissions via the auth.js module
    // This function is kept for backward compatibility
}

// Handle login form submission - now handled by auth.js module
async function handleLogin(e) {
    console.warn('Main.js handleLogin is deprecated. Using auth.js module instead.');
    // Import and use the module version
    try {
        const authModule = await import('./userjs/auth.js');
        authModule.handleLogin(e);
    } catch (error) {
        console.error('Failed to import auth module:', error);
    }
}

// Handle signup form submission - now handled by auth.js module
async function handleSignup(e) {
    console.warn('Main.js handleSignup is deprecated. Using auth.js module instead.');
    // Import and use the module version
    try {
        const authModule = await import('./userjs/auth.js');
        authModule.handleSignup(e);
    } catch (error) {
        console.error('Failed to import auth module:', error);
    }
}

// Logout function - now handled by auth.js module
async function logoutUser() {
    console.warn('Main.js logoutUser is deprecated. Using auth.js module instead.');
    // Import and use the module version
    try {
        const authModule = await import('./userjs/auth.js');
        authModule.handleLogout();
    } catch (error) {
        console.error('Failed to import auth module:', error);
    }
    const basePath = getRelativePathToRoot();
    window.location.href = basePath + 'index.html';
}

// Get current logged in user (from backend session)
async function getCurrentUser() {
    try {
        // Try to get user from backend session using the current user endpoint
        const res = await fetch(API_BASE + 'users/current/', { credentials: 'include' });
        if (!res.ok) return null;
        return await res.json();
    } catch (error) {
        console.error('Failed to get current user:', error);
        return null;
    }
}

// Fetch all jobs from backend
async function getJobs() {
    const res = await fetch(API_BASE + 'jobs/');
    if (!res.ok) return [];
    return await res.json();
}

// Fetch all users (admin only)
async function getUsers() {
    const res = await fetch(API_BASE + 'users/', { credentials: 'include' });
    if (!res.ok) return [];
    return await res.json();
}

// Fetch all applications (for current user or company)
async function getApplications() {
    const res = await fetch(API_BASE + 'applications/', { credentials: 'include' });
    if (!res.ok) return [];
    return await res.json();
}

// Login using backend
async function loginUser(username, password) {
    const res = await fetch(API_BASE + 'users/login/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        credentials: 'include',
        body: JSON.stringify({ username, password })
    });
    if (!res.ok) return null;
    return await res.json();
}

// Register using backend
async function registerUser(data) {
    const res = await fetch(API_BASE + 'users/register/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
    });
    if (!res.ok) return null;
    return await res.json();
}

// Logout using backend
async function logoutUser() {
    await fetch(API_BASE + 'users/logout/', {
        method: 'POST',
        credentials: 'include'
    });
}

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

// Truncate text to a specific length
function truncateText(text, maxLength) {
    return text.length > maxLength ? text.substring(0, maxLength) + '...' : text;
}

// Format date to readable string
function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', {
        year: 'numeric', 
        month: 'long', 
        day: 'numeric'
    });
}

// Initialize modal
function initModal(modalId) {
    const modal = document.getElementById(modalId);
    if (!modal) return;
    
    const closeButton = modal.querySelector('.close-modal');
    if (closeButton) {
        closeButton.addEventListener('click', () => {
            modal.style.display = 'none';
        });
    }
    
    // Close when clicking outside the modal
    window.addEventListener('click', (event) => {
        if (event.target === modal) {
            modal.style.display = 'none';
        }
    });
}

// Get URL parameters
function getUrlParams() {
    const params = {};
    const queryString = window.location.search;
    const urlParams = new URLSearchParams(queryString);
    
    for (const [key, value] of urlParams.entries()) {
        params[key] = value;
    }
    
    return params;
}