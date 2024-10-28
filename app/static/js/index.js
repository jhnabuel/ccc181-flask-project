document.getElementById('image_url').addEventListener('change', previewImage);

function previewImage(event) {
    const imagePreview = document.getElementById('image_preview');
    const file = event.target.files[0];

    if (file) {
        const reader = new FileReader();
        reader.onload = function(e) {
            imagePreview.src = e.target.result;
        };
        reader.readAsDataURL(file);
    } else {
        imagePreview.src = ''; // Reset if no image is selected
    }
}
