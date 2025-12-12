// This file will contain admin UI/modal logic split from admin.js

import { getCurrentUser, createJob, updateJob, getJobs } from './api.js';

// Utility functions
function showError(element, message) {
    if (element) {
        element.textContent = message;
        element.style.display = 'block';
    }
}

function clearError(element) {
    if (element) {
        element.textContent = '';
        element.style.display = 'none';
    }
}

function getUrlParams() {
    const params = {};
    const searchParams = new URLSearchParams(window.location.search);
    for (const [key, value] of searchParams) {
        params[key] = value;
    }
    return params;
}

function formatDate(dateString) {
    if (!dateString) return '';
    return new Date(dateString).toLocaleDateString();
}

// Initialize the add job form
export function initAddJobForm() {
    getCurrentUser().then(user => {
        const jobCompanyInput = document.getElementById('job-company');
        if (jobCompanyInput && user && user.company) {
            jobCompanyInput.value = user.company;
        }
        const addJobForm = document.getElementById('add-job-form');
        if (addJobForm) {
            addJobForm.addEventListener('submit', handleAddJob);
        }
    });
}

// Handle add job form submission
async function handleAddJob(e) {
    e.preventDefault();
    
    const user = await getCurrentUser();
    const errorElement = document.getElementById('add-job-error');
    
    // Clear previous errors
    clearError(errorElement);
    
    if (!user || !user.is_company) {
        showError(errorElement, 'You must be logged in as a company to add jobs');
        return;
    }
    
    const title = document.getElementById('job-title').value.trim();
    const salary = document.getElementById('job-salary').value.trim();
    const status = document.getElementById('job-status').value;
    const experience = document.getElementById('job-experience').value;
    const description = document.getElementById('job-description').value.trim();
    
    if (!title || !salary || !experience || !description) {
        showError(errorElement, 'All fields are required');
        return;
    }
    
    const newJob = {
        title,
        salary,
        company: user.company,
        status,
        experience: parseInt(experience, 10) || 0,
        description
    };
    
    try {
        console.log('Creating job:', newJob);
        const createdJob = await createJob(newJob);
        console.log('Job created successfully:', createdJob);
        
        // Redirect to dashboard with success message
        window.location.href = 'dashboard.html?success=job_added';
    } catch (error) {
        console.error('Failed to create job:', error);
        showError(errorElement, error.message || 'Failed to add job. Please try again.');
    }
}

// Initialize the edit job form
export async function initEditJobForm() {
    const params = getUrlParams();
    const jobId = params.id;
    if (!jobId) {
        window.location.href = 'dashboard.html';
        return;
    }
    const jobs = await getJobs();
    const job = jobs.find(j => j.id == jobId);
    if (!job) {
        window.location.href = 'dashboard.html';
        return;
    }
    document.getElementById('job-id').value = job.id;
    document.getElementById('job-title').value = job.title;
    document.getElementById('job-salary').value = job.salary;
    document.getElementById('job-company').value = job.company;
    document.getElementById('job-status').value = job.status;
    document.getElementById('job-experience').value = job.experience;
    document.getElementById('job-description').value = job.description;
    document.getElementById('job-created').value = formatDate(job.createdAt);
    const editJobForm = document.getElementById('edit-job-form');
    if (editJobForm) {
        editJobForm.addEventListener('submit', handleEditJob);
    }
}

// Handle edit job form submission
async function handleEditJob(e) {
    e.preventDefault();
    
    const user = await getCurrentUser();
    const errorElement = document.getElementById('edit-job-error');
    
    // Clear previous errors
    clearError(errorElement);
    
    if (!user || !user.is_company) {
        showError(errorElement, 'You must be logged in as a company to edit jobs');
        return;
    }
    
    const jobId = document.getElementById('job-id').value;
    const title = document.getElementById('job-title').value.trim();
    const salary = document.getElementById('job-salary').value.trim();
    const status = document.getElementById('job-status').value;
    const experience = document.getElementById('job-experience').value;
    const description = document.getElementById('job-description').value.trim();
    
    if (!jobId || !title || !salary || !experience || !description) {
        showError(errorElement, 'All fields are required');
        return;
    }
    
    const updatedJob = {
        title,
        salary,
        status,
        experience: parseInt(experience, 10) || 0,
        description
    };
    
    try {
        console.log('Updating job:', jobId, updatedJob);
        const result = await updateJob(jobId, updatedJob);
        console.log('Job updated successfully:', result);
        
        // Redirect to dashboard with success message
        window.location.href = 'dashboard.html?success=job_updated';
    } catch (error) {
        console.error('Failed to update job:', error);
        showError(errorElement, error.message || 'Failed to update job. Please try again.');
    }
}
