const form = document.getElementById('password_reset')
const email = document.getElementById('floatingInputEmail')

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
    fd.append('email', email.value)

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

    function handleFormSuccess(response, textStatus, xhr){
        if (xhr.status === 200){
            $('#password-reset .row').empty().append($(response).html())
        }
        else{
            console.log('Something went wrong')
            console.log(xhr)
        }
    }

    function handleFormError(response){
        $('p.hint').empty().append($(response.responseText).find('p.hint').html())
    }
});