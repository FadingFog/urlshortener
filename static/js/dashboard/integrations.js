import {genTooltip, initTooltips, ajax} from "../utils.js";

initTooltips()


// Section - Create API key
const tt_copy = "Copy to clipboard"

let el = $('div#createTokenModal div.modal-body > p'),
    new_text = "Coming soon..";

let applyModalHandlers = () => {
    el = $('div#createTokenModal div.modal-body > p');
    $('#switchSecretPublic').on('change', () => {
        let old_text = el.text();
        console.log('Should be replaced to: ' + new_text)
        el.html(new_text);
        new_text = old_text;

        $('#createToken').toggleClass('disabled');
    });

    $('#createToken').on('click', (ev) => {
        ev.preventDefault()
        $.ajax({
            method: 'POST',
            url: '/api/auth/',
            success: handleCreateSuccess,
            error: (error) => console.error(error),
            cache: false,
            contentType: false,
            processData: false
        });
    });
};
applyModalHandlers();


function handleCreateSuccess(response) {
    $('#tokenModalLabel').html("Created API key");
    let newModalBody = `<div class="d-flex justify-content-center align-items-center gap-2 text-muted">
                            <strong>${response.token}</strong>
                            <button class="btn btn-dark btn-clipboard"><i class="bi bi-clipboard"></i></button>
                        </div>`
    $('#createTokenModal .modal-body').html(newModalBody);
    genTooltip('.btn-clipboard', tt_copy);

    let newModalFooter = '<button class="btn btn-outline-success btn-clear text-uppercase fw-500" type="button" data-bs-dismiss="modal" id="closeModal">Ok</button>'
    $('#createTokenModal .modal-footer').html(newModalFooter);

    $('#createTokenModal #closeModal').on('click', () => setTimeout(replaceModal, 500));
    pollForTokenChanges()
}

let orig_modalToken = $('#createTokenModal .modal-dialog').html()
let replaceModal = () => {
    $('#createTokenModal .modal-content').replaceWith(orig_modalToken);
    applyModalHandlers();
}

const n = new ClipboardJS('.btn-clipboard', {
    target: function(trigger) {
        return trigger.previousElementSibling;
    }
});
n.on('success', (t) => {
    document.activeElement.blur();
    window.getSelection().removeAllRanges();
    let o = bootstrap.Tooltip.getInstance(t.trigger),
        i_el = t.trigger.firstChild;
    o.setContent({
        '.tooltip-inner': "Copied!"
    });
    t.trigger.addEventListener("hidden.bs.tooltip", () => {
        o.setContent({
            '.tooltip-inner': tt_copy
        })
    }, {
        once: !0
    });
    i_el.classList.replace('bi-clipboard', 'bi-check2');
    setTimeout(() => i_el.classList.replace('bi-check2','bi-clipboard'), 2000)
});
n.on("error", t => {
    let s = /mac/i.test(navigator.userAgent) ? "\u2318" : "Ctrl-",
        tt_text = `Press ${s}C to copy`,
        tt = bootstrap.Tooltip.getInstance(t.trigger);
    tt.setContent({
        '.tooltip-inner': tt_text
    });
    t.trigger.addEventListener("hidden.bs.tooltip", () => {
        tt.setContent({
            '.tooltip-inner': tt_copy
        })
    }, {
        once: !0
    });
});


// Section - Your Keys
let sTokens = $('#secretTokens'),
    pTokens = $('#publicTokens'),
    token;


$('#deleteTokenModal').on('show.bs.modal', function (e) {
    let invoker = $(e.relatedTarget);
    token = invoker.prev();
});


$('#deleteToken').on('click', (ev) => {
        ev.preventDefault()

        $.ajax({
            method: 'DELETE',
            url: `/api/auth/${token.text()}/`,
            success: () => {
                token.parent().remove();
                $('#deleteTokenModal').modal('hide');
                pollForTokenChanges();
            },
            error: (error) => console.error(error),
            cache: false,
            contentType: false,
            processData: false
        });
    });


async function pollForTokenChanges() {
    let tokens = await ajax('/api/auth/');
    [sTokens, pTokens].forEach(t => t.empty());

    if (tokens.length) {
        for (let token of tokens) {
            let key = token.key
            let tokenContainerContent = `<li class="list-group-item d-flex justify-content-between align-items-center mx-3">
                                            <span>${key}</span>
                                            <button class="btn btn-dark" type="button" data-bs-toggle="modal"
                                                data-bs-target="#deleteTokenModal">
                                            <i class="bi bi-trash"></i>
                                            </button>
                                        </li>`

            if (!token.isPublic) {
                sTokens.append(tokenContainerContent)
            } else {
                pTokens.append(tokenContainerContent)
            }
        }
    }

    let tokenContainers = {'private': sTokens, 'public': pTokens};
    for (let [tokenType, tokenContainer] of Object.entries(tokenContainers)) {
        if (!tokenContainer.children().length) {
            tokenContainer.append(`<p class="text-muted text-center fs-7 mt-3">You don't have ${tokenType} keys.</p>`)
        }
    }
}