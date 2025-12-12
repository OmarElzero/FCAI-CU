import { getJobs as getJobsAPI, applyToJobAPI, getCurrentUser } from './api.js';
import { formatDate, truncateText, capitalizeFirstLetter, showError, clearError } from './utils.js';

async function initSearchJobs() {
    await loadAvailableJobs();
    await loadCompaniesFilter();
    setupSearchFilters();
}

async function loadAvailableJobs() {
    const jobsContainer = document.getElementById('search-results-container');
    const noResultsMessage = document.getElementById('no-results-message');
    const resultsCount = document.getElementById('results-count');
    
    if (!jobsContainer) return;
    
    try {
        const allJobs = await getJobsAPI();
        const openJobs = allJobs.filter(job => job.status === 'Open');
        
        if (openJobs.length === 0) {
            if (noResultsMessage) noResultsMessage.style.display = 'block';
            if (resultsCount) resultsCount.textContent = '0 jobs found';
            return;
        }
        
        if (resultsCount) resultsCount.textContent = `${openJobs.length} jobs found`;
        jobsContainer.innerHTML = '';
        
        const user = await getCurrentUser();
        const applications = [];
        if (user) {
            const allApplications = await fetch('http://localhost:8000/api/applications/', {
                credentials: 'include'
            }).then(res => res.ok ? res.json() : []);
            
            applications.push(...allApplications.filter(app => app.user === user.id));
        }
        
        const appliedJobIds = applications.map(app => app.job);
        
        openJobs.forEach(job => {
            job.applied = appliedJobIds.includes(job.id);
            const jobCard = createJobCard(job);
            jobsContainer.appendChild(jobCard);
        });
    } catch (error) {
        console.error('Error loading jobs:', error);
        if (jobsContainer) jobsContainer.innerHTML = '<p>Failed to load jobs. Please try again later.</p>';
    }
}

async function loadCompaniesFilter() {
    const companyFilter = document.getElementById('company-filter');
    if (!companyFilter) return;
    
    try {
        const allJobs = await getJobsAPI();
        const companies = [...new Set(allJobs.map(job => job.company))];
        
        while (companyFilter.options.length > 1) {
            companyFilter.remove(1);
        }
        
        companies.forEach(company => {
            const option = document.createElement('option');
            option.value = company;
            option.textContent = company;
            companyFilter.appendChild(option);
        });
    } catch (error) {
        console.error('Error loading companies:', error);
    }
}

function setupSearchFilters() {
    const jobKeyword = document.getElementById('job-keyword');
    const experienceFilter = document.getElementById('experience-filter');
    const companyFilter = document.getElementById('company-filter');
    const searchButton = document.getElementById('search-button');
    
    if (searchButton) {
        searchButton.addEventListener('click', applyJobFilters);
    }
    
    if (jobKeyword) {
        jobKeyword.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                applyJobFilters();
            }
        });
    }
}

async function applyJobFilters() {
    const jobKeyword = document.getElementById('job-keyword');
    const experienceFilter = document.getElementById('experience-filter');
    const companyFilter = document.getElementById('company-filter');
    
    const keyword = jobKeyword ? jobKeyword.value.toLowerCase() : '';
    const experience = experienceFilter ? experienceFilter.value : '';
    const company = companyFilter ? companyFilter.value : '';
    
    try {
        const allJobs = await getJobsAPI();
        let filteredJobs = allJobs.filter(job => job.status === 'Open');
        
        if (keyword) {
            filteredJobs = filteredJobs.filter(job => 
                job.title.toLowerCase().includes(keyword) || 
                job.description.toLowerCase().includes(keyword)
            );
        }
        
        if (experience) {
            const minExperience = parseInt(experience, 10);
            filteredJobs = filteredJobs.filter(job => job.experience >= minExperience);
        }
        
        if (company) {
            filteredJobs = filteredJobs.filter(job => job.company === company);
        }
        
        const jobsContainer = document.getElementById('search-results-container');
        const noResultsMessage = document.getElementById('no-results-message');
        const resultsCount = document.getElementById('results-count');
        
        if (!jobsContainer) return;
        
        jobsContainer.innerHTML = '';
        
        if (resultsCount) resultsCount.textContent = `${filteredJobs.length} jobs found`;
        
        if (filteredJobs.length === 0) {
            if (noResultsMessage) noResultsMessage.style.display = 'block';
            return;
        } else {
            if (noResultsMessage) noResultsMessage.style.display = 'none';
        }
        
        const user = await getCurrentUser();
        const applications = [];
        
        if (user) {
            const allApplications = await fetch('http://localhost:8000/api/applications/', {
                credentials: 'include'
            }).then(res => res.ok ? res.json() : []);
            
            applications.push(...allApplications.filter(app => app.user === user.id));
        }
        
        const appliedJobIds = applications.map(app => app.job);
        
        filteredJobs.forEach(job => {
            job.applied = appliedJobIds.includes(job.id);
            const jobCard = createJobCard(job);
            jobsContainer.appendChild(jobCard);
        });
    } catch (error) {
        console.error('Error applying filters:', error);
    }
}

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
    viewBtn.onclick = function(e) {
        e.preventDefault();
        window.location.href = `job_details.html?id=${job.id}`;
    };
    
    footerDiv.appendChild(viewBtn);
    
    card.appendChild(headerDiv);
    card.appendChild(bodyDiv);
    card.appendChild(footerDiv);
    
    return card;
}

