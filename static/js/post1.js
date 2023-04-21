function processLike(){
    $('.like').click(function(){
    var like = $(this);
    $.ajax(like.data('url'), {
        'type': 'POST',
        'async': true,
        'dataType': 'json',
        'data': {
            'pk': like.data('id'),
            'add_like': 1,
            'csrfmiddlewaretoken': $('input[name="csrfmiddlewaretoken"]').val()
        },
        'success': function(data){
            var d = data['like_amount'];
            var n = document.getElementById('like');
            n.innerHTML = d;
            var i = $('#image');
            var is_like = 0;
            if ($.cookie('like'+like.data('id')) == 0) {
                is_like = 1;
                document.getElementById('image').src = '/static/design/a_like.png';
            } else {
                is_like = 0;
                document.getElementById('image').src = '/static/design/like.png';
            }
            $.cookie('like'+like.data('id'), is_like, {'expires': 1000000});
        }
    })
    })
}

function addComment(){
    $('#input').click(function(){
        var comment_btn = $(this);
        $.ajax(comment_btn.data('url'),{
        'type': 'POST',
        'async': true,
        'dataType': 'json',
        'data': {
            'pk': comment_btn.data('id'),
            'body': $('.form_e').val(),
            'csrfmiddlewaretoken': $('input[name="csrfmiddlewaretoken"]').val()
        },
        'success':  function(data){
            document.getElementById('id_body').value = '';
            var div = document.createElement('div');
            div.innerHTML = data.trim();
            document.getElementById('comments').appendChild(div);
        }
        })
    })
}

$(document).click(function(event) {
    b_id = $(event.target);
    if (b_id.attr('class') == "sm_info mx-2") {
        $.ajax(b_id.data('url'), {
            'type': 'POST',
            'async': true,
            'dataType': 'json',
            'data': {
                'delete_comment': b_id.data('id'),
                'csrfmiddlewaretoken': $('input[name="csrfmiddlewaretoken"]').val()
            },
            'success': function(data){
                document.getElementById(String(data['id'])).remove();
            }
    })} else if (b_id.attr('class') == "comment_like mb-2") {
        $.ajax(b_id.data('url'), {
        'type': 'POST',
        'async': true,
        'dataType': 'json',
        'data': {
            'like_comment': b_id.data('id'),
            'csrfmiddlewaretoken': $('input[name="csrfmiddlewaretoken"]').val()
        },
        'success': function(data){
            var elements = document.getElementsByClassName('comment');
            for (var i=0; i < elements.length; i++) {
                if (elements.item(i).getElementsByClassName('comment_like').item(0).getAttribute('data-id') == data['id']) {
                    if (data['is_liked'] == 0) {
                        elements.item(i).getElementsByClassName('is_liked').item(0).dataset.for = 0;
                        elements.item(i).getElementsByClassName("comment_like mb-2").item(0).src = "/static/design/like.png";
                        elements.item(i).getElementsByClassName("sm_info mx-2").item(1).innerHTML = data['like_am'];
                    } else {
                        elements.item(i).getElementsByClassName('is_liked').item(0).dataset.for = 1;
                        elements.item(i).getElementsByClassName("comment_like mb-2").item(0).src = "/static/design/a_like.png";
                        elements.item(i).getElementsByClassName("sm_info mx-2").item(1).innerHTML = data['like_am'];
                    }
                }
            }
                }

        })
    }
    })

$(document).ready(function(){
    var elements = document.getElementsByClassName('comment');
    for (var i=0; i < elements.length; i++) {
        if (elements.item(i).getElementsByClassName('is_liked').item(0).getAttribute('data-for') == 0) {
            elements.item(i).getElementsByClassName("comment_like mb-2").item(0).src = "/static/design/like.png";
        } else {
            elements.item(i).getElementsByClassName("comment_like mb-2").item(0).src = "/static/design/a_like.png";
        }
    }

    var like = $('#image');
    if (typeof $.cookie('like'+like.data('id')) == 'undefined') {
        $.cookie('like'+like.data('id'), 0, {'expires': 1000000});
    }
    if ($.cookie('like'+like.data('id')) == 0) {
        document.getElementById('image').src = '/static/design/like.png';
    } else {
        document.getElementById('image').src = '/static/design/a_like.png';
    }
    addComment();
    processLike();
});
