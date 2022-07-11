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

export function displayToast(msg, delay = 2000) {
    let div = `<div class="toast toast-info fade" role="alert" aria-live="polite" aria-atomic="true" data-autohide="true" data-delay="${delay}">
                   <div class="toast-body">
                   ${msg}
                   </div>
               </div>`
    $(document.body).append(div);
    $('.toast').on('hidden.bs.toast', function () {
        $(this).remove();
    })
    $(".toast").toast('show');
}

export function initMessages() {
    let message = sessionStorage.getItem('message');
    if (!message) {
        return;
    }
    $(document).ready(() => {
        displayToast(message);
        sessionStorage.removeItem('message');
    });
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