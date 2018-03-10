$(function(){
// SCRIPT TO OPEN the MODAL With the Preview
    $('#id_picture').change(function() {
        if(this.files && this.files[0]) {
            var reader = new FileReader();
            reader.onload = function(e) {
                $('#image').attr('src', e.target.result);
                $('#modalCrop').fadeIn('fast');
            }
            reader.readAsDataURL(this.files[0]);
        }
    });

    // SCRIPTS TO HANDLE THE CROPPER BOX
    var $image = $('#image');
    var cropBoxData;
    var canvasData;

    $image.on('load', function(){
        $image.cropper({
            viewMode: 1,
            aspectRatio: 1 / 1,
            minCropBoxWidth: 200,
            minCropBoxHeight: 200,
            ready: function() {
                $image.cropper('setCanvasData', canvasData);
                $image.cropper('setCropBoxData', cropBoxData);
            },
        });
        cropData = $image.cropper('getData');
        console.log("first : "+cropData);
    }).on('fadeout', function() {
        cropBoxData = $image.cropper('getCropBoxData');
        canvasData = $image.cropper('getCanvasData');
        $image.cropper('destory');
    });

    // SCRIPT TO COLLECT THE DATA AND POST TO THE SERVER
    $('.btn-crop').click(function(){
        var cropData = $image.cropper('getData');
        $('#id_x').val(cropData['x']);
        $('#id_y').val(cropData['y']);
        $('#id_height').val(cropData['height']);
        $('#id_width').val(cropData['width']);

        var nickname = $("#id_nickname").val();
        if (nickname.length >= 2){
            $("#btn-profile").prop("disabled", true);
            $("#formProfile").submit();
        }
    });
});