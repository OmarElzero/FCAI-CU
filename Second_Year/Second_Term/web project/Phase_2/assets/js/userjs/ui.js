import { getCurrentUser } from './api.js';
import { handleLogout } from './auth.js';
import { getRelativePathToRoot } from './utils.js';

function loadNavbar() {
    const navbarContainer = document.getElementById('navbar-container');
    if (!navbarContainer) return;

    const basePath = getRelativePathToRoot();

    fetch(`${basePath}components/navbar.html`)
        .then(response => response.text())
        .then(html => {
            navbarContainer.innerHTML = html;
            fixNavbarLinks();
            updateNavbarVisibility();
            setupNavbarEventListeners();
        })
        .catch(error => {
            console.error('Error loading navbar:', error);
        });
}

function fixNavbarLinks() {
    const basePath = getRelativePathToRoot();

    const navbarLinks = document.querySelectorAll('.navbar-menu a');
    navbarLinks.forEach(link => {
        const href = link.getAttribute('href');
        if (href && !href.startsWith('http') && !href.startsWith('/') && href !== '#') {
            link.setAttribute('href', basePath + href);
        }
    });

    const logoLink = document.querySelector('.logo');
    if (logoLink) {
        logoLink.setAttribute('href', basePath + 'index.html');
    }
}

async function updateNavbarVisibility() {
    const user = await getCurrentUser();
    

    setTimeout(() => {
        const userOnlyElements = document.querySelectorAll('.user-only');
        const adminOnlyElements = document.querySelectorAll('.admin-only');
        const loggedInOnlyElements = document.querySelectorAll('.logged-in-only');
        const loggedOutOnlyElements = document.querySelectorAll('.logged-out-only');

        const usernameDisplay = document.getElementById('username-display');
        if (usernameDisplay && user) {
            usernameDisplay.textContent = user.username;
        }

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
            userOnlyElements.forEach(el => el.style.display = 'block');
        }
    }, 100);
}

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
            handleLogout();
        });
    }

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

    getCurrentUser().then(user => {
        if (!user) {
            document.querySelectorAll('.user-only').forEach(el => {
                el.addEventListener('click', function(e) {
                    const href = this.getAttribute('href');
                    if (href) {
                        e.preventDefault();
                        window.location.href = basePath + 'login.html?redirect=' + encodeURIComponent(href);
                    }
                });
            });
        }
    });
}

export {
    loadNavbar,
    updateNavbarVisibility,
    setupNavbarEventListeners
};
