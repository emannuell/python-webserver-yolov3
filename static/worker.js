$('#detections').hide()
var $loading = $('#loading').hide();

$('#updateCamera').click(function (event) {
    event.preventDefault();
    const data = {
        "gray": $('#gray').is(":checked"),
        "gaussian": $('#gaussian').is(":checked"),
        "sobel": $('#sobel').is(":checked"),
        "canny": $('#canny').is(":checked")
    }
    console.log(data)
    $.ajax({
        type: 'POST',
        url: '/cameraParams',
        data: data,
        success: function (success) {
            console.log(success)
        }, error: function (error) {
            console.log(error)
        }
    })
});

var loadFile = function (event) {
    var output = document.getElementById('input');
    output.src = URL.createObjectURL(event.target.files[0]);
};

$(document)
    .ajaxStart(function () {
        $loading.show();
    })
    .ajaxStop(function () {
        $loading.hide();
    });

$('#buttonSendPhoto').click(function (event) {
    console.log('bateu aqui')
    $('#detections').hide()
    $('#output').hide()
    event.preventDefault()
    var form_data = new FormData($('#upload-file')[0]);

    $.ajax({
        type: 'POST',
        url: '/detectYolo',
        data: form_data,
        contentType: false,
        cache: false,
        processData: false,
        success: function (data) {
            if (data.detections.length > 0) {
                $('#detections').show()
                data.detections.forEach(element => {
                    console.log(element)
                    $('#tableDetections tr:last').after('<tr><td>' + element[1] + '</td><td>' + element[0] + '</td></tr>');
                });
            }
            $('#output').attr('src', 'data:image/png;base64,' + data.base64);
            $('#output').show();
            console.log('Success!');
        },
        error: function (error) {
            alert(error.responseJSON.message)
        }
    });
});