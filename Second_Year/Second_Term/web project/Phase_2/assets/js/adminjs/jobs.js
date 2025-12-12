// This file will contain admin job management logic split from admin.js

import { getCurrentUser, apiRequest } from './api.js';

// Get all jobs from API
export async function getJobs() {
    try {
        const jobs = await apiRequest('jobs/');
        return jobs || [];
    } catch (error) {
        console.error('Failed to fetch jobs:', error);
        return [];
    }
}

// Get company-specific jobs
export async function getCompanyJobs() {
    try {
        const jobs = await apiRequest('jobs/company_jobs/');
        return jobs || [];
    } catch (error) {
        console.error('Failed to fetch company jobs:', error);
        return [];
    }
}

// Load all jobs posted by the current company
export async function loadCompanyJobs() {
    const user = await getCurrentUser();
    const jobsContainer = document.getElementById('admin-jobs-container');
    const noJobsMessage = document.getElementById('no-jobs-message');
    
    if (!jobsContainer) {
        console.error('Jobs container not found');
        return;
    }
    
    if (!user || !user.is_company) {
        console.error('User is not a company admin');
        return;
    }
    
    try {
        // Try to get company-specific jobs first
        let companyJobs = await getCompanyJobs();
        
        // If that fails, get all jobs and filter by company
        if (!companyJobs || companyJobs.length === 0) {
            const allJobs = await getJobs();
            companyJobs = allJobs.filter(job => job.company === user.company);
        }
        
        console.log('Company jobs loaded:', companyJobs);
        
        if (companyJobs.length === 0) {
            if (noJobsMessage) noJobsMessage.style.display = 'block';
            jobsContainer.innerHTML = '';
            return;
        }
        
        if (noJobsMessage) noJobsMessage.style.display = 'none';
        jobsContainer.innerHTML = '';
        
        companyJobs.forEach(job => {
            const jobCard = createJobCard(job);
            jobsContainer.appendChild(jobCard);
        });
        
        console.log(`Loaded ${companyJobs.length} jobs for ${user.company}`);
    } catch (error) {
        console.error('Error loading company jobs:', error);
        if (noJobsMessage) {
            noJobsMessage.textContent = 'Error loading jobs. Please try again.';
            noJobsMessage.style.display = 'block';
        }
    }
}

// Create a DOM element for a job card
export function createJobCard(job) {
    console.log('Creating job card for:', job);
    
    const card = document.createElement('div');
    card.className = 'job-card';
    card.dataset.jobId = job.id;
    
    // Header section
    const headerDiv = document.createElement('div');
    headerDiv.className = 'job-card-header';
    
    const title = document.createElement('h3');
    title.className = 'job-title';
    title.textContent = job.title || 'Untitled Job';
    
    const salary = document.createElement('span');
    salary.className = 'job-salary';
    salary.textContent = job.salary || 'Salary not specified';
    
    headerDiv.appendChild(title);
    headerDiv.appendChild(salary);
    
    // Body section
    const bodyDiv = document.createElement('div');
    bodyDiv.className = 'job-card-body';
    
    const company = document.createElement('p');
    company.className = 'company-name';
    company.textContent = job.company || 'Unknown Company';
    
    const experience = document.createElement('p');
    experience.className = 'job-experience';
    experience.textContent = `Experience: ${job.experience || 0} years`;
    
    const description = document.createElement('p');
    description.className = 'job-description-preview';
    description.textContent = truncateText(job.description || 'No description available', 100);
    
    const status = document.createElement('p');
    status.className = 'job-status';
    status.textContent = `Status: ${job.status || 'Unknown'}`;
    status.style.fontWeight = 'bold';
    status.style.color = job.status === 'Open' ? '#28a745' : '#dc3545';
    
    bodyDiv.appendChild(company);
    bodyDiv.appendChild(experience);
    bodyDiv.appendChild(description);
    bodyDiv.appendChild(status);
    
    // Footer section with actions
    const footerDiv = document.createElement('div');
    footerDiv.className = 'job-card-footer';
    
    const viewBtn = document.createElement('button');
    viewBtn.className = 'btn btn-secondary';
    viewBtn.textContent = 'View Details';
    viewBtn.onclick = function() {
        window.location.href = `../user/job_details.html?id=${job.id}`;
    };
    
    const applicantsBtn = document.createElement('button');
    applicantsBtn.className = 'btn btn-primary';
    applicantsBtn.textContent = 'View Applicants';
    applicantsBtn.onclick = function() {
        window.location.href = `view_applicants.html?jobId=${job.id}`;
    };
    
    const adminActions = document.createElement('div');
    adminActions.className = 'admin-actions';
    adminActions.style.marginTop = '10px';
    
    const editBtn = document.createElement('button');
    editBtn.className = 'btn btn-warning';
    editBtn.textContent = 'Edit';
    editBtn.style.marginRight = '5px';
    editBtn.onclick = function() {
        editJob(job.id);
    };
    
    const deleteBtn = document.createElement('button');
    deleteBtn.className = 'btn btn-danger';
    deleteBtn.textContent = 'Delete';
    deleteBtn.onclick = async function() {
        await deleteJob(job.id);
    };
    
    adminActions.appendChild(editBtn);
    adminActions.appendChild(deleteBtn);
    
    footerDiv.appendChild(viewBtn);
    footerDiv.appendChild(applicantsBtn);
    footerDiv.appendChild(adminActions);
    
    // Assemble the card
    card.appendChild(headerDiv);
    card.appendChild(bodyDiv);
    card.appendChild(footerDiv);
    
    return card;
}

