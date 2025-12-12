// This file will contain admin UI/modal logic split from admin.js

import { getCurrentUser } from './api.js';

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
    if (!user || !user.company) {
        showError(errorElement, 'You must be logged in as a company to add jobs');
        return;
    }
    const title = document.getElementById('job-title').value;
    const salary = document.getElementById('job-salary').value;
    const status = document.getElementById('job-status').value;
    const experience = document.getElementById('job-experience').value;
    const description = document.getElementById('job-description').value;
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
    const res = await fetch('http://localhost:8000/api/jobs/', {
        method: 'POST',
        credentials: 'include',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(newJob)
    });
    if (!res.ok) {
        showError(errorElement, 'Failed to add job');
        return;
    }
    window.location.href = 'dashboard.html';
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
    if (!user || !user.company) {
        showError(errorElement, 'You must be logged in as a company to edit jobs');
        return;
    }
    const jobId = document.getElementById('job-id').value;
    const title = document.getElementById('job-title').value;
    const salary = document.getElementById('job-salary').value;
    const status = document.getElementById('job-status').value;
    const experience = document.getElementById('job-experience').value;
    const description = document.getElementById('job-description').value;
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
    const res = await fetch(`http://localhost:8000/api/jobs/${jobId}/`, {
        method: 'PATCH',
        credentials: 'include',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(updatedJob)
    });
    if (!res.ok) {
        showError(errorElement, 'Failed to update job');
        return;
    }
    window.location.href = 'dashboard.html';
}
