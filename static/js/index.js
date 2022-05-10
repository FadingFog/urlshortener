const form = document.getElementById('shorten_form')
const full_url = document.getElementById('id_full_url')

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        let cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            let cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

const csrftoken = getCookie('csrftoken');

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});

form.addEventListener('submit', ev => {
    ev.preventDefault()

    const fd = new FormData()
    fd.append('full_url', full_url.value)

    $.ajax({
        method: 'POST',
        url: '',
        enctype: 'multipart/form-data',
        data: fd,
        success: handleFormSuccess,
        error: handleFormError,
        cache: false,
        contentType: false,
        processData: false
    })

    function handleFormSuccess(response) {
        console.log(response)

        if ($("div#results").length === 0) {
            let result_box = '<div id="results" class="container mt-4">' +
                '<div class="row"><div class="col-12"><div id="alert-box">' +
                '<div id="result-message" class="alert alert-success text-center p-2"></div>' +
                '</div></div></div></div>';
            $("section.main").append(result_box)
        }

        if (response.status === 'success') {
            full_url.setAttribute('class', 'form-control is-valid')
            $("#result-message").attr('class', 'alert alert-success text-center p-2').text(response.message)

            if ($("#link-info").length === 0) {$("#results .col-12").append(response.html)}
            else {$("#link-info").replaceWith(response.html)}

        } else {
            full_url.setAttribute('class', 'form-control is-invalid')
            $("#result-message").attr('class', 'alert alert-danger text-center p-2').text(response.errors.full_url[0])
        }
    }

    function handleFormError(error){
        console.log(error)
    }
});
