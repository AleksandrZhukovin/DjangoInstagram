function showDialog(){
    $('#open').click(function(){
        document.getElementById("choose").show();
        document.getElementById('main').inert = true;
        document.getElementById('quit').classList.remove('quit_wait');
    })
}

function closeDialogue() {
    $('#quit').click(function(){
        document.getElementById("choose").close();
        document.getElementById("describe").close();
        document.getElementById('post').close();
        document.getElementById('main').inert = false;
        document.getElementById('quit').classList.add('quit_wait');
    })
}


function nextDialog(){
    $('#id_image').change(function(){
        var formData = new FormData();

        formData.append("file", document.getElementById('id_image').files[0]);
        formData.append('csrfmiddlewaretoken', $('input[name="csrfmiddlewaretoken"]').val());

        $.ajax('/add_post/', {
            'type': "POST",
            'async': true,
            'dataType': 'json',
            'data': formData,
            'processData': false,
            'contentType': false,
            'success': function(data){
                document.getElementById('image').src = data;
            }
            })

        document.getElementById("choose").close();
        document.getElementById("describe").show();
    })
}

function sharePost(){
     $('#share').click(function(){
        $.ajax('/add_post/', {
            'type': "POST",
            'async': true,
            'dataType': 'json',
            'data': {
                'csrfmiddlewaretoken': $('input[name="csrfmiddlewaretoken"]').val(),
                'description': $('#description_area').val()
            },
            'success': function(data){
                document.getElementById("choose").close();
                document.getElementById("describe").close();
                document.getElementById('main').inert = false;
                document.getElementById('quit').classList.add('quit_wait');
            }
            })
     })
}

$(document).ready(function(){
    showDialog();
    nextDialog();
    closeDialogue();
    sharePost();
    $('#file_upload').on('click', function(e) {
        e.preventDefault();
    $('#id_image').trigger('click');
    });
    document.getElementById('quit').addEventListener("mouseover", (event) => {
        document.getElementById('quit').src = '/static/design/quit_a.png';
    });
   document.getElementById('quit').addEventListener("mouseleave", (event) => {
        document.getElementById('quit').src = '/static/design/quit.png';
   });

})