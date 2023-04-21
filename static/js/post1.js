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
            document.getElementById('comment').innerHTML = data;
            document.getElementById('id_body').value = '';
        }
        })
    })
}

function likeComment(){
    var b_id = 0;
    $(document).click(function(event) {
        b_id = $(event.target);
        $.ajax(b_id.data('url'), {
            'type': 'POST',
            'async': true,
            'dataType': 'json',
            'data': {
                'like_comment': b_id.data('id'),
                'csrfmiddlewaretoken': $('input[name="csrfmiddlewaretoken"]').val()
            },
            'success': function(data){
                var elements = document.getElementsByClassName('comment_like_btn');
                for (var i=0; i < elements.length; i++) {
                    if (elements.item(i).getAttribute('data-id') == data['id']) {
                        elements.item(i).getElementsByClassName('sm_info mx-2').innerHTML = data['like_am'];
                        var is_like = 0;
                        if ($.cookie('comment_like'+elements.item(i).getAttribute('data-id')) == 0) {
                            is_like = 1;
                            elements.item(i).getElementsByClassName('comment_like_btn').innerHTML = '/static/design/a_like.png';
                        } else {
                            is_like = 0;
                            elements.item(i).getElementsByClassName('comment_like_btn').innerHTML = '/static/design/a_like.png';
                        }
                        $.cookie('comment_like'+elements.item(i).getAttribute('data-id'), is_like, {'expires': 1000000});
                    }
                }
            }
        })
      })
    }


function deleteComment(){
    var b_id = 0;
    $(document).click(function(event) {
        b_id = $(event.target);
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
        })
      })
    }

$(document).ready(function(){
    var elements = document.getElementsByClassName('comment_like_btn');
    for (var i=0; i < elements.length; i++) {
        console.log(elements.item(i).getElementsByClassName('mb-2'));
        if (typeof $.cookie('comment_like'+elements.item(i).getAttribute('data-id')) == 'undefined') {
        $.cookie('comment_like'+elements.item(i).getAttribute('data-id'), 0, {'expires': 1000000});
        }
        if ($.cookie('comment_like'+elements.item(i).getAttribute('data-id')) == 0) {
            elements.item(i).innerHTML = '<img class="mb-2" src="/static/design/like.png" width="12">';
        } else {
            elements.item(i).innerHTML = '<img class="mb-2" src="/static/design/a_like.png" width="12">';
        }
    }
    console.log($.cookie('comment_like146'))
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

