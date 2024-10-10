document.addEventListener('DOMContentLoaded', function() {
  const uploadInput = document.getElementById('upload');
  if (uploadInput) {
      uploadInput.addEventListener('change', function(event) {
          const file = event.target.files[0];
          if (file) {
            const fileType = file.type.split('/')[0];
            const fileURL = URL.createObjectURL(file);

            const imagePreview = document.getElementById('imagePreview');
            const videoPreview = document.getElementById('videoPreview');

            if (fileType === 'image') {
                imagePreview.src = fileURL;
                imagePreview.style.display = 'block';
                videoPreview.style.display = 'none';
            } else if (fileType === 'video') {
                videoPreview.src = fileURL;
                videoPreview.style.display = 'block';
                videoPreview.load();
                imagePreview.style.display = 'none';
            }
        }
      });
  }
});

function readURL(input) {
    if (input.files && input.files[0]) {
        var file = input.files[0];
        var fileType = file.type;
        var reader = new FileReader();

        reader.onload = function(e) {
            $('.image-upload-wrap').hide();
            $('#webcamButton').hide(); // Menyembunyikan tombol Webcam

            if (fileType.startsWith('image')) {
                $('.file-upload-image').attr('src', e.target.result);
                $('.file-upload-image').show();
                $('.file-upload-video').hide();
            } else if (fileType.startsWith('video')) {
                $('.file-upload-video').attr('src', e.target.result);
                $('.file-upload-video').show();
                $('.file-upload-image').hide();
                $('.file-upload-video')[0].load(); // Load the new video source
            }

            $('.file-upload-content').show();
            $('.image-title').html(file.name);
        };

        if (fileType.startsWith('image')) {
            reader.readAsDataURL(file);
        } else if (fileType.startsWith('video')) {
            reader.readAsDataURL(file);
        }
    } else {
        removeUpload();
    }
}

function removeUpload() {
  $('.file-upload-input').replaceWith($('.file-upload-input').clone());
  $('.file-upload-content').hide();
  $('.image-upload-wrap').show();
  $('#webcamButton').show(); // Menampilkan kembali tombol Webcam
}
$('.image-upload-wrap').bind('dragover', function () {
		$('.image-upload-wrap').addClass('image-dropping');
	});
	$('.image-upload-wrap').bind('dragleave', function () {
		$('.image-upload-wrap').removeClass('image-dropping');
});
