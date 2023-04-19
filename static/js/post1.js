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
            document.getElementById('comment').removeAttribute('id');
            var newBlock = document.createElement("id");
            newBlock.setAttribute("id", 'comment');
            document.getElementById('comments').appendChild(newBlock);
        }
        })
    })
}

function deleteComment(){
    $('#delete_comment').click(function(){
        var del_btn = $(this);
        $.ajax(del_btn.data('url'), {
            'type': 'POST';
            'async': true,
            'dataType': 'json',
            'data': {
                'csrfmiddlewaretoken': $('input[name="csrfmiddlewaretoken"]').val(),
                'delete_comment': del_btn.data('id')
            },
            'success': function(data){
                document.getElementById(data['id']).remove();
            }
        })
    })
}

$(document).ready(function(){
    var like = $('#image');
    if (typeof $.cookie('like'+like.data('id')) == 'undefined') {
        $.cookie('like'+like.data('id'), 0, {'expires': 1000000});
    }
    if ($.cookie('like'+like.data('id')) == 0) {
        document.getElementById('image').src = '/static/design/like.png';
    } else {
        document.getElementById('image').src = '/static/design/a_like.png';
    }
    deleteComment();
    addComment();
    processLike();
});

