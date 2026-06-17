document.addEventListener('DOMContentLoaded', function() {
    const fileInput = document.getElementById('fileInput');
    const dropZone = document.getElementById('dropZone');
    const uploadPrompt = document.getElementById('uploadPrompt');
    const imagePreviewContainer = document.getElementById('imagePreviewContainer');
    const imagePreview = document.getElementById('imagePreview');
    const removeImageBtn = document.getElementById('removeImageBtn');
    const predictBtn = document.getElementById('predictBtn');
    const uploadForm = document.getElementById('uploadForm');
    
    // Elements for Loading State
    const predictText = document.querySelector('.predict-text');
    const loadingSpinner = document.getElementById('loadingSpinner');
    const loadingText = document.querySelector('.loading-text');

    // Progress bar animation for Result Page
    const progressBars = document.querySelectorAll('.progress-bar-animated-custom');
    if (progressBars.length > 0) {
        // Delay slightly so the animation is visible after page load
        setTimeout(() => {
            progressBars.forEach(bar => {
                const targetWidth = bar.getAttribute('data-width');
                bar.style.width = targetWidth;
            });
        }, 100);
    }

    if (!fileInput) return; // Only run on index page

    // Valid file extensions
    const allowedExtensions = ['jpg', 'jpeg', 'png'];

    // Handle File Selection
    fileInput.addEventListener('change', function(e) {
        handleFiles(this.files);
    });

    // Drag and Drop Events
    ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
        dropZone.addEventListener(eventName, preventDefaults, false);
    });

    function preventDefaults(e) {
        e.preventDefault();
        e.stopPropagation();
    }

    ['dragenter', 'dragover'].forEach(eventName => {
        dropZone.addEventListener(eventName, highlight, false);
    });

    ['dragleave', 'drop'].forEach(eventName => {
        dropZone.addEventListener(eventName, unhighlight, false);
    });

    function highlight(e) {
        dropZone.classList.add('dragover');
    }

    function unhighlight(e) {
        dropZone.classList.remove('dragover');
    }

    dropZone.addEventListener('drop', function(e) {
        const dt = e.dataTransfer;
        const files = dt.files;
        fileInput.files = files; // Assign files to input
        handleFiles(files);
    });

    // Process and Preview Image
    function handleFiles(files) {
        if (files.length === 0) return;
        
        const file = files[0];
        const fileName = file.name.toLowerCase();
        const extension = fileName.split('.').pop();
        
        // Validation
        if (!allowedExtensions.includes(extension)) {
            alert('Format file tidak didukung! Harap gunakan format JPG, JPEG, atau PNG.');
            resetUploadState();
            return;
        }

        // Preview Image
        const reader = new FileReader();
        reader.readAsDataURL(file);
        reader.onloadend = function() {
            imagePreview.src = reader.result;
            
            // UI Toggle with simple animation effect
            uploadPrompt.classList.add('d-none');
            imagePreviewContainer.classList.remove('d-none');
            
            // Enable and add pulse effect to button
            predictBtn.removeAttribute('disabled');
            predictBtn.classList.add('btn-pulse');
        }
    }

    // Remove Image
    removeImageBtn.addEventListener('click', function(e) {
        e.preventDefault();
        resetUploadState();
    });

    function resetUploadState() {
        fileInput.value = '';
        imagePreview.src = '#';
        uploadPrompt.classList.remove('d-none');
        imagePreviewContainer.classList.add('d-none');
        
        predictBtn.setAttribute('disabled', 'true');
        predictBtn.classList.remove('btn-pulse');
    }

    // Handle Form Submit (Loading State)
    uploadForm.addEventListener('submit', function(e) {
        // Tampilkan loading spinner
        predictBtn.setAttribute('disabled', 'true');
        predictBtn.classList.remove('btn-pulse');
        predictText.classList.add('d-none');
        loadingSpinner.classList.remove('d-none');
        loadingText.classList.remove('d-none');
    });
});