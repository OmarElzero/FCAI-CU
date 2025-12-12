// Dashboard script for admin dashboard
import { getCompanyJobs, deleteJob, updateJob } from '../../assets/js/userjs/api.js';
import { formatDate, showError, clearError } from '../../assets/js/userjs/utils.js';

// DOM elements
const jobListingsContainer = document.getElementById('job-listings');
const statusFilter = document.getElementById('status-filter');
const sortBy = document.getElementById('sort-by');
const searchInput = document.getElementById('search-jobs');
const loadingIndicator = document.getElementById('loading-indicator');
const noJobsMessage = document.getElementById('no-jobs-message');

// Company jobs data
let companyJobs = [];

// Initialize the dashboard
document.addEventListener('DOMContentLoaded', async function() {
    // Load company jobs
    await loadCompanyJobs();
    
    // Setup event listeners
    setupEventListeners();
});

/**
 * Load company jobs from the API
 */
async function loadCompanyJobs() {
    try {
        // Show loading indicator
        if (loadingIndicator) {
            loadingIndicator.style.display = 'block';
        }
        
        if (noJobsMessage) {
            noJobsMessage.style.display = 'none';
        }
        
        // Get company jobs from API
        companyJobs = await getCompanyJobs();
        
        // Hide loading indicator
        if (loadingIndicator) {
            loadingIndicator.style.display = 'none';
        }
        
        // Apply filters and render jobs
        filterAndRenderJobs();
    } catch (error) {
        console.error('Error loading company jobs:', error);
        
        // Hide loading indicator
        if (loadingIndicator) {
            loadingIndicator.style.display = 'none';
        }
        
        // Show error message
        if (jobListingsContainer) {
            jobListingsContainer.innerHTML = '<div class="error-message">Failed to load jobs. Please try again.</div>';
        }
    }
}

/**
 * Setup event listeners for filters and search
 */
function setupEventListeners() {
    // Status filter
    if (statusFilter) {
        statusFilter.addEventListener('change', filterAndRenderJobs);
    }
    
    // Sort by
    if (sortBy) {
        sortBy.addEventListener('change', filterAndRenderJobs);
    }
    
    // Search input
    if (searchInput) {
        searchInput.addEventListener('input', filterAndRenderJobs);
    }
}

/**
 * Filter and render jobs based on current filters
 */
function filterAndRenderJobs() {
    if (!jobListingsContainer) return;
    
    // Get filter values
    const status = statusFilter ? statusFilter.value : 'all';
    const sort = sortBy ? sortBy.value : 'date';
    const search = searchInput ? searchInput.value.toLowerCase() : '';
    
    // Filter jobs
    let filteredJobs = [...companyJobs];
    
    // Filter by status
    if (status !== 'all') {
        filteredJobs = filteredJobs.filter(job => job.status.toLowerCase() === status.toLowerCase());
    }
    
    // Filter by search
    if (search) {
        filteredJobs = filteredJobs.filter(job => 
            job.title.toLowerCase().includes(search) || 
            job.description.toLowerCase().includes(search) ||
            job.location.toLowerCase().includes(search)
        );
    }
    
    // Sort jobs
    switch (sort) {
        case 'title':
            filteredJobs.sort((a, b) => a.title.localeCompare(b.title));
            break;
        case 'applications':
            filteredJobs.sort((a, b) => (b.application_count || 0) - (a.application_count || 0));
            break;
        case 'date':
        default:
            filteredJobs.sort((a, b) => new Date(b.created_at) - new Date(a.created_at));
            break;
    }
    
    // Render jobs
    renderJobs(filteredJobs);
}

/**
 * Render jobs to the container
 * @param {Array} jobs - Jobs to render
 */
function renderJobs(jobs) {
    if (!jobListingsContainer) return;
    
    // Clear container
    jobListingsContainer.innerHTML = '';
    
    // Check if no jobs
    if (!jobs || jobs.length === 0) {
        if (noJobsMessage) {
            noJobsMessage.style.display = 'block';
        } else {
            jobListingsContainer.innerHTML = '<div class="no-jobs-message">No jobs found matching your criteria.</div>';
        }
        return;
    }
    
    // Render each job
    jobs.forEach(job => {
        const jobElement = createJobElement(job);
        jobListingsContainer.appendChild(jobElement);
    });
}

