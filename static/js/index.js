import {initTooltips} from "./utils.js";

const form = document.getElementById('shorten_form');
const full_url = document.getElementById('id_full_url');


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
    });

    function handleFormSuccess(response) {
        if (!$("div#results").length) {  // if results do not exist append block
            let result_box = ['<div id="results" class="container mt-4"><div class="row">',
                '<div class="col-12"><div id="alert-box"><div id="result-message">',
                '</div></div></div></div></div>'].join('');
            $("section.main").append(result_box);
        }

        full_url.setAttribute('class', 'form-control is-valid');
        $("#result-message").attr('class', 'alert alert-success text-center p-2').text(response.message);

        let link_info = $("#link-info")
        if (link_info.length === 0) {
            $("#results .col-12").append(response.html);
        } else {
            link_info.replaceWith(response.html);
        }

        initTooltips()
    }

    function handleFormError(response) {
        if (!$("div#results").length) {  // if results do not exist append block
            let result_box = ['<div id="results" class="container mt-4"><div class="row">',
                '<div class="col-12"><div id="alert-box"><div id="result-message">',
                '</div></div></div></div></div>'].join('');
            $("section.main").append(result_box);
        }

        let errors = response.responseJSON.errors['full_url'];

        full_url.setAttribute('class', 'form-control is-invalid');
        $("#result-message").attr('class', 'alert alert-danger text-center p-2')
                            .text(errors.map(i => i.message).join('\n'));
    }
});

const n = new ClipboardJS('.btn-clipboard', {
    target: function (trigger) {
        return trigger.previousElementSibling;
    }
});
n.on('success', (t) => {
    document.activeElement.blur();
    window.getSelection().removeAllRanges();
    $(t.trigger).text('Copied!')
    setTimeout(() => $(t.trigger).text('Copy'), 1500);
});
