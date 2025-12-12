// This file will contain admin job management logic split from admin.js

import { getCurrentUser } from './api.js';

// Load all jobs posted by the current company
export async function loadCompanyJobs() {
    const user = await getCurrentUser();
    const jobsContainer = document.getElementById('admin-jobs-container');
    const noJobsMessage = document.getElementById('no-jobs-message');
    if (!jobsContainer || !user || !user.company) return;
    // Get all jobs
    const allJobs = await getJobs();
    // Filter to only this company's jobs
    const companyJobs = allJobs.filter(job => job.company === user.company);
    if (companyJobs.length === 0) {
        if (noJobsMessage) noJobsMessage.style.display = 'block';
        return;
    }
    jobsContainer.innerHTML = '';
    companyJobs.forEach(job => {
        const jobCard = createJobCard(job);
        jobsContainer.appendChild(jobCard);
    });
}

// Create a DOM element for a job card
export function createJobCard(job) {
    const card = document.createElement('div');
    card.className = 'job-card';
    card.dataset.jobId = job.id;
    const headerDiv = document.createElement('div');
    headerDiv.className = 'job-card-header';
    const title = document.createElement('h3');
    title.className = 'job-title';
    title.textContent = job.title;
    const salary = document.createElement('span');
    salary.className = 'job-salary';
    salary.textContent = job.salary;
    headerDiv.appendChild(title);
    headerDiv.appendChild(salary);
    const bodyDiv = document.createElement('div');
    bodyDiv.className = 'job-card-body';
    const company = document.createElement('p');
    company.className = 'company-name';
    company.textContent = job.company;
    const experience = document.createElement('p');
    experience.className = 'job-experience';
    experience.textContent = `Experience: ${job.experience} years`;
    const description = document.createElement('p');
    description.className = 'job-description-preview';
    description.textContent = truncateText(job.description, 100);
    bodyDiv.appendChild(company);
    bodyDiv.appendChild(experience);
    bodyDiv.appendChild(description);
    const footerDiv = document.createElement('div');
    footerDiv.className = 'job-card-footer';
    const viewBtn = document.createElement('button');
    viewBtn.className = 'btn-view-details';
    viewBtn.textContent = 'View Details';
    viewBtn.onclick = function() {
        window.location.href = '../user/job_details.html?id=' + job.id;
    };
    const applicantsBtn = document.createElement('button');
    applicantsBtn.className = 'btn-primary';
    applicantsBtn.textContent = 'View Applicants';
    applicantsBtn.onclick = function() {
        window.location.href = `view_applicants.html?jobId=${job.id}`;
    };
    const adminActions = document.createElement('div');
    adminActions.className = 'admin-actions';
    const editBtn = document.createElement('button');
    editBtn.className = 'btn-edit';
    editBtn.textContent = 'Edit';
    editBtn.onclick = function() {
        editJob(job.id);
    };
    const deleteBtn = document.createElement('button');
    deleteBtn.className = 'btn-delete';
    deleteBtn.textContent = 'Delete';
    deleteBtn.onclick = async function() {
        await deleteJob(job.id);
    };
    adminActions.appendChild(editBtn);
    adminActions.appendChild(deleteBtn);
    footerDiv.appendChild(viewBtn);
    footerDiv.appendChild(applicantsBtn);
    footerDiv.appendChild(adminActions);
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
    if (!user || !user.company) return;
    const statusFilter = document.getElementById('status-filter');
    const jobSearch = document.getElementById('job-search');
    const status = statusFilter ? statusFilter.value : 'all';
    const searchTerm = jobSearch ? jobSearch.value.toLowerCase() : '';
    const allJobs = await getJobs();
    let filteredJobs = allJobs.filter(job => job.company === user.company);
    if (status !== 'all') {
        filteredJobs = filteredJobs.filter(job => job.status === status);
    }
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
        if (noJobsMessage) noJobsMessage.style.display = 'block';
        return;
    } else {
        if (noJobsMessage) noJobsMessage.style.display = 'none';
    }
    filteredJobs.forEach(job => {
        const jobCard = createJobCard(job);
        jobsContainer.appendChild(jobCard);
    });
}

// Edit job (redirect)
export function editJob(jobId) {
    window.location.href = 'edit_job.html?id=' + jobId;
}

// Delete job via API
export async function deleteJob(jobId) {
    if (!confirm('Are you sure you want to delete this job?')) return;
    const res = await fetch(`http://localhost:8000/api/jobs/${jobId}/`, {
        method: 'DELETE',
        credentials: 'include'
    });
    if (!res.ok) {
        console.error('Failed to delete job');
        return;
    }
    // Refresh the job list if on dashboard
    if (typeof loadCompanyJobs === 'function') await loadCompanyJobs();
}
