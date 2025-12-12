import { getApplications as getApplicationsAPI, withdrawApplicationAPI } from './api.js';
import { getCurrentUser } from './api.js';
import { getJobs as getJobsAPI } from './api.js';
import { formatDate, capitalizeFirstLetter } from './utils.js';

async function initAppliedJobs() {
    const user = await getCurrentUser();
    if (!user) return;
    await loadUserApplications();
    setupApplicationFiltering();
}

async function loadUserApplications() {
    try {
        const user = await getCurrentUser();
        const applicationsContainer = document.getElementById('applications-container');
        const noApplicationsMessage = document.getElementById('no-applications-message');
        if (!applicationsContainer || !user) return;
        const applications = await getApplicationsAPI();
        const userApplications = applications.filter(app => app.user === user.id);
        if (userApplications.length === 0) {
            if (noApplicationsMessage) noApplicationsMessage.style.display = 'block';
            return;
        }
        if (noApplicationsMessage) noApplicationsMessage.style.display = 'none';
        applicationsContainer.innerHTML = '';
        const jobs = await getJobsAPI();
        for (const application of userApplications) {
            const job = jobs.find(j => j.id === application.job);
            if (job) {
                application.job_title = job.title;
                application.company = job.company;
            }
            const applicationCard = createApplicationCard(application);
            applicationsContainer.appendChild(applicationCard);
        }
    } catch (error) {
        console.error('Error loading applications:', error);
    }
}

function createApplicationCard(application) {
    const card = document.createElement('div');
    card.className = 'application-card';
    card.dataset.applicationId = application.id;

    const infoDiv = document.createElement('div');
    infoDiv.className = 'application-info';

    const title = document.createElement('h3');
    title.className = 'application-title';
    title.textContent = application.job_title || 'Job';

    const company = document.createElement('p');
    company.className = 'application-company';
    company.textContent = application.company || '';

    const date = document.createElement('p');
    date.className = 'application-date';
    date.textContent = `Applied on: ${formatDate(application.applied_at || application.appliedAt)}`;

    infoDiv.appendChild(title);
    infoDiv.appendChild(company);
    infoDiv.appendChild(date);

    const statusSpan = document.createElement('span');
    statusSpan.className = `application-status status-${application.status}`;
    statusSpan.textContent = capitalizeFirstLetter(application.status);

    card.appendChild(infoDiv);
    card.appendChild(statusSpan);

    card.addEventListener('click', function() {
        viewApplicationDetails(application.id);
    });

    return card;
}

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

async function applyApplicationFilters() {
    try {
        const user = await getCurrentUser();
        if (!user) return;

        const statusFilter = document.getElementById('application-status-filter');
        const searchInput = document.getElementById('applications-search');

        const status = statusFilter ? statusFilter.value : 'all';
        const searchTerm = searchInput ? searchInput.value.toLowerCase() : '';

        const applications = await getApplicationsAPI();
        let userApplications = applications.filter(app => app.user === user.id);

        if (status !== 'all') {
            userApplications = userApplications.filter(app => app.status === status);
        }

        const jobs = await getJobsAPI();
        userApplications = userApplications.map(app => {
            const job = jobs.find(j => j.id === app.job);
            if (job) {
                return {
                    ...app,
                    job_title: job.title,
                    company: job.company
                };
            }
            return app;
        });

        if (searchTerm) {
            userApplications = userApplications.filter(app => {
                return (app.job_title && app.job_title.toLowerCase().includes(searchTerm)) ||
                       (app.company && app.company.toLowerCase().includes(searchTerm));
            });
        }

        const applicationsContainer = document.getElementById('applications-container');
        const noApplicationsMessage = document.getElementById('no-applications-message');
        if (!applicationsContainer) return;

        applicationsContainer.innerHTML = '';
        if (userApplications.length === 0) {
            if (noApplicationsMessage) noApplicationsMessage.style.display = 'block';
            return;
        } else {
            if (noApplicationsMessage) noApplicationsMessage.style.display = 'none';
        }

        userApplications.forEach(application => {
            const applicationCard = createApplicationCard(application);
            applicationsContainer.appendChild(applicationCard);
        });
    } catch (error) {
        console.error('Error applying application filters:', error);
    }
}

async function viewApplicationDetails(applicationId) {
    try {
        const modal = document.getElementById('application-details-modal');
        const detailsContainer = document.getElementById('application-details-container');
        const withdrawBtn = document.getElementById('withdraw-application-btn');
        if (!modal || !detailsContainer) return;

        const applications = await getApplicationsAPI();
        const application = applications.find(a => a.id === applicationId);
        if (!application) {
            detailsContainer.innerHTML = '<p>Application not found.</p>';
            return;
        }

        const jobs = await getJobsAPI();
        const job = jobs.find(j => j.id === application.job);

        detailsContainer.innerHTML = `
            <div class="application-details-header">
                <h2>${job ? job.title : 'Unknown Job'}</h2>
                <p>${job ? job.company : ''}</p>
            </div>
            <div class="application-details-status">
                <strong>Status:</strong> <span class="status-${application.status}">${capitalizeFirstLetter(application.status)}</span>
            </div>
            <p><strong>Applied on:</strong> ${formatDate(application.applied_at || application.appliedAt)}</p>
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

        if (withdrawBtn) {
            withdrawBtn.onclick = async function() {
                if (confirm('Are you sure you want to withdraw this application?')) {
                    await withdrawApplication(applicationId);
                    modal.style.display = 'none';
                }
            };
        }

        modal.style.display = 'block';
    } catch (error) {
        console.error('Error viewing application details:', error);
    }
}

async function withdrawApplication(applicationId) {
    try {
        const success = await withdrawApplicationAPI(applicationId);
        if (success) {
            await loadUserApplications();
        } else {
            alert('Failed to withdraw application. Please try again.');
        }
    } catch (error) {
        console.error('Error withdrawing application:', error);
        alert('An error occurred while withdrawing your application.');
    }
}

export {
    initAppliedJobs,
    loadUserApplications,
    applyApplicationFilters,
    viewApplicationDetails,
    withdrawApplication
};