// Setup job filtering for the dashboard
export function setupJobFiltering() {
    const statusFilter = document.getElementById('status-filter');
    const jobSearch = document.getElementById('job-search');
    if (statusFilter) {
        statusFilter.addEventListener('change', applyJobFilters);
    }
    if (jobSearch) {
        jobSearch.addEventListener('input', applyJobFilters);
    }
}

// Apply filters to job listings
export async function applyJobFilters() {
    const user = await getCurrentUser();
    if (!user || !user.is_company) return;
    
    const statusFilter = document.getElementById('status-filter');
    const jobSearch = document.getElementById('job-search');
    const status = statusFilter ? statusFilter.value : 'all';
    const searchTerm = jobSearch ? jobSearch.value.toLowerCase() : '';
    
    try {
        // Get company jobs
        let companyJobs = await getCompanyJobs();
        
        // If that fails, get all jobs and filter by company
        if (!companyJobs || companyJobs.length === 0) {
            const allJobs = await getJobs();
            companyJobs = allJobs.filter(job => job.company === user.company);
        }
        
        let filteredJobs = [...companyJobs];
        
        // Apply status filter
        if (status !== 'all') {
            filteredJobs = filteredJobs.filter(job => job.status === status);
        }
        
        // Apply search filter
        if (searchTerm) {
            filteredJobs = filteredJobs.filter(job => 
                job.title.toLowerCase().includes(searchTerm) || 
                job.description.toLowerCase().includes(searchTerm)
            );
        }
        
        const jobsContainer = document.getElementById('admin-jobs-container');
        const noJobsMessage = document.getElementById('no-jobs-message');
        
        if (!jobsContainer) return;
        
        jobsContainer.innerHTML = '';
        
        if (filteredJobs.length === 0) {
            if (noJobsMessage) {
                noJobsMessage.textContent = searchTerm || status !== 'all' 
                    ? 'No jobs match your filters.' 
                    : 'No jobs found. Create your first job listing!';
                noJobsMessage.style.display = 'block';
            }
            return;
        } else {
            if (noJobsMessage) noJobsMessage.style.display = 'none';
        }
        
        filteredJobs.forEach(job => {
            const jobCard = createJobCard(job);
            jobsContainer.appendChild(jobCard);
        });
        
        console.log(`Filtered to ${filteredJobs.length} jobs`);
    } catch (error) {
        console.error('Error filtering jobs:', error);
    }
}

// Edit job (redirect)
export function editJob(jobId) {
    window.location.href = 'edit_job.html?id=' + jobId;
}

// Delete job via API
export async function deleteJob(jobId) {
    if (!confirm('Are you sure you want to delete this job?')) return;
    
    try {
        const result = await apiRequest(`jobs/${jobId}/`, {
            method: 'DELETE'
        });
        
        console.log('Job deleted successfully');
        
        // Refresh the job list
        await loadCompanyJobs();
        
    } catch (error) {
        console.error('Failed to delete job:', error);
        alert('Failed to delete job. Please try again.');
    }
}

// Debug function to test job loading
window.debugAdminJobs = async function() {
    console.log('=== ADMIN JOBS DEBUG ===');
    
    try {
        const user = await getCurrentUser();
        console.log('Current user:', user);
        
        if (!user || !user.is_company) {
            console.log('❌ User is not a company admin');
            return;
        }
        
        console.log('Fetching company jobs...');
        const companyJobs = await getCompanyJobs();
        console.log('Company jobs from API:', companyJobs);
        
        console.log('Fetching all jobs...');
        const allJobs = await getJobs();
        console.log('All jobs from API:', allJobs);
        
        const filteredJobs = allJobs.filter(job => job.company === user.company);
        console.log('Filtered jobs for company:', filteredJobs);
        
        console.log('Loading jobs in dashboard...');
        await loadCompanyJobs();
        
        console.log('=== DEBUG COMPLETE ===');
        return { user, companyJobs, allJobs, filteredJobs };
    } catch (error) {
        console.error('Debug failed:', error);
        return null;
    }
};

// Utility function to truncate text
function truncateText(text, maxLength) {
    if (!text) return '';
    if (text.length <= maxLength) return text;
    return text.substring(0, maxLength) + '...';
}
