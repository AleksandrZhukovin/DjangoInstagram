$(function(){
    $('#id_search').keyup(function(){
        $.ajax('/search/', {
            'type': 'POST',
            'async': true,
            'dataType': 'json',
            'data': {
                'csrfmiddlewaretoken': $('input[name="csrfmiddlewaretoken"]').val(),
                'input': $(this).val()
            },
            'success': function(data){
                document.getElementById('result').innerHTML = data;
            }
        })
    })
})
