document.addEventListener('DOMContentLoaded', function() {
    const imageInput = document.getElementById('imageInput');
    const chooseImageBtn = document.getElementById('chooseImageBtn');
    const imagePreview = document.getElementById('imagePreview'); // Fixed typo: was 'imgePreview'
    const form = document.getElementById('handcraftForm');

    chooseImageBtn.addEventListener('click', function() {
        imageInput.click();
    });

    imageInput.addEventListener('change', function(e) {
        const file = e.target.files[0];
        if (file) {
            const reader = new FileReader();
            reader.onload = function(event) {
                const img = new Image();
                img.onload = function() {
                    const canvas = document.createElement('canvas');
                    const ctx = canvas.getContext('2d');
                    const DESIRED_WIDTH = 286;
                    const DESIRED_HEIGHT = 382;
                    let width = img.width;
                    let height = img.height;

                    // Calculate the new dimensions while maintaining the aspect ratio
                    if (width > height) {
                        if (width > DESIRED_WIDTH) {
                            height *= DESIRED_WIDTH / width;
                            width = DESIRED_WIDTH;
                        }
                    } else {
                        if (height > DESIRED_HEIGHT) {
                            width *= DESIRED_HEIGHT / height;
                            height = DESIRED_HEIGHT;
                        }
                    }

                    canvas.width = DESIRED_WIDTH;
                    canvas.height = DESIRED_HEIGHT;
                    ctx.drawImage(img, 0, 0, width, height, 0, 0, DESIRED_WIDTH, DESIRED_HEIGHT);

                    canvas.toBlob(function(blob) {
                        const resizedFile = new File([blob], file.name, {
                            type: 'image/jpeg',
                            lastModified: Date.now()
                        });

                        const dataTransfer = new DataTransfer();
                        dataTransfer.items.add(resizedFile);
                        imageInput.files = dataTransfer.files;

                        imagePreview.src = URL.createObjectURL(resizedFile);
                        imagePreview.style.display = 'block';
                    }, 'image/jpeg', 0.85);
                };
                img.src = event.target.result;
            };
            reader.readAsDataURL(file);
        }
    });
});
