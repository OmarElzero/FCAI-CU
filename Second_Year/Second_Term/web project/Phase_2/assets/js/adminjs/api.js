const API_BASE = 'http://localhost:8000/api/';

async function apiRequest(endpoint, options = {}) {
    try {
        if (!options.headers) {
            options.headers = { 'Content-Type': 'application/json' };
        }
        if (!options.hasOwnProperty('credentials')) {
            options.credentials = 'include';
        }
        
        const response = await fetch(`${API_BASE}${endpoint}`, options);
        
        if (!response.ok) {
            const errorData = await response.json().catch(() => ({}));
            throw new Error(errorData.error || errorData.detail || `API error: ${response.status}`);
        }
        
        if (response.status === 204) {
            return null;
        }
        
        return await response.json();
    } catch (error) {
        console.error(`API request failed: ${error.message}`);
        throw error;
    }
}

async function getCurrentUser() {
    try {
        const response = await apiRequest('users/current/');
        return response;
    } catch (error) {
        console.error('Failed to get current user:', error);
        return null;
    }
}

// Get all jobs
async function getJobs(filters = {}) {
    try {
        const queryParams = new URLSearchParams();
        Object.entries(filters).forEach(([key, value]) => {
            if (value) queryParams.append(key, value);
        });
        
        const endpoint = `jobs/${queryParams.toString() ? '?' + queryParams.toString() : ''}`;
        const jobs = await apiRequest(endpoint);
        return jobs || [];
    } catch (error) {
        console.error('Failed to fetch jobs:', error);
        return [];
    }
}

// Get company jobs
async function getCompanyJobs() {
    try {
        return await apiRequest('jobs/company_jobs/');
    } catch (error) {
        console.error('Failed to fetch company jobs:', error);
        return [];
    }
}

// Create a new job
async function createJob(jobData) {
    try {
        return await apiRequest('jobs/', {
            method: 'POST',
            body: JSON.stringify(jobData)
        });
    } catch (error) {
        console.error('Failed to create job:', error);
        throw error;
    }
}

// Update a job
async function updateJob(jobId, jobData) {
    try {
        return await apiRequest(`jobs/${jobId}/`, {
            method: 'PATCH',
            body: JSON.stringify(jobData)
        });
    } catch (error) {
        console.error('Failed to update job:', error);
        throw error;
    }
}

export { 
    apiRequest, 
    getCurrentUser, 
    getJobs, 
    getCompanyJobs, 
    createJob, 
    updateJob 
};
