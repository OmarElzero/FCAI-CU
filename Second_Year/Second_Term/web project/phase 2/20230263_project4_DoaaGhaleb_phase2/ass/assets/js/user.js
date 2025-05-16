// User JavaScript file for JobSearch Website

// DOM Content Loaded Event Listener
document.addEventListener('DOMContentLoaded', function() {
    // Check if user is logged in
    const user = getCurrentUser();
    
    // Initialize search jobs page if on that page
    if (window.location.pathname.includes('search_jobs.html')) {
        initSearchJobs();
        initModal('job-details-modal');
    }
    
    // Initialize applied jobs page if on that page
    if (window.location.pathname.includes('applied_jobs.html')) {
        if (!user) {
            window.location.href = '/login.html?redirect=' + encodeURIComponent(window.location.pathname);
            return;
        }
        initAppliedJobs();
        initModal('application-details-modal');
    }
});

// Initialize the job search page
function initSearchJobs() {
    // Load all available jobs
    loadAvailableJobs();
    
    // Load companies for filter
    loadCompaniesFilter();
    
    // Setup search and filter functionality
    setupSearchFilters();
}

// Load all open jobs
function loadAvailableJobs() {
    const jobsContainer = document.getElementById('search-results-container');
    const noResultsMessage = document.getElementById('no-results-message');
    const resultsCount = document.getElementById('results-count');
    
    if (!jobsContainer) return;
    
    // Get all jobs
    const allJobs = getJobs();
    
    // Filter to only open jobs
    const openJobs = allJobs.filter(job => job.status === 'Open');
    
    if (openJobs.length === 0) {
        if (noResultsMessage) {
            noResultsMessage.style.display = 'block';
        }
        if (resultsCount) {
            resultsCount.textContent = '0 jobs found';
        }
        return;
    }
    
    // Update results count
    if (resultsCount) {
        resultsCount.textContent = `${openJobs.length} jobs found`;
    }
    
    // Clear container
    jobsContainer.innerHTML = '';
    
    // Get user's applications
    const user = getCurrentUser();
    const applications = user ? getApplications().filter(app => app.userId === user.id) : [];
    const appliedJobIds = applications.map(app => app.jobId);
    
    // Add each job card
    openJobs.forEach(job => {
        // Check if user has applied
        job.applied = appliedJobIds.includes(job.id);
        const jobCard = createJobCard(job);
        jobsContainer.appendChild(jobCard);
    });
}

// Load companies for the company filter dropdown
function loadCompaniesFilter() {
    const companyFilter = document.getElementById('company-filter');
    if (!companyFilter) return;
    
    // Get all jobs
    const allJobs = getJobs();
    
    // Get unique companies
    const companies = [...new Set(allJobs.map(job => job.company))];
    
    // Clear existing options (except the first)
    while (companyFilter.options.length > 1) {
        companyFilter.remove(1);
    }
    
    // Add company options
    companies.forEach(company => {
        const option = document.createElement('option');
        option.value = company;
        option.textContent = company;
        companyFilter.appendChild(option);
    });
}

// Setup job search and filter functionality
function setupSearchFilters() {
    const jobKeyword = document.getElementById('job-keyword');
    const experienceFilter = document.getElementById('experience-filter');
    const companyFilter = document.getElementById('company-filter');
    const searchButton = document.getElementById('search-button');
    
    // Apply filters when search button is clicked
    if (searchButton) {
        searchButton.addEventListener('click', applyJobFilters);
    }
    
    // Apply filters when Enter key is pressed in the search box
    if (jobKeyword) {
        jobKeyword.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                applyJobFilters();
            }
        });
    }
}

// Apply filters to job listings
function applyJobFilters() {
    const jobKeyword = document.getElementById('job-keyword');
    const experienceFilter = document.getElementById('experience-filter');
    const companyFilter = document.getElementById('company-filter');
    
    const keyword = jobKeyword ? jobKeyword.value.toLowerCase() : '';
    const experience = experienceFilter ? experienceFilter.value : '';
    const company = companyFilter ? companyFilter.value : '';
    
    // Get all jobs
    const allJobs = getJobs();
    
    // Filter to only open jobs
    let filteredJobs = allJobs.filter(job => job.status === 'Open');
    
    // Apply keyword filter
    if (keyword) {
        filteredJobs = filteredJobs.filter(job => 
            job.title.toLowerCase().includes(keyword) || 
            job.description.toLowerCase().includes(keyword)
        );
    }
    
    // Apply experience filter
    if (experience) {
        const minExperience = parseInt(experience, 10);
        filteredJobs = filteredJobs.filter(job => job.experience >= minExperience);
    }
    
    // Apply company filter
    if (company) {
        filteredJobs = filteredJobs.filter(job => job.company === company);
    }
    
    // Update the jobs display
    const jobsContainer = document.getElementById('search-results-container');
    const noResultsMessage = document.getElementById('no-results-message');
    const resultsCount = document.getElementById('results-count');
    
    if (!jobsContainer) return;
    
    // Clear container
    jobsContainer.innerHTML = '';
    
    // Update results count
    if (resultsCount) {
        resultsCount.textContent = `${filteredJobs.length} jobs found`;
    }
    
    if (filteredJobs.length === 0) {
        if (noResultsMessage) {
            noResultsMessage.style.display = 'block';
        }
        return;
    } else {
        if (noResultsMessage) {
            noResultsMessage.style.display = 'none';
        }
    }
    
    // Get user's applications
    const user = getCurrentUser();
    const applications = user ? getApplications().filter(app => app.userId === user.id) : [];
    const appliedJobIds = applications.map(app => app.jobId);
    
    // Add each job card
    filteredJobs.forEach(job => {
        // Check if user has applied
        job.applied = appliedJobIds.includes(job.id);
        const jobCard = createJobCard(job);
        jobsContainer.appendChild(jobCard);
    });
}

