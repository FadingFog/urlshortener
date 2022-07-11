const form = document.getElementById('login'),
    username = document.getElementById('floatingInputUsername'),
    passwrd = document.getElementById('floatingPassword'),
    invalid_sel = 'div.invalid-feedback';


form.addEventListener('submit', ev => {
    ev.preventDefault();

    const fd = new FormData(form);

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

    function handleFormSuccess(response) {
        $(invalid_sel).remove();
        sessionStorage.setItem('message', response.message);
        window.location.href = new URLSearchParams(window.location.search).get("next") || '/';
    }

    function handleFormError(response) {
        let errors = response.responseJSON.errors['__all__'];
        $(invalid_sel).remove();  // remove existing errors

        [username, passwrd].forEach(e => e.setAttribute('class', 'form-control is-invalid'));
        $(passwrd).parent().append('<div class="invalid-feedback"></div>')
        $(invalid_sel).text(errors.map(i => i.message).join('\n'));
    }
});