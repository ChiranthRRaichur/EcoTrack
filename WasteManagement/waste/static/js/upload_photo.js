function uploadPhoto(event) {
    event.preventDefault();
    
    const form = event.target;
    const formData = new FormData(form);

    fetch('/upload_photo/', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.message) {
            alert(data.message);
            // Optional: reset form or redirect
        } else {
            alert('Error: ' + data.error);
        }
    })
    .catch(error => {
        console.error('Upload error:', error);
        alert('An error occurred during upload');
    });
}

// Attach event listener
document.querySelector('form').addEventListener('submit', uploadPhoto);