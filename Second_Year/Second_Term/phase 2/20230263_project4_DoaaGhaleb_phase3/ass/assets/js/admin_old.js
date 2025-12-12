// Admin JavaScript file for JobSearch Website

// DOM Content Loaded Event Listener
document.addEventListener('DOMContentLoaded', function() {
    // Check if user is admin
    const user = getCurrentUser();
    if (!user || user.role !== 'admin') {
        window.location.href = '/login.html';
        return;
    }
    
    // Initialize dashboard if on that page
    if (window.location.pathname.includes('dashboard.html')) {
        initAdminDashboard();
        initModal('job-details-modal');
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

// Initialize the admin dashboard
function initAdminDashboard() {
    const user = getCurrentUser();
    const companyNameDisplay = document.getElementById('company-name-display');
    
    if (companyNameDisplay && user && user.company) {
        companyNameDisplay.textContent = `Managing jobs for ${user.company}`;
    }
    
    // Load company's jobs
    loadCompanyJobs();
    
    // Setup filtering
    setupJobFiltering();
}

// Load all jobs posted by the current company
function loadCompanyJobs() {
    const user = getCurrentUser();
    const jobsContainer = document.getElementById('admin-jobs-container');
    const noJobsMessage = document.getElementById('no-jobs-message');
    
    if (!jobsContainer || !user || !user.company) return;
    
    // Get all jobs
    const allJobs = getJobs();
    
    // Filter to only this company's jobs
    const companyJobs = allJobs.filter(job => job.company === user.company);
    
    if (companyJobs.length === 0) {
        if (noJobsMessage) {
            noJobsMessage.style.display = 'block';
        }
        return;
    }
    
    // Clear container
    jobsContainer.innerHTML = '';
    
    // Add each job card
    companyJobs.forEach(job => {
        const jobCard = createJobCard(job);
        jobsContainer.appendChild(jobCard);
    });
}

// Create a DOM element for a job card
function createJobCard(job) {
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
        // Redirect to job details page
        window.location.href = '../user/job_details.html?id=' + job.id;
    };

    // Add View Applicants button for admin
    const applicantsBtn = document.createElement('button');
    applicantsBtn.className = 'btn-primary';
    applicantsBtn.textContent = 'View Applicants';
    applicantsBtn.onclick = function() {
        // Redirect to a dedicated admin view applicants page
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
    deleteBtn.onclick = function() {
        deleteJob(job.id);
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
function setupJobFiltering() {
    const statusFilter = document.getElementById('status-filter');
    const jobSearch = document.getElementById('job-search');
    
    // Apply filters when changed
    if (statusFilter) {
        statusFilter.addEventListener('change', applyJobFilters);
    }
    
    if (jobSearch) {
        jobSearch.addEventListener('input', applyJobFilters);
    }
}

// Apply filters to job listings
function applyJobFilters() {
    const user = getCurrentUser();
    if (!user || !user.company) return;
    
    const statusFilter = document.getElementById('status-filter');
    const jobSearch = document.getElementById('job-search');
    
    const status = statusFilter ? statusFilter.value : 'all';
    const searchTerm = jobSearch ? jobSearch.value.toLowerCase() : '';
    
    // Get all jobs
    const allJobs = getJobs();
    
    // Filter to this company's jobs and apply filters
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
    
    // Update the jobs display
    const jobsContainer = document.getElementById('admin-jobs-container');
    const noJobsMessage = document.getElementById('no-jobs-message');
    
    if (!jobsContainer) return;
    
    // Clear container
    jobsContainer.innerHTML = '';
    
    if (filteredJobs.length === 0) {
        if (noJobsMessage) {
            noJobsMessage.style.display = 'block';
        }
        return;
    } else {
        if (noJobsMessage) {
            noJobsMessage.style.display = 'none';
        }
    }
    
    // Add each job card
    filteredJobs.forEach(job => {
        const jobCard = createJobCard(job);
        jobsContainer.appendChild(jobCard);
    });
}

// Show job details in modal
function viewJobDetails(jobId) {
    const modal = document.getElementById('job-details-modal');
    const detailsContainer = document.getElementById('job-details-container');
    
    if (!modal || !detailsContainer) return;
    
    // Get job details
    const jobs = getJobs();
    const job = jobs.find(j => j.id === jobId);
    
    if (!job) return;
    
    // Populate job details
    detailsContainer.innerHTML = `
        <div class="job-details-header">
            <h2>${job.title}</h2>
            <span class="job-details-salary">${job.salary}</span>
        </div>
        <p class="job-details-company">
            <strong>Company:</strong> ${job.company}
        </p>
        <div class="job-details-info">
            <span><strong>Status:</strong> ${job.status}</span>
            <span><strong>Experience Required:</strong> ${job.experience} years</span>
            <span><strong>Posted:</strong> ${formatDate(job.createdAt)}</span>
        </div>
        <h3>Job Description:</h3>
        <div class="job-details-description">
            ${job.description.replace(/\n/g, '<br>')}
        </div>
    `;
    
    // Update modal action buttons
    const editJobBtn = document.getElementById('edit-job-btn');
    const deleteJobBtn = document.getElementById('delete-job-btn');
    
    if (editJobBtn) {
        editJobBtn.onclick = function() {
            editJob(jobId);
        };
    }
    
    if (deleteJobBtn) {
        deleteJobBtn.onclick = function() {
            if (confirm('Are you sure you want to delete this job?')) {
                deleteJob(jobId);
                modal.style.display = 'none';
            }
        };
    }
    
    // Show modal
    modal.style.display = 'block';

    // Add event for View Applicants button
    const viewApplicantsBtn = document.getElementById('view-applicants-btn');
    if (viewApplicantsBtn) {
        viewApplicantsBtn.onclick = function() {
            showApplicantsModal(jobId);
        };
    }
}

// Show applicants for a job in a modal
function showApplicantsModal(jobId) {
    const applicantsModal = document.getElementById('applicants-modal');
    const applicantsContainer = document.getElementById('applicants-container');
    if (!applicantsModal || !applicantsContainer) return;
    // Get all applications for this job
    const applications = getApplications().filter(app => app.jobId === jobId);
    if (applications.length === 0) {
        applicantsContainer.innerHTML = '<p>No applicants for this job yet.</p>';
    } else {
        // Get users for profile info
        const users = getUsers();
        applicantsContainer.innerHTML = '<h3>Applicants</h3>' + applications.map(app => {
            const user = users.find(u => u.id === app.userId);
            return `<div class="application-card">
                <div><strong>Name:</strong> ${user ? user.username : 'Unknown'}</div>
                <div><strong>Email:</strong> ${user ? user.email : 'Unknown'}</div>
                <div><strong>LinkedIn:</strong> ${user && user.linkedin ? `<a href='${user.linkedin}' target='_blank'>${user.linkedin}</a>` : 'N/A'}</div>
                <div><strong>CV:</strong> ${user && user.cvLink ? `<a href='${user.cvLink}' target='_blank'>CV Link</a>` : (user && user.cvFile ? `<a href='${user.cvFile}' target='_blank'>CV File</a>` : 'N/A')}</div>
                <div><strong>Status:</strong> <select data-app-id="${app.id}" class="app-status-select">
                    <option value="pending" ${app.status==='pending'?'selected':''}>Pending</option>
                    <option value="reviewed" ${app.status==='reviewed'?'selected':''}>Reviewed</option>
                    <option value="interviewed" ${app.status==='interviewed'?'selected':''}>Interviewed</option>
                    <option value="rejected" ${app.status==='rejected'?'selected':''}>Rejected</option>
                </select></div>
                <div><strong>Applied on:</strong> ${formatDate(app.appliedAt)}</div>
            </div>`;
        }).join('');
    }
    // Add event listeners for status change
    setTimeout(() => {
        document.querySelectorAll('.app-status-select').forEach(select => {
            select.addEventListener('change', function() {
                const appId = this.getAttribute('data-app-id');
                updateApplicationStatus(appId, this.value);
            });
        });
    }, 100);
    applicantsModal.style.display = 'block';
}

// Update application status
function updateApplicationStatus(appId, newStatus) {
    const applications = getApplications();
    const idx = applications.findIndex(app => app.id === appId);
    if (idx !== -1) {
        applications[idx].status = newStatus;
        localStorage.setItem('applications', JSON.stringify(applications));
    }
}

// Initialize the add job form
function initAddJobForm() {
    const user = getCurrentUser();
    const jobCompanyInput = document.getElementById('job-company');
    
    // Set company name (readonly field)
    if (jobCompanyInput && user && user.company) {
        jobCompanyInput.value = user.company;
    }
    
    // Setup form submission
    const addJobForm = document.getElementById('add-job-form');
    if (addJobForm) {
        addJobForm.addEventListener('submit', handleAddJob);
    }
}

// Handle add job form submission
function handleAddJob(e) {
    e.preventDefault();
    const user = getCurrentUser();
    const errorElement = document.getElementById('add-job-error');
    
    if (!user || !user.company) {
        showError(errorElement, 'You must be logged in as a company to add jobs');
        return;
    }
    
    // Get form values
    const title = document.getElementById('job-title').value;
    const salary = document.getElementById('job-salary').value;
    const status = document.getElementById('job-status').value;
    const experience = document.getElementById('job-experience').value;
    const description = document.getElementById('job-description').value;
    
    // Validate inputs
    if (!title || !salary || !experience || !description) {
        showError(errorElement, 'All fields are required');
        return;
    }
    
    // Create new job object
    const newJob = {
        id: generateId(),
        title,
        salary,
        company: user.company,
        status,
        experience: parseInt(experience, 10) || 0,
        description,
        createdAt: new Date().toISOString(),
        updatedAt: new Date().toISOString(),
        createdBy: user.id
    };
    
    // Add to jobs array
    const jobs = getJobs();
    jobs.push(newJob);
    localStorage.setItem('jobs', JSON.stringify(jobs));
    
    // Redirect to dashboard
    window.location.href = 'dashboard.html';
}

// Initialize the edit job form
function initEditJobForm() {
    // Get job ID from URL
    const params = getUrlParams();
    const jobId = params.id;
    
    if (!jobId) {
        window.location.href = 'dashboard.html';
        return;
    }
    
    // Get job details
    const jobs = getJobs();
    const job = jobs.find(j => j.id === jobId);
    
    if (!job) {
        window.location.href = 'dashboard.html';
        return;
    }
    
    // Populate form
    document.getElementById('job-id').value = job.id;
    document.getElementById('job-title').value = job.title;
    document.getElementById('job-salary').value = job.salary;
    document.getElementById('job-company').value = job.company;
    document.getElementById('job-status').value = job.status;
    document.getElementById('job-experience').value = job.experience;
    document.getElementById('job-description').value = job.description;
    document.getElementById('job-created').value = formatDate(job.createdAt);
    
    // Setup form submission
    const editJobForm = document.getElementById('edit-job-form');
    if (editJobForm) {
        editJobForm.addEventListener('submit', handleEditJob);
    }
}

// Handle edit job form submission
function handleEditJob(e) {
    e.preventDefault();
    const user = getCurrentUser();
    const errorElement = document.getElementById('edit-job-error');
    
    if (!user || !user.company) {
        showError(errorElement, 'You must be logged in as a company to edit jobs');
        return;
    }
    
    // Get form values
    const jobId = document.getElementById('job-id').value;
    const title = document.getElementById('job-title').value;
    const salary = document.getElementById('job-salary').value;
    const status = document.getElementById('job-status').value;
    const experience = document.getElementById('job-experience').value;
    const description = document.getElementById('job-description').value;
    
    // Validate inputs
    if (!jobId || !title || !salary || !experience || !description) {
        showError(errorElement, 'All fields are required');
        return;
    }
    
    // Get all jobs
    const jobs = getJobs();
    const jobIndex = jobs.findIndex(j => j.id === jobId);
    
    if (jobIndex === -1) {
        showError(errorElement, 'Job not found');
        return;
    }
    
    // Ensure user owns this job
    if (jobs[jobIndex].company !== user.company) {
        showError(errorElement, 'You do not have permission to edit this job');
        return;
    }
    
    // Update job
    jobs[jobIndex] = {
        ...jobs[jobIndex],
        title,
        salary,
        status,
        experience: parseInt(experience, 10) || 0,
        description,
        updatedAt: new Date().toISOString()
    };
    
    // Save changes
    localStorage.setItem('jobs', JSON.stringify(jobs));
    
    // Redirect to dashboard
    window.location.href = 'dashboard.html';
}

// Initialize applicants modal close button
setTimeout(() => {
    const applicantsModal = document.getElementById('applicants-modal');
    if (applicantsModal) {
        const closeBtn = applicantsModal.querySelector('.close-modal');
        if (closeBtn) {
            closeBtn.onclick = () => { applicantsModal.style.display = 'none'; };
        }
        window.addEventListener('click', (event) => {
            if (event.target === applicantsModal) {
                applicantsModal.style.display = 'none';
            }
        });
    }
}, 500);

// Expose editJob and deleteJob globally for inline HTML usage
window.editJob = function(jobId) {
    // Redirect to edit job page with job ID
    window.location.href = 'edit_job.html?id=' + jobId;
};
window.deleteJob = function(jobId) {
    if (!confirm('Are you sure you want to delete this job?')) return;
    const user = getCurrentUser();
    if (!user || !user.company) return;
    let jobs = getJobs();
    jobs = jobs.filter(j => j.id !== jobId || j.company !== user.company);
    localStorage.setItem('jobs', JSON.stringify(jobs));
    // Refresh the job list if on dashboard
    if (typeof loadCompanyJobs === 'function') loadCompanyJobs();
    // Optionally, remove the card from DOM directly if needed
};