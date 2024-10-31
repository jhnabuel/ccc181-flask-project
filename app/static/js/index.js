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

document.addEventListener("DOMContentLoaded", function() {
    const removePhotoButton = document.getElementById('remove_photo_btn');
    const imagePreview = document.getElementById('image_preview');
    const removeImageInput = document.getElementById('remove_image');
    const fileInput = document.getElementById('image_url');

    removePhotoButton.addEventListener('click', function() {
        // Set the hidden input to true to mark the image for removal
        removeImageInput.value = "true";

        // Update the preview to the placeholder image
        imagePreview.src = 'https://res.cloudinary.com/dzmgvynf3/image/upload/v1234567890/student_photo/placeholder.jpg';

        // Clear the file input
        fileInput.value = '';
    });
});
