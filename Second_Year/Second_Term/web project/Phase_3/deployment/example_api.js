// API client for JobSearch application
// This file handles all API interactions with the backend

// Base URL for API - change this when deploying to production
const API_BASE = 'http://localhost:8000/api/';

/**
 * Generic API request function with error handling
 * @param {string} endpoint - API endpoint to call
 * @param {object} options - Fetch API options
 * @returns {Promise<object>} - Response data
 */
async function apiRequest(endpoint, options = {}) {
    try {
        // Set default headers if not provided
        if (!options.headers) {
            options.headers = { 'Content-Type': 'application/json' };
        }
        
        // Include credentials for session-based auth
        options.credentials = 'include';

        const response = await fetch(`${API_BASE}${endpoint}`, options);

        // Handle non-successful responses
        if (!response.ok) {
            const errorData = await response.json().catch(() => ({}));
            throw new Error(errorData.error || errorData.detail || `API error: ${response.status}`);
        }

        // No content
        if (response.status === 204) {
            return null;
        }

        return await response.json();
    } catch (error) {
        console.error(`API request failed: ${error.message}`);
        throw error;
    }
}

// ====== USER AUTHENTICATION ======

/**
 * Get current logged in user
 * @returns {Promise<object|null>} User object or null if not logged in
 */
async function getCurrentUser() {
    try {
        return await apiRequest('users/current/');
    } catch (error) {
        console.error('Failed to get current user:', error);
        return null;
    }
}

/**
 * Login user
 * @param {string} username - Username
 * @param {string} password - Password
 * @returns {Promise<object>} User object
 */
async function loginUser(username, password) {
    return await apiRequest('users/login/', {
        method: 'POST',
        body: JSON.stringify({ username, password })
    });
}

/**
 * Register a new user
 * @param {object} userData - User registration data
 * @returns {Promise<object>} New user object
 */
async function registerUser(userData) {
    return await apiRequest('users/register/', {
        method: 'POST',
        body: JSON.stringify(userData)
    });
}

/**
 * Logout current user
 * @returns {Promise<object>} Logout confirmation
 */
async function logoutUser() {
    return await apiRequest('users/logout/', {
        method: 'POST'
    });
}

/**
 * Update user profile
 * @param {number} userId - User ID
 * @param {object} userData - User data to update
 * @returns {Promise<object>} Updated user object
 */
async function updateUserProfile(userId, userData) {
    return await apiRequest(`users/${userId}/`, {
        method: 'PATCH',
        body: JSON.stringify(userData)
    });
}

// ====== JOBS ======

/**
 * Get all jobs with optional filtering
 * @param {object} filters - Filter criteria
 * @returns {Promise<Array>} Jobs list
 */
async function getJobs(filters = {}) {
    const queryParams = new URLSearchParams();
    
    // Add filters to query params
    Object.entries(filters).forEach(([key, value]) => {
        if (value) queryParams.append(key, value);
    });
    
    const endpoint = `jobs/${queryParams.toString() ? '?' + queryParams.toString() : ''}`;
    return await apiRequest(endpoint);
}

/**
 * Get job details by ID
 * @param {number} jobId - Job ID
 * @returns {Promise<object>} Job details
 */
async function getJobById(jobId) {
    return await apiRequest(`jobs/${jobId}/`);
}

/**
 * Create a new job
 * @param {object} jobData - Job data
 * @returns {Promise<object>} Created job
 */
async function createJob(jobData) {
    return await apiRequest('jobs/', {
        method: 'POST',
        body: JSON.stringify(jobData)
    });
}

/**
 * Update a job
 * @param {number} jobId - Job ID
 * @param {object} jobData - Job data to update
 * @returns {Promise<object>} Updated job
 */
async function updateJob(jobId, jobData) {
    return await apiRequest(`jobs/${jobId}/`, {
        method: 'PATCH',
        body: JSON.stringify(jobData)
    });
}

/**
 * Delete a job
 * @param {number} jobId - Job ID
 * @returns {Promise<void>}
 */
async function deleteJob(jobId) {
    return await apiRequest(`jobs/${jobId}/`, {
        method: 'DELETE'
    });
}

/**
 * Get company jobs
 * @returns {Promise<Array>} Company jobs
 */
async function getCompanyJobs() {
    return await apiRequest('jobs/company_jobs/');
}

// ====== APPLICATIONS ======

/**
 * Apply for a job
 * @param {object} applicationData - Application data
 * @returns {Promise<object>} Created application
 */
async function applyForJob(applicationData) {
    return await apiRequest('applications/', {
        method: 'POST',
        body: JSON.stringify(applicationData)
    });
}

/**
 * Get user applications
 * @returns {Promise<Array>} User applications
 */
async function getUserApplications() {
    return await apiRequest('applications/user_applications/');
}

/**
 * Get job applications (for company/admin)
 * @param {number} jobId - Job ID
 * @returns {Promise<Array>} Job applications
 */
async function getJobApplications(jobId) {
    return await apiRequest(`applications/?job=${jobId}`);
}

/**
 * Update application status
 * @param {number} applicationId - Application ID
 * @param {string} status - New status
 * @returns {Promise<object>} Updated application
 */
async function updateApplicationStatus(applicationId, status) {
    return await apiRequest(`applications/${applicationId}/`, {
        method: 'PATCH',
        body: JSON.stringify({ status })
    });
}

// Export all functions
export {
    getCurrentUser,
    loginUser,
    registerUser,
    logoutUser,
    updateUserProfile,
    getJobs,
    getJobById,
    createJob,
    updateJob,
    deleteJob,
    getCompanyJobs,
    applyForJob,
    getUserApplications,
    getJobApplications,
    updateApplicationStatus
};
