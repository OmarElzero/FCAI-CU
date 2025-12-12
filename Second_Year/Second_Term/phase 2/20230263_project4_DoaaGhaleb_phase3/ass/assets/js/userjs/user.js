import { initSearchJobs, viewJobDetails, applyToJob, applyJobFilters } from './jobs.js';
import { initAppliedJobs, viewApplicationDetails } from './applications.js';
import { initModal } from './utils.js';

document.addEventListener('DOMContentLoaded', function() {
    if (window.location.pathname.includes('search_jobs.html')) {
        initSearchJobs();
        initModal('job-details-modal');
        window.applyJobFilters = applyJobFilters;
    }

    if (window.location.pathname.includes('job_details.html')) {
    }

    if (window.location.pathname.includes('applied_jobs.html')) {
        initAppliedJobs();
        initModal('application-details-modal');
    }

    window.viewJobDetails = viewJobDetails;
    window.applyToJob = applyToJob;
    window.viewApplicationDetails = viewApplicationDetails;
});
