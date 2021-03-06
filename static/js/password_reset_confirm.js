const form = document.getElementById('password_reset_confirm');
const new_password1 = document.getElementById('floatingPassword');
const new_password2 = document.getElementById('floatingPasswordConfirm');


form.addEventListener('submit', ev => {
    ev.preventDefault();

    const fd = new FormData();
    fd.append('new_password1', new_password1.value);
    fd.append('new_password2', new_password2.value);

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
        $('p.hint').each((index, el) => {
            let smth = $(response.responseText).find('p.hint')[index];
            $(el).empty().append($(smth).html());
        });
    }
});