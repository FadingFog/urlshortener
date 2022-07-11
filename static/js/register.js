const form = document.getElementById('register'),
    {username, email, password1, password2} = form.getElementsByTagName("input"),
    form_els = [username, email, password1, password2],
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
        window.location.href = new URLSearchParams(window.location.search).get("next") || '/login';
    }

    function handleFormError(response) {
        let errors = response.responseJSON.errors
        $(invalid_sel).remove();  // remove existing errors

        for (let el of form_els) {  // for every form element
            el.container = $(el).parent();
            el.setAttribute('class', 'form-control');

            if (el.name in errors) {  // if element in error list
                el.errors = errors[el.name];

                el.setAttribute('class', 'form-control is-invalid');
                el.container.append('<div class="invalid-feedback"></div>');
                $(el.container).attr('class', 'form-floating mb-1')
                $(el.container).children(invalid_sel).text(el.errors.map(i => i.message).join('\n'));
            } else {
                $(el.container).attr('class', 'form-floating mb-3')
            }
        }
    }
});