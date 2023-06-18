function updateData(){
    $('#submit').click(function(){
        btn = $(this);
        if ($('#url_info').val() == '/edit_profile/') {
        var formData = new FormData();
        formData.append("file", document.getElementById('prof_img').files[0]);
        formData.append('bio', $('#id_bio').val());
        formData.append('gender', $('#id_gender').val());
        formData.append('website', $('#id_website').val());
        formData.append('csrfmiddlewaretoken', $('input[name="csrfmiddlewaretoken"]').val());
        $.ajax($('#url_info').val(), {
            'type': 'POST',
            'async': true,
            'dataType': 'json',
            'data': formData,
            'processData': false,
            'contentType': false,
            'success': function(data){
                document.getElementById('success').classList.add('success_anim');
                setTimeout(function(){
                    document.getElementById('success').classList.remove('success_anim');
                }, 8000);
                document.getElementById('id_bio').value = data['bio'];
                document.getElementById('id_gender').value = data['gender'];
                document.getElementById('id_website').value = data['website'];
                if ('image' in data) {
                    document.getElementById('profile_image').src = data['image'];
                }
            }
        })
    } else if ($('#url_info').val() == '/personal_info/'){
        $.ajax($('#url_info').val(), {
            'type': 'POST',
            'async': true,
            'dataType': 'json',
            'data': {
                'csrfmiddlewaretoken': $('input[name="csrfmiddlewaretoken"]').val(),
                'username': $('#id_username').val(),
                'first_name': $('#id_first_name').val(),
                'last_name': $('#id_last_name').val()
            },
            'success': function(data){

                if ('error' in data) {
                    document.getElementById('errors').innerHTML = `<p class="text-danger h6 float-end"><b>${data['error']}</b></p>`;
                } else {
                    document.getElementById('errors').innerHTML = '';
                    document.getElementById('success').classList.add('success_anim');
                    setTimeout(function(){
                        document.getElementById('success').classList.remove('success_anim');
                    }, 8000);
                    document.getElementById('id_username').value = data['username'];
                    document.getElementById('id_first_name').value = data['first_name'];
                    document.getElementById('id_last_name').value = data['last_name'];
                }
            }
        })
    } else if ($('#url_info').val() == '/security/') {
        $.ajax($('#url_info').val(), {
            'type': 'POST',
            'async': true,
            'dataType': 'json',
            'data': {
                'csrfmiddlewaretoken': $('input[name="csrfmiddlewaretoken"]').val(),
                'username': $('#id_password').val(),
            },
            'success': function(data){

                if ('error' in data) {
                    document.getElementById('errors').innerHTML = `<p class="text-danger h6 float-end"><b>${data['error']}</b></p>`;
                } else {
                    document.getElementById('errors').innerHTML = '';
                    document.getElementById('success').classList.add('success_anim');
                    setTimeout(function(){
                        document.getElementById('success').classList.remove('success_anim');
                    }, 8000);
                    document.getElementById('id_username').value = data['username'];
                    document.getElementById('id_first_name').value = data['first_name'];
                    document.getElementById('id_last_name').value = data['last_name'];
                }
            }
        })
    } else if ($('#url_info').val() == '/notifications/') {
        $.ajax($('#url_info').val(), {
            'type': 'POST',
            'async': true,
            'dataType': 'json',
            'data': {
                'csrfmiddlewaretoken': $('input[name="csrfmiddlewaretoken"]').val(),
                'email': $('#id_email').val(),
            },
            'success': function(data){

                if ('error' in data) {
                    document.getElementById('errors').innerHTML = `<p class="text-danger h6 float-end"><b>${data['error']}</b></p>`;
                } else {
                    document.getElementById('errors').innerHTML = '';
                    document.getElementById('success').classList.add('success_anim');
                    setTimeout(function(){
                        document.getElementById('success').classList.remove('success_anim');
                    }, 8000);
                    document.getElementById('id_email').value = data['email'];
                }
            }
        })
    }

})
}

function genderChoose(){
    $('#id_gender').click(function(){
        document.getElementById('gender').show();
         document.getElementById('main').inert = true;
         document.getElementById('quit').classList.remove('quit_wait');
    })
}

function closeDialogue() {
    $('#quit').click(function(){
        document.getElementById("gender").close();
        document.getElementById('main').inert = false;
        document.getElementById('quit').classList.add('quit_wait');
    })
}

function enterGender() {
    $('#enter_gender').click(function(){
        if (document.getElementById('male').checked){
            document.getElementById('id_gender').value = 'Male';
        } else if (document.getElementById('female').checked){
            document.getElementById('id_gender').value = 'Female';
        } else {
            document.getElementById('id_gender').value = 'Custom';
        }
        document.getElementById("gender").close();
        document.getElementById('main').inert = false;
        document.getElementById('quit').classList.add('quit_wait');
    })
}


$(document).ready(function(){
    updateData();
    genderChoose();
    closeDialogue();
    enterGender();
    $.ajax($('#url_info').val(), {
        'type': 'POST',
        'async': true,
        'dataType': 'json',
        'data': {
            'csrfmiddlewaretoken': $('input[name="csrfmiddlewaretoken"]').val()
        },
        'success': function(data){
            if (data['select'] == 'profile'){
                document.getElementById('id_bio').value = data['bio'];
                document.getElementById('id_gender').value = data['gender'];
                document.getElementById('id_website').value = data['website'];
            } else if (data['select'] == 'personal'){
                document.getElementById('id_username').value = data['username'];
                document.getElementById('id_first_name').value = data['first_name'];
                document.getElementById('id_last_name').value = data['last_name'];
            } else if (data['select'] == 'notifications'){
                document.getElementById('id_email').value = data['email'];
            }
        }
    });
    $('#change_img').on('click', function(e) {
        e.preventDefault();
        $('#prof_img').trigger('click');
    });
})