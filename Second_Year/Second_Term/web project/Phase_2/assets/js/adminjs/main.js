// This file will contain the main entry point for admin logic (DOMContentLoaded, routing, etc.)

import { initAdminDashboard } from './dashboard.js';
import { initAddJobForm, initEditJobForm } from './ui.js';
import { getCurrentUser } from './api.js';

// DOM Content Loaded Event Listener

document.addEventListener('DOMContentLoaded', async function() {
    // Check if user is admin
    const user = await getCurrentUser();
    // if (!user || user.role !== 'admin') {
    //     window.location.href = '/login.html';
    //     return;
    // }
    // Initialize dashboard if on that page
    if (window.location.pathname.includes('dashboard.html')) {
        await initAdminDashboard();
        // Optionally: initModal('job-details-modal');
    }
    // Initialize add job form if on that page
    if (window.location.pathname.includes('add_job.html')) {
        initAddJobForm();
    }
    // Initialize edit job form if on that page
    if (window.location.pathname.includes('edit_job.html')) {
        initEditJobForm();
    }
});
