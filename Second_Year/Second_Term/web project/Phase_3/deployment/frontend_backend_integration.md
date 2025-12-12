# Frontend-Backend Integration Guide for JobSearch Application

This guide explains how to properly integrate the frontend HTML/CSS/JS with the Django backend API.

## Overview

The integration follows these principles:
- Frontend makes AJAX calls to the Django REST API endpoints
- Authentication is handled using Django's session-based authentication
- API endpoints follow RESTful conventions

## Directory Structure

```
/root/FCAI-CU/Second_Year/Second_Term/web project/
├── phase 2/
│   └── 20230263_project4_DoaaGhaleb_phase2/
│       └── ass/                         # Frontend files
│           ├── assets/
│           │   ├── css/
│           │   └── js/
│           │       └── userjs/
│           │           ├── api.js       # API client for backend
│           │           ├── auth.js      # Authentication handling
│           │           └── ...
│           ├── index.html
│           └── ...
└── Phase_3/
    └── jobsearch/                       # Django backend
        ├── accounts/
        ├── jobs/
        ├── applications/
        └── jobsearch/
            └── urls.py                 # API routes
```

## Step 1: Configure CORS (Cross-Origin Resource Sharing)

Django needs to be configured to accept requests from your frontend domain.

1. Add CORS configuration in `settings.py`:

```python
# In Phase_3/jobsearch/jobsearch/settings.py

CORS_ALLOWED_ORIGINS = [
    "http://localhost:8080",  # Development frontend server
    "http://yourproductiondomain.com",  # Production frontend
]

CORS_ALLOW_CREDENTIALS = True  # Important for cookies/sessions
```

## Step 2: Update API Client in Frontend

Ensure the API client is configured correctly to work with your backend:

```javascript
// Update Phase 2/20230263_project4_DoaaGhaleb_phase2/ass/assets/js/userjs/api.js

const API_BASE = 'http://localhost:8000/api/';  // Development
// const API_BASE = 'https://your-production-api.com/api/';  // Production

async function apiRequest(endpoint, options = {}) {
    try {
        if (!options.headers) {
            options.headers = { 'Content-Type': 'application/json' };
        }
        
        // Include credentials (cookies) for session-based auth
        options.credentials = 'include';

        const response = await fetch(`${API_BASE}${endpoint}`, options);

        if (!response.ok) {
            const errorData = await response.json().catch(() => ({}));
            throw new Error(errorData.error || `API error: ${response.status}`);
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
```

## Step 3: Update Authentication Flow

Make sure login, signup, and logout are properly integrated:

```javascript
// Update auth.js to handle login properly

async function handleLogin(e) {
    e.preventDefault();
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;
    const errorElement = document.getElementById('login-error');
    
    try {
        const user = await loginUserAPI(username, password);
        
        if (user) {
            // Store minimal user info in localStorage for UI purposes
            localStorage.setItem('user', JSON.stringify({
                id: user.id,
                username: user.username,
                is_company: user.is_company
            }));
            
            // Redirect based on user type
            if (user.is_company) {
                window.location.href = '/ass/features/admin/dashboard.html';
            } else {
                window.location.href = '/ass/features/user/search_jobs.html';
            }
        }
    } catch (error) {
        showError(errorElement, error.message || 'Invalid credentials');
    }
}

// Similar updates for signup and logout functions
```

## Step 4: Implement Authentication Check on Protected Pages

Add this to the top of your JavaScript files for protected pages:

```javascript
// Add this to the top of each page that requires authentication

document.addEventListener('DOMContentLoaded', async function() {
    try {
        const user = await getCurrentUserAPI();
        if (!user) {
            // No authenticated user, redirect to login
            window.location.href = '/ass/login.html?redirect=' + encodeURIComponent(window.location.pathname);
            return;
        }
        
        // For company-only pages
        if (needsToBeCompany && !user.is_company) {
            window.location.href = '/ass/features/user/search_jobs.html';
            return;
        }
        
        // For job seeker-only pages
        if (needsToBeJobSeeker && user.is_company) {
            window.location.href = '/ass/features/admin/dashboard.html';
            return;
        }
        
        // Setup page with user info
        setupPage(user);
    } catch (error) {
        console.error('Authentication check failed:', error);
        window.location.href = '/ass/login.html';
    }
});
```

## Step 5: Implement API Calls for Jobs

