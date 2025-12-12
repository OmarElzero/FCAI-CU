// This file will contain admin dashboard logic split from admin.js

import { getCurrentUser } from './api.js';
import { loadCompanyJobs, setupJobFiltering } from './jobs.js';

// Initialize the admin dashboard
export async function initAdminDashboard() {
    console.log('🚀 Initializing admin dashboard...');
    
    try {
        const user = await getCurrentUser();
        console.log('👤 Current user:', user);
        
        const companyNameDisplay = document.getElementById('company-name-display');
        if (companyNameDisplay && user && user.company) {
            companyNameDisplay.textContent = `Managing jobs for ${user.company}`;
        }
        
        // Load company's jobs
        console.log('📋 Loading company jobs...');
        await loadCompanyJobs();
        
        // Setup filtering
        console.log('🔍 Setting up job filtering...');
        setupJobFiltering();
        
        console.log('✅ Admin dashboard initialized successfully');
    } catch (error) {
        console.error('❌ Failed to initialize admin dashboard:', error);
    }
}
