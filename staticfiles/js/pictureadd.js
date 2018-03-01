$(function() {
  $("#id_pictures").change(function() {
    if (this.files && this.files[0]) {
      for (var i = 0; i < this.files.length; i++) {
        console.log("Count : " + i);
        var reader = new FileReader();
        reader.onload = imageIsLoaded;
        reader.readAsDataURL(this.files[i]);
      }
    }
    $(".upload").hide();

    var name = $("#id_name").val();
    if (name.length >= 3){
      $("#btn_ok").click();
      $("#btn_ok").prop("disabled", true);
    }
  });
});

function imageIsLoaded(e) {
  $('#img_id').append('<img class="img" src="' + e.target.result + '" width="150px"  height="150px">');
};

$(document).on('click', '.upload', function(){
    $("#id_pictures").click();
});