```javascript
// jobs.js - Functions for job-related operations

async function fetchJobs(filters = {}) {
    const queryParams = new URLSearchParams();
    
    if (filters.title) queryParams.append('title', filters.title);
    if (filters.location) queryParams.append('location', filters.location);
    if (filters.company) queryParams.append('company', filters.company);
    
    const endpoint = `jobs/?${queryParams.toString()}`;
    return await apiRequest(endpoint);
}

async function fetchJobDetails(jobId) {
    return await apiRequest(`jobs/${jobId}/`);
}

async function createJob(jobData) {
    return await apiRequest('jobs/', {
        method: 'POST',
        body: JSON.stringify(jobData)
    });
}

async function updateJob(jobId, jobData) {
    return await apiRequest(`jobs/${jobId}/`, {
        method: 'PUT',
        body: JSON.stringify(jobData)
    });
}

async function deleteJob(jobId) {
    return await apiRequest(`jobs/${jobId}/`, {
        method: 'DELETE'
    });
}
```

## Step 6: Implement API Calls for Applications

```javascript
// applications.js - Functions for job application operations

async function applyForJob(jobId, applicationData) {
    return await apiRequest('applications/', {
        method: 'POST',
        body: JSON.stringify({
            job: jobId,
            ...applicationData
        })
    });
}

async function fetchUserApplications() {
    return await apiRequest('applications/user_applications/');
}

async function fetchJobApplications(jobId) {
    return await apiRequest(`applications/?job=${jobId}`);
}

async function updateApplicationStatus(applicationId, status) {
    return await apiRequest(`applications/${applicationId}/`, {
        method: 'PATCH',
        body: JSON.stringify({ status })
    });
}
```

## Step 7: Update the UI Components

Create utility functions to render job listings, application forms, etc.:

```javascript
// ui.js - UI utility functions

function renderJobList(jobs, containerId) {
    const container = document.getElementById(containerId);
    container.innerHTML = '';
    
    if (!jobs || jobs.length === 0) {
        container.innerHTML = '<p class="no-results">No jobs found matching your criteria.</p>';
        return;
    }
    
    jobs.forEach(job => {
        const jobCard = createJobCard(job);
        container.appendChild(jobCard);
    });
}

function createJobCard(job) {
    const card = document.createElement('div');
    card.className = 'job-card';
    card.innerHTML = `
        <h3>${job.title}</h3>
        <p class="company">${job.company_name}</p>
        <p class="location"><i class="fas fa-map-marker-alt"></i> ${job.location}</p>
        <p class="salary"><i class="fas fa-money-bill-wave"></i> ${job.salary_range}</p>
        <div class="job-type">${job.job_type}</div>
        <a href="/ass/job-details.html?id=${job.id}" class="btn-view">View Details</a>
    `;
    return card;
}
```

## Step 8: Implement Search and Filters

```javascript
// search.js - Search functionality

document.addEventListener('DOMContentLoaded', function() {
    const searchForm = document.getElementById('job-search-form');
    
    if (searchForm) {
        searchForm.addEventListener('submit', async function(e) {
            e.preventDefault();
            
            const title = document.getElementById('search-title').value;
            const location = document.getElementById('search-location').value;
            
            try {
                const jobs = await fetchJobs({
                    title: title,
                    location: location
                });
                
                renderJobList(jobs, 'job-results');
            } catch (error) {
                console.error('Search failed:', error);
                document.getElementById('job-results').innerHTML = 
                    '<p class="error">Failed to load jobs. Please try again.</p>';
            }
        });
    }
});
```

## Step 9: Error Handling and Loading States

```javascript
// utils.js - Utility functions for error handling and loading states

function showLoading(containerId) {
    const container = document.getElementById(containerId);
    container.innerHTML = '<div class="loading-spinner"></div>';
}

function hideLoading(containerId) {
    const spinner = document.getElementById(containerId).querySelector('.loading-spinner');
    if (spinner) {
        spinner.remove();
    }
}

function showError(element, message) {
    element.textContent = message;
    element.style.display = 'block';
}

function clearError(element) {
    element.textContent = '';
    element.style.display = 'none';
}
```

## Testing the Integration

1. Start the Django development server:
   ```
   cd /root/FCAI-CU/Second_Year/Second_Term/web\ project/Phase_3/jobsearch
   python manage.py runserver
   ```

2. Open your frontend pages in the browser and test:
   - User registration
   - Login/logout
   - Viewing job listings
   - Applying for jobs
   - Company posting jobs

## Production Deployment Considerations

1. Update `API_BASE` in api.js to point to your production API endpoint
2. Configure CORS settings in Django to allow your production frontend domain
3. Set up proper HTTPS for both frontend and backend
4. Use environment variables for API endpoints to easily switch between environments

By following this guide, your frontend will be properly integrated with your Django backend API.
