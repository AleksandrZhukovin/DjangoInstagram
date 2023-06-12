function processLike(){
    $('.like').click(function(){
    var like = $(this);
    $.ajax(like.data('url'), {
        'type': 'POST',
        'async': true,
        'dataType': 'json',
        'data': {
            'add_like': 1,
            'csrfmiddlewaretoken': $('input[name="csrfmiddlewaretoken"]').val()
        },
        'success': function(data){
            var d = data['like_amount'];
            var n = document.getElementById('like');
            n.innerHTML = d;
            var i = $('#image-like');
            if (data['is_liked'] == 0) {
               document.getElementById('image-like').src = '/static/design/like.png';
               document.getElementsByClassName('is_liked').item(0).dataset.for = 0;
            } else {
               document.getElementById('image-like').src = '/static/design/a_like.png';
               document.getElementsByClassName('is_liked').item(0).dataset.for = 1;
            }
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
        'success':  function(data){$
            document.getElementById('id_body').value = '';
            document.getElementById('comments').innerHTML += data;
        }
    })
})
}


$(function(){
    $(document).click(function(event) {
    b_id = $(event.target);
    if (b_id.attr('class') == "btn_add mx-2") {
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
            var elements = document.getElementsByClassName('comment_block');
            for (var i=0; i < elements.length; i++) {
                if (elements.item(i).getElementsByClassName('comment_like').item(0).getAttribute('data-id') == data['id']) {
                    if (data['is_liked'] == 0) {
                        elements.item(i).getElementsByClassName('is_liked').item(0).dataset.for = 0;
                        elements.item(i).getElementsByClassName("comment_like mb-2").item(0).src = "/static/design/like.png";
                        elements.item(i).getElementsByClassName("text-white-50 mx-2").item(1).innerHTML = data['like_am'];
                    } else {
                        elements.item(i).getElementsByClassName('is_liked').item(0).dataset.for = 1;
                        elements.item(i).getElementsByClassName("comment_like mb-2").item(0).src = "/static/design/a_like.png";
                        elements.item(i).getElementsByClassName("text-white-50 mx-2").item(1).innerHTML = data['like_am'];
                    }
                }
            }
                }

        })
    }
    })
})

$(function(){
    $(document).click(function(event) {
        b_id = $(event.target);
        if (b_id.attr('class') == 'post_image my-2' || b_id.attr('class') == 'comment_ico') {
            document.getElementById('post').show();
            document.getElementById('quit').classList.remove('quit_wait');
            document.getElementById('main').inert = true;
            $.ajax('/', {
                'type': 'POST',
                'async': true,
                'dataType': 'json',
                'data': {
                    'csrfmiddlewaretoken': $('input[name="csrfmiddlewaretoken"]').val(),
                    'id': b_id.attr('data-id')
                },
                'success': function(data){
                    document.getElementById('post').innerHTML = data;
                    var elements = document.getElementsByClassName('comment_block');
                    for (var i=0; i < elements.length; i++) {
                        if (elements.item(i).getElementsByClassName('is_liked').item(0).getAttribute('data-for') == 0) {
                            elements.item(i).getElementsByClassName("comment_like mb-2").item(0).src = "/static/design/like.png";
                        } else {
                            elements.item(i).getElementsByClassName("comment_like mb-2").item(0).src = "/static/design/a_like.png";
                        }
                    }

                    var elements = document.getElementsByClassName('block my-2 likes');
                    if (elements.item(0).getElementsByClassName('post_is_liked').item(0).getAttribute('data-for') == 0) {
                        elements.item(0).getElementsByClassName("like").item(0).src = "/static/design/like.png";
                    } else {
                        elements.item(0).getElementsByClassName("like").item(0).src = "/static/design/a_like.png";
                    }
                     addComment();
                     processLike();
                }
            })
        }
    })
})