// Create a DOM element for a job card
function createJobCard(job) {
    const user = getCurrentUser();
    
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
        window.location.href = `job_details.html?id=${job.id}`;
    };
    
    footerDiv.appendChild(viewBtn);
    
    card.appendChild(headerDiv);
    card.appendChild(bodyDiv);
    card.appendChild(footerDiv);
    
    return card;
}

// Show job details in modal
function viewJobDetails(jobId) {
    const modal = document.getElementById('job-details-modal');
    const detailsContainer = document.getElementById('job-details-container');
    const applyBtn = document.getElementById('apply-job-btn');
    
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
            <span><strong>Experience Required:</strong> ${job.experience} years</span>
            <span><strong>Posted:</strong> ${formatDate(job.createdAt)}</span>
        </div>
        <h3>Job Description:</h3>
        <div class="job-details-description">
            ${job.description.replace(/\n/g, '<br>')}
        </div>
    `;
    
    // Update apply button
    if (applyBtn) {
        const user = getCurrentUser();
        const applications = user ? getApplications().filter(app => app.userId === user.id) : [];
        const hasApplied = applications.some(app => app.jobId === jobId);
        
        if (!user || user.role !== 'user') {
            applyBtn.style.display = 'none';
        } else {
            applyBtn.style.display = 'inline-block';
            
            if (hasApplied) {
                applyBtn.textContent = 'Already Applied';
                applyBtn.disabled = true;
            } else {
                applyBtn.textContent = 'Apply Now';
                applyBtn.disabled = false;
                applyBtn.onclick = function() {
                    applyToJob(jobId);
                    modal.style.display = 'none';
                };
            }
        }
    }
    
    // Show modal
    modal.style.display = 'block';
}

// Apply to a job
function applyToJob(jobId) {
    const user = getCurrentUser();
    
    if (!user) {
        window.location.href = '/login.html?redirect=' + encodeURIComponent(window.location.pathname);
        return;
    }
    
    if (user.role !== 'user') {
        alert('Only job seekers can apply to jobs');
        return;
    }
    
    // Get job details
    const jobs = getJobs();
    const job = jobs.find(j => j.id === jobId);
    
    if (!job) return;
    
    // Check if already applied
    const applications = getApplications();
    if (applications.some(app => app.jobId === jobId && app.userId === user.id)) {
        alert('You have already applied to this job');
        return;
    }
    
    // Create new application
    const newApplication = {
        id: generateId(),
        userId: user.id,
        jobId: job.id,
        jobTitle: job.title,
        company: job.company,
        status: 'pending',
        appliedAt: new Date().toISOString()
    };
    
    // Add to applications
    applications.push(newApplication);
    localStorage.setItem('applications', JSON.stringify(applications));
    
    // Update UI
    alert('Successfully applied to ' + job.title);
    
    // Refresh job listings if on search page
    if (window.location.pathname.includes('search_jobs.html')) {
        loadAvailableJobs();
    }
}

// Initialize the applied jobs page
function initAppliedJobs() {
    const user = getCurrentUser();
    
    if (!user) return;
    
    // Load user's applications
    loadUserApplications();
    
    // Setup filtering
    setupApplicationFiltering();
}

// Load all applications for the current user
function loadUserApplications() {
    const user = getCurrentUser();
    const applicationsContainer = document.getElementById('applications-container');
    const noApplicationsMessage = document.getElementById('no-applications-message');
    
    if (!applicationsContainer || !user) return;
    
    // Get all applications for this user
    const applications = getApplications().filter(app => app.userId === user.id);
    
    if (applications.length === 0) {
        if (noApplicationsMessage) {
            noApplicationsMessage.style.display = 'block';
        }
        return;
    }
    
    // Clear container
    applicationsContainer.innerHTML = '';
    
    // Add each application
    applications.forEach(application => {
        const applicationCard = createApplicationCard(application);
        applicationsContainer.appendChild(applicationCard);
    });
}

// Create a DOM element for an application card
function createApplicationCard(application) {
    const card = document.createElement('div');
    card.className = 'application-card';
    card.dataset.applicationId = application.id;
    
    const infoDiv = document.createElement('div');
    infoDiv.className = 'application-info';
    
    const title = document.createElement('h3');
    title.className = 'application-title';
    title.textContent = application.jobTitle;
    
    const company = document.createElement('p');
    company.className = 'application-company';
    company.textContent = application.company;
    
    const date = document.createElement('p');
    date.className = 'application-date';
    date.textContent = `Applied on: ${formatDate(application.appliedAt)}`;
    
    infoDiv.appendChild(title);
    infoDiv.appendChild(company);
    infoDiv.appendChild(date);
    
    const statusSpan = document.createElement('span');
    statusSpan.className = `application-status status-${application.status}`;
    statusSpan.textContent = capitalizeFirstLetter(application.status);
    
    card.appendChild(infoDiv);
    card.appendChild(statusSpan);
    
    // Add click event to show details
    card.addEventListener('click', function() {
        viewApplicationDetails(application.id);
    });
    
    return card;
}

// Setup application filtering
function setupApplicationFiltering() {
    const statusFilter = document.getElementById('application-status-filter');
    const searchInput = document.getElementById('applications-search');
    
    if (statusFilter) {
        statusFilter.addEventListener('change', applyApplicationFilters);
    }
    
    if (searchInput) {
        searchInput.addEventListener('input', applyApplicationFilters);
    }
}

// Apply filters to applications
function applyApplicationFilters() {
    const user = getCurrentUser();
    if (!user) return;
    
    const statusFilter = document.getElementById('application-status-filter');
    const searchInput = document.getElementById('applications-search');
    
    const status = statusFilter ? statusFilter.value : 'all';
    const searchTerm = searchInput ? searchInput.value.toLowerCase() : '';
    
    // Get all applications for this user
    let applications = getApplications().filter(app => app.userId === user.id);
    
    // Apply status filter
    if (status !== 'all') {
        applications = applications.filter(app => app.status === status);
    }
    
    // Apply search filter
    if (searchTerm) {
        applications = applications.filter(app => 
            app.jobTitle.toLowerCase().includes(searchTerm) || 
            app.company.toLowerCase().includes(searchTerm)
        );
    }
    
    // Update the applications display
    const applicationsContainer = document.getElementById('applications-container');
    const noApplicationsMessage = document.getElementById('no-applications-message');
    
    if (!applicationsContainer) return;
    
    // Clear container
    applicationsContainer.innerHTML = '';
    
    if (applications.length === 0) {
        if (noApplicationsMessage) {
            noApplicationsMessage.style.display = 'block';
        }
        return;
    } else {
        if (noApplicationsMessage) {
            noApplicationsMessage.style.display = 'none';
        }
    }
    
    // Add each application card
    applications.forEach(application => {
        const applicationCard = createApplicationCard(application);
        applicationsContainer.appendChild(applicationCard);
    });
}

// View application details in modal
function viewApplicationDetails(applicationId) {
    const modal = document.getElementById('application-details-modal');
    const detailsContainer = document.getElementById('application-details-container');
    const withdrawBtn = document.getElementById('withdraw-application-btn');
    
    if (!modal || !detailsContainer) return;
    
    // Get application details
    const applications = getApplications();
    const application = applications.find(a => a.id === applicationId);
    
    if (!application) return;
    
    // Get related job details
    const jobs = getJobs();
    const job = jobs.find(j => j.id === application.jobId);
    
    // Populate application details
    detailsContainer.innerHTML = `
        <div class="application-details-header">
            <h2>${application.jobTitle}</h2>
            <p>${application.company}</p>
        </div>
        <div class="application-details-status">
            <strong>Status:</strong> <span class="status-${application.status}">${capitalizeFirstLetter(application.status)}</span>
        </div>
        <p><strong>Applied on:</strong> ${formatDate(application.appliedAt)}</p>
        
        <h3>Job Details:</h3>
        ${job ? 
            `<p><strong>Experience Required:</strong> ${job.experience} years</p>
             <p><strong>Salary:</strong> ${job.salary}</p>
             <div class="job-details-description">
                ${job.description.replace(/\n/g, '<br>')}
             </div>` 
            : 
            '<p>Original job listing is no longer available.</p>'
        }
    `;
    
    // Update withdraw button
    if (withdrawBtn) {
        withdrawBtn.onclick = function() {
            if (confirm('Are you sure you want to withdraw this application?')) {
                withdrawApplication(applicationId);
                modal.style.display = 'none';
            }
        };
    }
    
    // Show modal
    modal.style.display = 'block';
}

// Withdraw an application
function withdrawApplication(applicationId) {
    // Get all applications
    let applications = getApplications();
    const applicationIndex = applications.findIndex(a => a.id === applicationId);
    
    if (applicationIndex === -1) return;
    
    // Remove application
    applications.splice(applicationIndex, 1);
    
    // Update storage
    localStorage.setItem('applications', JSON.stringify(applications));
    
    // Refresh application listings
    loadUserApplications();
}

// Capitalize first letter of a string
function capitalizeFirstLetter(string) {
    return string.charAt(0).toUpperCase() + string.slice(1);
}