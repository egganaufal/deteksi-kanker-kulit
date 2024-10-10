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
    var reader = new FileReader();
    reader.onload = function(e) {
      $('.image-upload-wrap').hide();
      $('.file-upload-image').attr('src', e.target.result);
      $('.file-upload-content').show();
      $('.image-title').html(input.files[0].name);
      $('#webcamButton').hide(); // Menyembunyikan tombol Webcam
    };
    reader.readAsDataURL(input.files[0]);
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

document.getElementById('unggah').addEventListener('click', function() {
  submitPopup();
});

function submitPopup() {
  Swal.fire({
      html: `
          <div style="display: flex; flex-direction: column; align-items: center;">
              <h1>Uploud gambar</h1>
              <img src="{{ url_for('static', filename='uploads/' ~ filename) }}" alt="Original Image">
              <br>
              <h1>Detected object</h1>
              <img src="{{ url_for('static', filename='results/' ~ filename) }}" alt="Detected Image">
          </div>
      `,
      showCloseButton: true,
      showConfirmButton: false,
  });
}
