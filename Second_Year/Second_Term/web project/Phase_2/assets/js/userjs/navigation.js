// Centralized navigation/redirect manager
// This handles all navigation logic in one place

import { getCurrentUser } from './api.js';
import { getRelativePathToRoot } from './utils.js';

/**
 * Navigate to a specific page with proper authentication checks
 * @param {string} page - Page to navigate to ('dashboard', 'search', 'login', 'signup', 'home')
 * @param {object} options - Navigation options
 */
export async function navigateTo(page, options = {}) {
    const basePath = getRelativePathToRoot();
    const user = await getCurrentUser();
    
    console.log('Navigation request:', { page, user: user?.username, isCompany: user?.is_company });
    
    switch (page) {
        case 'dashboard':
            if (!user) {
                navigateTo('login', { returnTo: 'dashboard' });
                return;
            }
            if (!user.is_company) {
                showMessage('Access denied: This page is for company users only');
                navigateTo('search');
                return;
            }
            window.location.href = basePath + 'features/admin/dashboard.html';
            break;
            
        case 'search':
            if (!user) {
                navigateTo('login', { returnTo: 'search' });
                return;
            }
            window.location.href = basePath + 'features/user/search_jobs.html';
            break;
            
        case 'applied':
            if (!user) {
                navigateTo('login', { returnTo: 'applied' });
                return;
            }
            if (user.is_company) {
                showMessage('This page is for job seekers only');
                navigateTo('dashboard');
                return;
            }
            window.location.href = basePath + 'features/user/applied_jobs.html';
            break;
            
        case 'add-job':
            if (!user) {
                navigateTo('login', { returnTo: 'add-job' });
                return;
            }
            if (!user.is_company) {
                showMessage('Access denied: This page is for company users only');
                navigateTo('search');
                return;
            }
            window.location.href = basePath + 'features/admin/add_job.html';
            break;
            
        case 'login':
            if (user) {
                console.log('User already logged in, redirecting to appropriate page');
                navigateTo(user.is_company ? 'dashboard' : 'search');
                return;
            }
            const returnTo = options.returnTo ? `?return=${encodeURIComponent(options.returnTo)}` : '';
            window.location.href = basePath + 'login.html' + returnTo;
            break;
            
        case 'signup':
            if (user) {
                console.log('User already logged in, redirecting to appropriate page');
                navigateTo(user.is_company ? 'dashboard' : 'search');
                return;
            }
            window.location.href = basePath + 'signup.html';
            break;
            
        case 'home':
            window.location.href = basePath + 'index.html';
            break;
            
        case 'logout':
            window.location.href = basePath + 'index.html';
            break;
            
        default:
            console.error('Unknown navigation target:', page);
            window.location.href = basePath + 'index.html';
    }
}

/**
 * Handle successful login - redirect to appropriate page
 * @param {object} user - User object from login response
 */
export function handleLoginSuccess(user) {
    console.log('Login successful, handling navigation for:', user.username);
    
    // Check for return URL parameter
    const urlParams = new URLSearchParams(window.location.search);
    const returnTo = urlParams.get('return');
    
    if (returnTo) {
        console.log('Returning to requested page:', returnTo);
        navigateTo(returnTo);
        return;
    }
    
    // Default navigation based on user type
    if (user.is_company) {
        navigateTo('dashboard');
    } else {
        navigateTo('search');
    }
}

/**
 * Handle successful registration - redirect to appropriate page
 * @param {object} user - User object from registration response
 */
export function handleRegistrationSuccess(user) {
    console.log('Registration successful, handling navigation for:', user.username);
    
    // Show success message
    showMessage('Registration successful! Welcome to JobSearch!', 'success');
    
    // Navigate to login page for now (can be changed to auto-login later)
    setTimeout(() => {
        navigateTo('login');
    }, 1500);
}

/**
 * Handle logout - clear session and redirect
 */
export function handleLogoutSuccess() {
    console.log('Logout successful, redirecting to home');
    showMessage('You have been logged out successfully', 'info');
    setTimeout(() => {
        navigateTo('home');
    }, 1000);
}

/**
 * Show a message to the user
 * @param {string} message - Message to show
 * @param {string} type - Message type ('success', 'error', 'info', 'warning')
 */
function showMessage(message, type = 'info') {
    // Create or get message container
    let messageContainer = document.getElementById('nav-message-container');
    if (!messageContainer) {
        messageContainer = document.createElement('div');
        messageContainer.id = 'nav-message-container';
        messageContainer.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            z-index: 10000;
            max-width: 300px;
        `;
        document.body.appendChild(messageContainer);
    }
    
    // Create message element
    const messageEl = document.createElement('div');
    messageEl.style.cssText = `
        padding: 12px 16px;
        margin-bottom: 10px;
        border-radius: 6px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.15);
        font-size: 14px;
        line-height: 1.4;
        animation: slideInRight 0.3s ease-out;
    `;
    
    // Set colors based on type
    const colors = {
        success: { bg: '#d4edda', text: '#155724', border: '#c3e6cb' },
        error: { bg: '#f8d7da', text: '#721c24', border: '#f5c6cb' },
        warning: { bg: '#fff3cd', text: '#856404', border: '#ffeaa7' },
        info: { bg: '#d1ecf1', text: '#0c5460', border: '#bee5eb' }
    };
    
    const color = colors[type] || colors.info;
    messageEl.style.backgroundColor = color.bg;
    messageEl.style.color = color.text;
    messageEl.style.border = `1px solid ${color.border}`;
    
    messageEl.textContent = message;
    messageContainer.appendChild(messageEl);
    
    // Auto remove after 3 seconds
    setTimeout(() => {
        if (messageEl.parentNode) {
            messageEl.style.animation = 'slideOutRight 0.3s ease-in';
            setTimeout(() => {
                if (messageEl.parentNode) {
                    messageEl.parentNode.removeChild(messageEl);
                }
            }, 300);
        }
    }, 3000);
}

// Add CSS animations
if (!document.getElementById('nav-animations')) {
    const style = document.createElement('style');
    style.id = 'nav-animations';
    style.textContent = `
        @keyframes slideInRight {
            from { transform: translateX(100%); opacity: 0; }
            to { transform: translateX(0); opacity: 1; }
        }
        @keyframes slideOutRight {
            from { transform: translateX(0); opacity: 1; }
            to { transform: translateX(100%); opacity: 0; }
        }
    `;
    document.head.appendChild(style);
}
