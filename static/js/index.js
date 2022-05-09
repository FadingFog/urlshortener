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

    function handleFormSuccess(response){
        console.log(response)
            if(response.status === 'success'){
                full_url.setAttribute('class', 'form-control is-valid');

                $("#link-info").replaceWith(response.html);
                // $("#results .row .col-12").append(response.html);

                $("#results").attr('class', 'container mt-4')
            }
            else{
                full_url.setAttribute('class', 'form-control is-invalid')
            }
    }

    function handleFormError(error){
        console.log(error)
    }
});