/**
 * Create a job element
 * @param {Object} job - Job data
 * @returns {HTMLElement} - Job element
 */
function createJobElement(job) {
    const jobElement = document.createElement('div');
    jobElement.className = 'admin-job-card';
    jobElement.dataset.jobId = job.id;
    
    // Format date
    const createdDate = formatDate(job.created_at);
    
    // Determine status class
    let statusClass = 'status-open';
    if (job.status.toLowerCase() === 'closed') {
        statusClass = 'status-closed';
    } else if (job.status.toLowerCase() === 'draft') {
        statusClass = 'status-draft';
    }
    
    jobElement.innerHTML = `
        <div class="job-header">
            <h3 class="job-title">${job.title}</h3>
            <span class="job-status ${statusClass}">${job.status}</span>
        </div>
        <div class="job-details">
            <div class="job-meta">
                <span><i class="fas fa-map-marker-alt"></i> ${job.location}</span>
                <span><i class="fas fa-calendar"></i> Posted: ${createdDate}</span>
                <span><i class="fas fa-users"></i> ${job.application_count || 0} Applications</span>
            </div>
            <div class="job-actions">
                <a href="edit_job.html?id=${job.id}" class="btn-secondary btn-sm">
                    <i class="fas fa-edit"></i> Edit
                </a>
                <a href="view_applicants.html?jobId=${job.id}" class="btn-secondary btn-sm">
                    <i class="fas fa-users"></i> View Applicants
                </a>
                <button class="btn-danger btn-sm delete-job" data-job-id="${job.id}">
                    <i class="fas fa-trash"></i> Delete
                </button>
                <button class="btn-${job.status.toLowerCase() === 'open' ? 'warning' : 'success'} btn-sm toggle-status" data-job-id="${job.id}" data-current-status="${job.status}">
                    <i class="fas fa-${job.status.toLowerCase() === 'open' ? 'pause' : 'play'}"></i> ${job.status.toLowerCase() === 'open' ? 'Close' : 'Open'} Listing
                </button>
            </div>
        </div>
    `;
    
    // Add event listeners for actions
    const deleteButton = jobElement.querySelector('.delete-job');
    if (deleteButton) {
        deleteButton.addEventListener('click', () => handleDeleteJob(job.id));
    }
    
    const toggleStatusButton = jobElement.querySelector('.toggle-status');
    if (toggleStatusButton) {
        toggleStatusButton.addEventListener('click', () => handleToggleStatus(job));
    }
    
    return jobElement;
}

/**
 * Handle delete job
 * @param {number} jobId - Job ID
 */
async function handleDeleteJob(jobId) {
    if (!confirm('Are you sure you want to delete this job? This action cannot be undone.')) {
        return;
    }
    
    try {
        await deleteJob(jobId);
        
        // Remove job from list
        companyJobs = companyJobs.filter(job => job.id !== jobId);
        
        // Re-render jobs
        filterAndRenderJobs();
        
        // Show success message
        alert('Job deleted successfully');
    } catch (error) {
        console.error('Failed to delete job:', error);
        alert('Failed to delete job. Please try again.');
    }
}

/**
 * Handle toggle job status
 * @param {Object} job - Job data
 */
async function handleToggleStatus(job) {
    const newStatus = job.status.toLowerCase() === 'open' ? 'Closed' : 'Open';
    
    try {
        await updateJob(job.id, { status: newStatus });
        
        // Update job in list
        const updatedJob = { ...job, status: newStatus };
        const index = companyJobs.findIndex(j => j.id === job.id);
        if (index !== -1) {
            companyJobs[index] = updatedJob;
        }
        
        // Re-render jobs
        filterAndRenderJobs();
        
        // Show success message
        alert(`Job status changed to ${newStatus}`);
    } catch (error) {
        console.error('Failed to update job status:', error);
        alert('Failed to update job status. Please try again.');
    }
}

// Export functions for use in other modules
export {
    loadCompanyJobs,
    filterAndRenderJobs
};
