// Main JavaScript file for JobSearch Website

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
function checkAuthStatus() {
    const user = getCurrentUser();
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
function updateNavbarVisibility() {
    const user = getCurrentUser();
    
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
    const user = getCurrentUser();
    if (!user) {
        document.querySelectorAll('.user-only').forEach(el => {
            el.addEventListener('click', function(e) {
                e.preventDefault();
                window.location.href = getRelativePathToRoot() + 'login.html?redirect=' + encodeURIComponent(this.getAttribute('href'));
            });
        });
    }
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
            logout();
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
    const loginForm = document.getElementById('login-form');
    if (loginForm) {
        loginForm.addEventListener('submit', handleLogin);
    }
    
    const signupForm = document.getElementById('signup-form');
    if (signupForm) {
        signupForm.addEventListener('submit', handleSignup);
        
        // Show/hide company field based on checkbox
        const isCompanyCheckbox = document.getElementById('is-company');
        const companyField = document.getElementById('company-field');
        
        if (isCompanyCheckbox && companyField) {
            isCompanyCheckbox.addEventListener('change', function() {
                companyField.style.display = this.checked ? 'block' : 'none';
            });
        }
    }
}

// Handle login form submission
function handleLogin(e) {
    e.preventDefault();
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;
    const errorElement = document.getElementById('login-error');
    const basePath = getRelativePathToRoot();
    
    // Simple validation
    if (!username || !password) {
        showError(errorElement, 'Please enter both username and password');
        return;
    }
    
    // Check local storage for user data
    const users = getUsers();
    const user = users.find(u => u.username === username && u.password === password);
    
    if (user) {
        // Set current user in local storage
        localStorage.setItem('currentUser', JSON.stringify({
            id: user.id,
            username: user.username,
            email: user.email,
            role: user.isCompany ? 'admin' : 'user',
            company: user.company || null
        }));
        
        // Redirect to appropriate page
        const redirectUrl = new URLSearchParams(window.location.search).get('redirect');
        if (redirectUrl) {
            window.location.href = redirectUrl;
        } else if (user.isCompany) {
            window.location.href = basePath + 'features/admin/dashboard.html';
        } else {
            window.location.href = basePath + 'features/user/search_jobs.html';
        }
    } else {
        showError(errorElement, 'Invalid username or password');
    }
}

// Handle signup form submission
function handleSignup(e) {
    e.preventDefault();
    const username = document.getElementById('username').value;
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;
    const confirmPassword = document.getElementById('confirm-password').value;
    const isCompany = document.getElementById('is-company').checked;
    const companyName = isCompany ? document.getElementById('company-name').value : null;
    const errorElement = document.getElementById('signup-error');
    const basePath = getRelativePathToRoot();
    
    // Simple validation
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
    
    // Check if username already exists
    const users = getUsers();
    if (users.some(u => u.username === username)) {
        showError(errorElement, 'Username already exists');
        return;
    }
    
    // Add new user
    const newUser = {
        id: generateId(),
        username,
        email,
        password,
        isCompany,
        company: companyName,
        createdAt: new Date().toISOString()
    };
    
    users.push(newUser);
    localStorage.setItem('users', JSON.stringify(users));
    
    // Auto login
    localStorage.setItem('currentUser', JSON.stringify({
        id: newUser.id,
        username: newUser.username,
        email: newUser.email,
        role: newUser.isCompany ? 'admin' : 'user',
        company: newUser.company || null
    }));
    
    // Redirect to appropriate page
    if (isCompany) {
        window.location.href = basePath + 'features/admin/dashboard.html';
    } else {
        window.location.href = basePath + 'features/user/search_jobs.html';
    }
}

// Logout function
function logout() {
    localStorage.removeItem('currentUser');
    const basePath = getRelativePathToRoot();
    window.location.href = basePath + 'index.html';
}

// Get current logged in user
function getCurrentUser() {
    const userJson = localStorage.getItem('currentUser');
    return userJson ? JSON.parse(userJson) : null;
}

// Get all users from local storage
function getUsers() {
    const usersJson = localStorage.getItem('users');
    return usersJson ? JSON.parse(usersJson) : [];
}

// Get all jobs from local storage
function getJobs() {
    const jobsJson = localStorage.getItem('jobs');
    return jobsJson ? JSON.parse(jobsJson) : [];
}

// Get all applications from local storage
function getApplications() {
    const applicationsJson = localStorage.getItem('applications');
    return applicationsJson ? JSON.parse(applicationsJson) : [];
}

// Generate a unique ID
function generateId() {
    return Date.now().toString(36) + Math.random().toString(36).substring(2);
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