const form = document.getElementById('password_reset');
const email = document.getElementById('floatingInputEmail');


form.addEventListener('submit', ev => {
    ev.preventDefault();

    const fd = new FormData();
    fd.append('email', email.value);

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
    });

    function handleFormSuccess(response, textStatus, xhr) {
        if (xhr.status === 200) {
            $('#password-reset .row').empty().append($(response).html());
        } else {
            console.log('Something went wrong');
            console.log(xhr);
        }
    }

    function handleFormError(response) {
        $('p.hint').empty().append($(response.responseText).find('p.hint').html());
    }
});