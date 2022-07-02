export function genTooltip(el, title) {
    document.querySelectorAll(el).forEach(el => {
        bootstrap.Tooltip.getOrCreateInstance(el, {
            title: title
        })
    })
}

export function initTooltips() {
    const tooltipTriggerList = document.querySelectorAll('[data-bs-toggle="tooltip"]');
    const tooltipList = [...tooltipTriggerList].map(tooltipTriggerEl => new bootstrap.Tooltip(tooltipTriggerEl));
}

export function ajax(url) {
    return fetch(url)
        .then(response => {
            if (response.ok) {
                return response.json()
            }
            return Promise.reject(
                new Error(response.status + ": " + response.statusText)
            );
        })
        .catch(err => {
            console.error('Fetch Error:', err);
        });
}