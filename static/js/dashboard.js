function ajaxPagination() {
    $('a.page-link').each((index, el) => {
        $(el).click((e) => {
            e.preventDefault()
            let page_url = $(el).attr('href')
            console.log(page_url)

            $.ajax({
                url: page_url,
                type: 'GET',
                success: (data) => {
                    $('#url-list').empty().append($(data).find('#url-list').html())
                    $('.pagination').empty().append($(data).find('.pagination').html())
                }
            });
        });
    });
}

$(document).ready(function() {
    ajaxPagination()
})

$(document).ajaxStop(function() {
    ajaxPagination()
})