function getRelativePathToRoot() {
    const path = window.location.pathname;
    let depth = 0;

    if (path.includes('/features/')) {
        depth = 2;
    } else if (path.includes('/components/')) {
        depth = 1;
    }

    return depth === 0 ? '' : '../'.repeat(depth);
}

function showError(element, message) {
    if (element) {
        element.textContent = message;
        element.style.display = 'block';
    }
}

function clearError(element) {
    if (element) {
        element.textContent = '';
        element.style.display = 'none';
    }
}

function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', {
        year: 'numeric', 
        month: 'long', 
        day: 'numeric'
    });
}

function truncateText(text, maxLength) {
    return text.length > maxLength ? text.substring(0, maxLength) + '...' : text;
}

function initModal(modalId) {
    const modal = document.getElementById(modalId);
    if (!modal) return;

    const closeButton = modal.querySelector('.close-modal');
    if (closeButton) {
        closeButton.addEventListener('click', () => {
            modal.style.display = 'none';
        });
    }

    window.addEventListener('click', (event) => {
        if (event.target === modal) {
            modal.style.display = 'none';
        }
    });
}

function getUrlParams() {
    const params = {};
    const queryString = window.location.search;
    const urlParams = new URLSearchParams(queryString);

    for (const [key, value] of urlParams.entries()) {
        params[key] = value;
    }

    return params;
}

function capitalizeFirstLetter(string) {
    return string.charAt(0).toUpperCase() + string.slice(1);
}

export {
    getRelativePathToRoot,
    showError,
    clearError,
    formatDate,
    truncateText,
    initModal,
    getUrlParams,
    capitalizeFirstLetter
};
