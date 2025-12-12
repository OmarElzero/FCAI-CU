// Authentication check for protected pages
import { checkAuth } from './auth.js';

// Run the authentication check without redirects
document.addEventListener('DOMContentLoaded', function() {
    checkAuth({
        requireAuth: false, // Don't enforce auth requirements here
        requireCompany: false,
        requireJobSeeker: false,
        onAuthenticated: setupPage // Call setupPage function when authentication is successful
    });
});

/**
 * Set up the page with user information after authentication
 * @param {Object} user - User object from the API
 */
function setupPage(user) {
    // Update UI elements with user info
    const userNameElements = document.querySelectorAll('.user-name');
    userNameElements.forEach(element => {
        element.textContent = user.username;
    });
    
    // Update company name display for company users
    const companyNameDisplay = document.getElementById('company-name-display');
    if (companyNameDisplay && user.is_company && user.company) {
        companyNameDisplay.textContent = `Welcome, ${user.company}`;
    }
    
    // Show/hide elements based on user role
    if (user.is_company) {
        document.body.classList.add('company-user');
        document.querySelectorAll('.company-only').forEach(el => {
            el.style.display = 'block';
        });
        document.querySelectorAll('.job-seeker-only').forEach(el => {
            el.style.display = 'none';
        });
    } else {
        document.body.classList.add('job-seeker');
        document.querySelectorAll('.company-only').forEach(el => {
            el.style.display = 'none';
        });
        document.querySelectorAll('.job-seeker-only').forEach(el => {
            el.style.display = 'block';
        });
    }
}
