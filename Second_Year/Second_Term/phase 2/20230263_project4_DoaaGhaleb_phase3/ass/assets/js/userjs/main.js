import { checkAuthStatus } from './auth.js';
import { setupAuthForms } from './auth.js';
import { loadNavbar } from './ui.js';
import { initModal, formatDate, truncateText } from './utils.js';

document.addEventListener('DOMContentLoaded', async function() {
    loadNavbar();
    await checkAuthStatus();
    setupAuthForms();
    window.formatDate = formatDate;
    window.truncateText = truncateText;
    window.initModal = initModal;
});
