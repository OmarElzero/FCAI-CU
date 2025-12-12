// Authentication handling for JobSearch application
// This file handles login, registration, and session management

import { 
    loginUser as loginUserAPI, 
    registerUser as registerUserAPI, 
    logoutUser as logoutUserAPI, 
    getCurrentUser as getCurrentUserAPI 
} from './api.js';
import { getRelativePathToRoot, showError, clearError } from './utils.js';
import { handleLoginSuccess, handleRegistrationSuccess, handleLogoutSuccess } from './navigation.js';

/**
 * Handle login form submission
 * @param {Event} e - Form submit event
 */
async function handleLogin(e) {
    e.preventDefault();
    
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;
    const email = document.getElementById('email')?.value || null; // Optional for login
    const companyAdmin = document.getElementById('company-admin')?.checked || false;
    const companyName = companyAdmin ? document.getElementById('company-name')?.value : null;
    
    const errorElement = document.getElementById('login-error');
    const basePath = getRelativePathToRoot();
    
    // Clear previous errors
    clearError(errorElement);
    
    // Basic validation
    if (!username || !password) {
        showError(errorElement, 'Please enter both username and password');
        return;
    }

    // Additional validation for company admins
    if (companyAdmin && !companyName) {
        showError(errorElement, 'Please enter company name');
        return;
    }
    
    try {
        // Call the login API
        const user = await loginUserAPI(username, password);
        
        // Store minimal user info in localStorage for UI purposes only
        // The actual authentication is handled by cookies/sessions
        if (user) {
            localStorage.setItem('user', JSON.stringify({
                id: user.id,
                username: user.username,
                is_company: user.is_company
            }));
            
            // Refresh navbar to show correct menu items
            if (window.refreshNavbar) {
                window.refreshNavbar();
            }
            
            // Use navigation manager for clean redirects
            handleLoginSuccess(user);
        }
    } catch (error) {
        // Show error message
        showError(errorElement, error.message || 'Invalid username or password');
    }
}

/**
 * Handle signup form submission
 * @param {Event} e - Form submit event
 */
async function handleSignup(e) {
    e.preventDefault();
    
    const username = document.getElementById('username').value;
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;
    const confirmPassword = document.getElementById('confirm-password')?.value;
    const isCompany = document.getElementById('is-company')?.checked || false;
    const companyName = isCompany ? document.getElementById('company-name')?.value : null;
    
    const errorElement = document.getElementById('signup-error');
    const basePath = getRelativePathToRoot();
    
    // Clear previous errors
    clearError(errorElement);
    
    // Basic validations
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
        // Prepare user data
        const userData = {
            username,
            email,
            password,
            is_company: isCompany,
            company: companyName
        };
        
        // Call the register API
        const user = await registerUserAPI(userData);
        
        if (user) {
            // Refresh navbar to show correct menu items
            if (window.refreshNavbar) {
                window.refreshNavbar();
            }
            
            // Use navigation manager for clean redirects
            handleRegistrationSuccess(user);
        }
    } catch (error) {
        // Show error message
        showError(errorElement, error.message || 'Registration failed');
    }
}

/**
 * Handle logout
 */
async function handleLogout() {
    try {
        await logoutUserAPI();
        // Clear local storage
        localStorage.removeItem('user');
        
        // Refresh navbar to show logged out state
        if (window.refreshNavbar) {
            window.refreshNavbar();
        }
        
        // Use navigation manager for clean redirects
        handleLogoutSuccess();
    } catch (error) {
        console.error('Logout failed:', error);
        // Force clear local storage even if API fails
        localStorage.removeItem('user');
        
        // Refresh navbar even if API call failed
        if (window.refreshNavbar) {
            window.refreshNavbar();
        }
        
        // Still redirect even if API call failed
        handleLogoutSuccess();
    }
}

/**
 * Check if user is authenticated and redirect if needed
 * @param {Object} options - Options for authentication check
 * @param {boolean} options.requireAuth - Whether authentication is required
 * @param {boolean} options.requireCompany - Whether company role is required
 * @param {boolean} options.requireJobSeeker - Whether job seeker role is required
 * @param {Function} options.onAuthenticated - Callback for when user is authenticated
 */
async function checkAuth({
    requireAuth = true,
    requireCompany = false,
    requireJobSeeker = false,
    onAuthenticated = null
} = {}) {
    try {
        const user = await getCurrentUserAPI();
        
        // Just update UI - no redirects
        if (user) {
            // Update UI based on authentication status
            document.body.classList.add('authenticated');
            
            if (user.is_company) {
                document.body.classList.add('company-user');
                document.body.classList.remove('job-seeker');
            } else {
                document.body.classList.add('job-seeker');
                document.body.classList.remove('company-user');
            }
            
            // Call the onAuthenticated callback if provided
            if (onAuthenticated && typeof onAuthenticated === 'function') {
                onAuthenticated(user);
            }
        } else {
            // Update UI for unauthenticated user
            document.body.classList.remove('authenticated', 'company-user', 'job-seeker');
        }
        
        // Return user info for caller to handle navigation
        return user;
    } catch (error) {
        console.error('Auth check failed:', error);
        return null;
    }
}

// Initialize auth check on page load
document.addEventListener('DOMContentLoaded', function() {
    // Setup login form handler
    const loginForm = document.getElementById('login-form');
    if (loginForm) {
        loginForm.addEventListener('submit', handleLogin);
    }
    
    // Setup signup form handler
    const signupForm = document.getElementById('signup-form');
    if (signupForm) {
        signupForm.addEventListener('submit', handleSignup);
    }
    
    // Setup logout buttons
    const logoutButtons = document.querySelectorAll('.logout-button');
    logoutButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            e.preventDefault();
            handleLogout();
        });
    });
    
    // Toggle company name field visibility
    const companyAdminCheckbox = document.getElementById('company-admin');
    const companyNameContainer = document.getElementById('company-name-container');
    
    if (companyAdminCheckbox && companyNameContainer) {
        companyAdminCheckbox.addEventListener('change', function() {
            if (this.checked) {
                companyNameContainer.style.display = 'block';
            } else {
                companyNameContainer.style.display = 'none';
            }
        });
    }
    
    // Same for signup page
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
});

// Export functions for use in other modules
export {
    handleLogin,
    handleSignup,
    handleLogout,
    checkAuth
};
