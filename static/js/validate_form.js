function comparePasswords() {
    let p1 = $("input[name=password1]"),
        p2 = $("input[name=password2]");
    if (p1.val()) {
        if (p1.val() === p2.val()) {
            p2.attr('class', 'form-control is-valid')
        } else {
            p2.attr('class', 'form-control is-invalid');
        }
    } else {
        p2.attr('class', 'form-control')
    }
}