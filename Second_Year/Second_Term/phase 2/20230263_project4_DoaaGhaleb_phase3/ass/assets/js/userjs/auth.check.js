// Authentication check for protected pages
import { checkAuth } from '../../assets/js/userjs/auth.js';

// Check if the current page is a company-only page
const isCompanyPage = window.location.pathname.includes('/admin/');

// Check if the current page is a job seeker-only page
const isJobSeekerPage = window.location.pathname.includes('/user/');

// Run the authentication check with appropriate requirements
document.addEventListener('DOMContentLoaded', function() {
    checkAuth({
        requireAuth: true, // All protected pages require authentication
        requireCompany: isCompanyPage, // Company-only pages require company role
        requireJobSeeker: isJobSeekerPage, // Job seeker-only pages require job seeker role
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
