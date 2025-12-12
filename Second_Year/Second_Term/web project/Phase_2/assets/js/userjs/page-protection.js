// Page protection system - checks auth and redirects if needed
import { getCurrentUser } from './api.js';
import { navigateTo } from './navigation.js';

/**
 * Protect a page with authentication and role requirements
 * @param {object} options - Protection options
 * @param {boolean} options.requireAuth - Require user to be logged in
 * @param {boolean} options.requireCompany - Require user to be a company
 * @param {boolean} options.requireJobSeeker - Require user to be a job seeker
 * @param {string} options.redirectTo - Where to redirect if requirements not met
 */
export async function protectPage(options = {}) {
    const {
        requireAuth = false,
        requireCompany = false,
        requireJobSeeker = false,
        redirectTo = null
    } = options;
    
    const user = await getCurrentUser();
    const currentPath = window.location.pathname;
    
    console.log('Page protection check:', {
        path: currentPath,
        user: user?.username,
        isCompany: user?.is_company,
        requirements: { requireAuth, requireCompany, requireJobSeeker }
    });
    
    // Check authentication requirement
    if (requireAuth && !user) {
        console.log('Auth required but user not logged in');
        const returnPage = getReturnPageFromPath(currentPath);
        navigateTo('login', { returnTo: returnPage });
        return false;
    }
    
    // Check company requirement
    if (requireCompany && (!user || !user.is_company)) {
        console.log('Company role required but user is not a company');
        if (!user) {
            navigateTo('login', { returnTo: 'dashboard' });
        } else {
            navigateTo(redirectTo || 'search');
        }
        return false;
    }
    
    // Check job seeker requirement
    if (requireJobSeeker && (!user || user.is_company)) {
        console.log('Job seeker role required but user is a company');
        if (!user) {
            navigateTo('login', { returnTo: 'search' });
        } else {
            navigateTo(redirectTo || 'dashboard');
        }
        return false;
    }
    
    // All checks passed
    console.log('Page protection passed');
    return true;
}

/**
 * Get the return page identifier from a file path
 * @param {string} path - Current page path
 * @returns {string} - Return page identifier
 */
function getReturnPageFromPath(path) {
    if (path.includes('/admin/dashboard')) return 'dashboard';
    if (path.includes('/admin/add_job')) return 'add-job';
    if (path.includes('/admin/')) return 'dashboard';
    if (path.includes('/user/search_jobs')) return 'search';
    if (path.includes('/user/applied_jobs')) return 'applied';
    if (path.includes('/user/')) return 'search';
    return 'home';
}

/**
 * Setup page protection on DOM ready
 * @param {object} options - Protection options
 */
export function setupPageProtection(options = {}) {
    document.addEventListener('DOMContentLoaded', async function() {
        const isProtected = await protectPage(options);
        
        if (isProtected) {
            // Update UI based on user status
            const user = await getCurrentUser();
            if (user) {
                document.body.classList.add('authenticated');
                if (user.is_company) {
                    document.body.classList.add('company-user');
                } else {
                    document.body.classList.add('job-seeker');
                }
            }
        }
    });
}