async function viewJobDetails(jobId) {
    try {
        const modal = document.getElementById('job-details-modal');
        const detailsContainer = document.getElementById('job-details-container');
        const applyBtn = document.getElementById('apply-job-btn');
        
        if (!modal || !detailsContainer) return;
        
        const jobs = await getJobsAPI();
        const job = jobs.find(j => j.id === jobId);
        
        if (!job) {
            detailsContainer.innerHTML = '<p>Job not found.</p>';
            return;
        }
        
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
                <span><strong>Posted:</strong> ${formatDate(job.created_at || job.createdAt)}</span>
            </div>
            <h3>Job Description:</h3>
            <div class="job-details-description">
                ${job.description.replace(/\n/g, '<br>')}
            </div>
        `;
        
        if (applyBtn) {
            const user = await getCurrentUser();
            
            if (!user || user.role !== 'user') {
                applyBtn.style.display = 'none';
            } else {
                const applications = await fetch('http://localhost:8000/api/applications/', {
                    credentials: 'include'
                }).then(res => res.ok ? res.json() : []);
                
                const hasApplied = applications.some(app => app.job === jobId && app.user === user.id);
                
                applyBtn.style.display = 'inline-block';
                
                if (hasApplied) {
                    applyBtn.textContent = 'Already Applied';
                    applyBtn.disabled = true;
                } else {
                    applyBtn.textContent = 'Apply Now';
                    applyBtn.disabled = false;
                    applyBtn.onclick = async function() {
                        await applyToJob(jobId);
                        modal.style.display = 'none';
                    };
                }
            }
        }
        
        modal.style.display = 'block';
    } catch (error) {
        console.error('Error viewing job details:', error);
    }
}

async function applyToJob(jobId) {
    try {
        const user = await getCurrentUser();
        
        if (!user) {
            window.location.href = '/login.html?redirect=' + encodeURIComponent(window.location.pathname);
            return;
        }
        
        if (user.role !== 'user') {
            alert('Only job seekers can apply to jobs');
            return;
        }
        
        const applications = await fetch('http://localhost:8000/api/applications/', {
            credentials: 'include'
        }).then(res => res.ok ? res.json() : []);
        
        if (applications.some(app => app.job === jobId && app.user === user.id)) {
            alert('You have already applied to this job');
            return;
        }
        
        const result = await applyToJobAPI(jobId);
        
        if (result) {
            alert('Successfully applied to this job');
            
            if (window.location.pathname.includes('search_jobs.html')) {
                await loadAvailableJobs();
            }
            
            const applyBtn = document.getElementById('apply-job-btn');
            if (applyBtn) {
                applyBtn.textContent = 'Applied';
                applyBtn.disabled = true;
            }
        } else {
            alert('Failed to apply. Please try again.');
        }
    } catch (error) {
        console.error('Error applying to job:', error);
        alert('An error occurred while applying to the job.');
    }
}

export {
    initSearchJobs,
    loadAvailableJobs,
    applyJobFilters,
    viewJobDetails,
    applyToJob
};
