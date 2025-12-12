// This file will contain admin application/applicant management logic split from admin.js

import { getCurrentUser } from './api.js';

// Fetch and show applicants for a job (admin view)
export async function showApplicantsModal(jobId) {
    const applicantsModal = document.getElementById('applicants-modal');
    const applicantsContainer = document.getElementById('applicants-container');
    if (!applicantsModal || !applicantsContainer) return;
    // Get all applications for this job from API
    const applications = (await fetch('http://localhost:8000/api/applications/', { credentials: 'include' }).then(r => r.json())).filter(app => app.job == jobId);
    if (applications.length === 0) {
        applicantsContainer.innerHTML = '<p>No applicants for this job yet.</p>';
    } else {
        // Get users for profile info from API
        const users = await fetch('http://localhost:8000/api/users/', { credentials: 'include' }).then(r => r.json());
        applicantsContainer.innerHTML = '<h3>Applicants</h3>' + applications.map(app => {
            const user = users.find(u => u.id === app.user);
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
                <div><strong>Applied on:</strong> ${formatDate(app.applied_at || app.appliedAt)}</div>
            </div>`;
        }).join('');
    }
    // Add event listeners for status change
    setTimeout(() => {
        document.querySelectorAll('.app-status-select').forEach(select => {
            select.addEventListener('change', async function() {
                const appId = this.getAttribute('data-app-id');
                await updateApplicationStatus(appId, this.value);
            });
        });
    }, 100);
    applicantsModal.style.display = 'block';
}

// Update application status via API
export async function updateApplicationStatus(appId, newStatus) {
    await fetch(`http://localhost:8000/api/applications/${appId}/`, {
        method: 'PATCH',
        credentials: 'include',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ status: newStatus })
    });
}
