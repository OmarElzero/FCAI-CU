// This file will contain admin dashboard logic split from admin.js

import { getCurrentUser } from './api.js';
import { loadCompanyJobs, setupJobFiltering } from './jobs.js';

// Initialize the admin dashboard
export async function initAdminDashboard() {
    const user = await getCurrentUser();
    const companyNameDisplay = document.getElementById('company-name-display');
    if (companyNameDisplay && user && user.company) {
        companyNameDisplay.textContent = `Managing jobs for ${user.company}`;
    }
    // Load company's jobs
    await loadCompanyJobs();
    // Setup filtering
    setupJobFiltering();
}
