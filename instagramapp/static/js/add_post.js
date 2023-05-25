function showDialog(){
    $('#open').click(function(){
        document.getElementById("choose").show();
    })
}

function describeDialog(data) {
    document.getElementById("describe").show();
    console.log(data);
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
        describeDialog($("#id_image").val());
    })
}

$(document).ready(function(){
    showDialog();
    nextDialog();
    $('.file-upload').on('click', function(e) {
        e.preventDefault();
    $('#id_image').trigger('click');
    });
})