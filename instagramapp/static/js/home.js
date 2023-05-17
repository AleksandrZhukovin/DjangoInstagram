$(function(){
    $(document).click(function(event) {
    b_id = $(event.target);
    console.log(b_id.attr('class'));
    if (b_id.attr('class') == 'like_btn') {
    console.log(b_id);
    $.ajax(b_id.data('url'), {
        'type': 'POST',
        'async': true,
        'dataType': 'json',
        'data': {
            'like_post': b_id.data('id'),
            'csrfmiddlewaretoken': $('input[name="csrfmiddlewaretoken"]').val()
        },
        'success': function(data){
            var elements = document.getElementsByClassName('likes');
            for (var i=0; i < elements.length; i++) {
                if (elements.item(i).getAttribute('data-id') == data['id']) {
                    if (data['is_liked'] == 0) {
                        elements.item(i).getElementsByClassName('is_liked').item(0).dataset.for = 0;
                        elements.item(i).getElementsByClassName("like_btn").item(0).src = "/static/design/like.png";
                        elements.item(i).getElementsByClassName("like_amount").item(0).innerHTML = data['like_am'];
                    } else {
                        elements.item(i).getElementsByClassName('is_liked').item(0).dataset.for = 1;
                        elements.item(i).getElementsByClassName("like_btn").item(0).src = "/static/design/a_like.png";
                        elements.item(i).getElementsByClassName("like_amount").item(0).innerHTML = data['like_am'];
                    }
                }
            }
        }
    })
}})})

$(document).ready(function(){
    var elements = document.getElementsByClassName('likes');
    for (var i=0; i < elements.length; i++) {
        if (elements.item(i).getElementsByClassName('is_liked').item(0).getAttribute('data-for') == 0) {
            elements.item(i).getElementsByClassName("like_btn").item(0).src = "/static/design/like.png";
        } else {
            elements.item(i).getElementsByClassName("like_btn").item(0).src = "/static/design/a_like.png";
        }
    }

});