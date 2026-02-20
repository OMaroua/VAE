<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Variational Autoencoder Denoising Interface</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Georgia', 'Times New Roman', serif;
            background: #f5f5f5;
            color: #2c3e50;
            line-height: 1.6;
            min-height: 100vh;
            padding: 0;
        }

        .header {
            background: #2c3e50;
            color: white;
            padding: 30px 20px;
            text-align: center;
            border-bottom: 3px solid #34495e;
        }

        .header h1 {
            font-size: 2em;
            font-weight: 400;
            margin-bottom: 8px;
            letter-spacing: 0.5px;
        }

        .header .subtitle {
            font-size: 1em;
            opacity: 0.9;
            font-weight: 300;
        }

        .container {
            max-width: 1200px;
            margin: 40px auto;
            padding: 0 20px;
        }

        .main-content {
            background: white;
            border: 1px solid #e0e0e0;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
            padding: 40px;
            margin-bottom: 30px;
        }

        .section-title {
            font-size: 1.4em;
            font-weight: 400;
            color: #2c3e50;
            margin-bottom: 25px;
            padding-bottom: 10px;
            border-bottom: 2px solid #ecf0f1;
        }

        .upload-area {
            border: 2px dashed #95a5a6;
            border-radius: 4px;
            padding: 50px 20px;
            text-align: center;
            background: #fafafa;
            transition: all 0.2s ease;
            cursor: pointer;
            margin-bottom: 25px;
        }

        .upload-area:hover {
            border-color: #7f8c8d;
            background: #f5f5f5;
        }

        .upload-area.dragover {
            border-color: #34495e;
            background: #ecf0f1;
        }

        .upload-icon {
            font-size: 3em;
            color: #7f8c8d;
            margin-bottom: 15px;
        }

        .upload-text {
            font-size: 1.1em;
            color: #2c3e50;
            margin-bottom: 8px;
            font-weight: 400;
        }

        .upload-hint {
            color: #7f8c8d;
            font-size: 0.9em;
            font-style: italic;
        }

        #fileInput {
            display: none;
        }

        .file-info {
            margin-top: 20px;
            padding: 12px 15px;
            background: #e8f5e9;
            border-left: 4px solid #4caf50;
            display: none;
            font-size: 0.95em;
        }

        .file-info.show {
            display: block;
        }

        .file-name {
            font-weight: 500;
            color: #2e7d32;
        }

        .button-group {
            display: flex;
            gap: 12px;
            justify-content: flex-start;
            margin-top: 25px;
        }

        button {
            padding: 12px 30px;
            font-size: 1em;
            border: 1px solid #bdc3c7;
            border-radius: 4px;
            cursor: pointer;
            transition: all 0.2s ease;
            font-weight: 400;
            font-family: inherit;
        }

        .btn-primary {
            background: #34495e;
            color: white;
            border-color: #34495e;
        }

        .btn-primary:hover:not(:disabled) {
            background: #2c3e50;
            border-color: #2c3e50;
        }

        .btn-primary:disabled {
            opacity: 0.5;
            cursor: not-allowed;
        }

        .btn-secondary {
            background: white;
            color: #34495e;
            border-color: #bdc3c7;
        }

        .btn-secondary:hover {
            background: #f8f9fa;
            border-color: #95a5a6;
        }

        .loading {
            display: none;
            text-align: center;
            margin-top: 30px;
            padding: 20px;
        }

        .loading.show {
            display: block;
        }

        .spinner {
            border: 3px solid #ecf0f1;
            border-top: 3px solid #34495e;
            border-radius: 50%;
            width: 40px;
            height: 40px;
            animation: spin 1s linear infinite;
            margin: 0 auto 15px;
        }

        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }

        .loading-text {
            color: #7f8c8d;
            font-size: 0.95em;
        }

        .result-container {
            margin-top: 40px;
            display: none;
        }

        .result-container.show {
            display: block;
        }

        .result-title {
            font-size: 1.3em;
            font-weight: 400;
            color: #2c3e50;
            margin-bottom: 25px;
            padding-bottom: 10px;
            border-bottom: 2px solid #ecf0f1;
        }

        .image-comparison {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 30px;
            margin-top: 25px;
        }

        .image-box {
            text-align: center;
        }

        .image-label {
            font-weight: 500;
            color: #34495e;
            margin-bottom: 15px;
            font-size: 1em;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            font-size: 0.9em;
        }

        .image-preview {
            max-width: 100%;
            border: 1px solid #e0e0e0;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        }

        .error-message {
            background: #ffebee;
            color: #c62828;
            padding: 15px;
            border-left: 4px solid #c62828;
            margin-top: 20px;
            display: none;
            font-size: 0.95em;
        }

        .error-message.show {
            display: block;
        }

        .download-btn {
            margin-top: 25px;
            text-align: left;
        }

        .info-section {
            background: #f8f9fa;
            border: 1px solid #e0e0e0;
            padding: 20px;
            margin-top: 30px;
            font-size: 0.9em;
            color: #555;
        }

        .info-section h3 {
            font-size: 1.1em;
            margin-bottom: 10px;
            color: #2c3e50;
            font-weight: 400;
        }

        .info-section ul {
            margin-left: 20px;
            margin-top: 10px;
        }

        .info-section li {
            margin-bottom: 5px;
        }

        .footer {
            background: #2c3e50;
            color: white;
            text-align: center;
            padding: 20px;
            font-size: 0.85em;
            margin-top: 40px;
        }

        @media (max-width: 768px) {
            .image-comparison {
                grid-template-columns: 1fr;
            }

            .main-content {
                padding: 25px;
            }

            .header h1 {
                font-size: 1.6em;
            }

            .button-group {
                flex-direction: column;
            }

            button {
                width: 100%;
            }
        }
    </style>
</head>
<body>
    <div class="header">
        <h1>Variational Autoencoder Denoising Interface</h1>
        <div class="subtitle">Beta-VAE Model for Image Denoising</div>
    </div>

    <div class="container">
        <div class="main-content">
            <h2 class="section-title">Image Upload and Processing</h2>
            
            <div class="upload-area" id="uploadArea">
                <div class="upload-icon">⬆</div>
                <div class="upload-text">Select or drag image file(s)</div>
                <div class="upload-hint">Supported formats: PNG, JPG, JPEG, GIF, BMP, TIFF (multiple files supported)</div>
                <input type="file" id="fileInput" accept="image/*" multiple>
            </div>

            <div class="file-info" id="fileInfo">
                <span class="file-name" id="fileName"></span>
            </div>

            <div class="button-group">
                <button class="btn-primary" id="processBtn" disabled>Process Image(s)</button>
                <button class="btn-secondary" id="clearBtn" disabled>Clear Selection</button>
            </div>

            <div class="loading" id="loading">
                <div class="spinner"></div>
                <div class="loading-text" id="loadingText">Processing image(s) through VAE model...</div>
            </div>

            <div class="error-message" id="errorMessage"></div>

            <div class="result-container" id="resultContainer">
                <h2 class="result-title">Processing Results</h2>
                <div class="image-comparison">
                    <div class="image-box">
                        <div class="image-label">Input Image</div>
                        <img id="inputImage" class="image-preview" alt="Input">
                    </div>
                    <div class="image-box">
                        <div class="image-label">Denoised Output</div>
                        <img id="outputImage" class="image-preview" alt="Output">
                    </div>
                </div>
                <div class="download-btn">
                    <button class="btn-primary" id="downloadBtn">Download Result</button>
                </div>
            </div>

            <div class="info-section">
                <h3>Model Information</h3>
                <ul>
                    <li>Model Architecture: Beta-Variational Autoencoder (Beta-VAE)</li>
                    <li>Input Format: 28×28 grayscale images</li>
                    <li>Latent Dimension: 32</li>
                    <li>Training: Denoising task on MNIST dataset</li>
                    <li>Images are automatically resized and converted to grayscale</li>
                    <li>Supports batch processing: upload multiple images to receive a ZIP file</li>
                </ul>
            </div>
        </div>
    </div>

    <div class="footer">
        <p>Research Implementation | Variational Autoencoder Denoising System</p>
    </div>

    <script>
        const uploadArea = document.getElementById('uploadArea');
        const fileInput = document.getElementById('fileInput');
        const fileInfo = document.getElementById('fileInfo');
        const fileName = document.getElementById('fileName');
        const processBtn = document.getElementById('processBtn');
        const clearBtn = document.getElementById('clearBtn');
        const loading = document.getElementById('loading');
        const errorMessage = document.getElementById('errorMessage');
        const resultContainer = document.getElementById('resultContainer');
        let inputImage = document.getElementById('inputImage');
        let outputImage = document.getElementById('outputImage');
        let downloadBtn = document.getElementById('downloadBtn');
        const loadingText = document.getElementById('loadingText');

        let selectedFiles = [];
        let outputBlob = null;
        let isZipFile = false;

        // Click to upload
        uploadArea.addEventListener('click', () => fileInput.click());

        // Drag and drop
        uploadArea.addEventListener('dragover', (e) => {
            e.preventDefault();
            uploadArea.classList.add('dragover');
        });

        uploadArea.addEventListener('dragleave', () => {
            uploadArea.classList.remove('dragover');
        });

        uploadArea.addEventListener('drop', (e) => {
            e.preventDefault();
            uploadArea.classList.remove('dragover');
            const files = Array.from(e.dataTransfer.files);
            if (files.length > 0) {
                handleFileSelect(files);
            }
        });

        fileInput.addEventListener('change', (e) => {
            if (e.target.files.length > 0) {
                handleFileSelect(Array.from(e.target.files));
            }
        });

        function handleFileSelect(files) {
            // Filter valid image files
            const imageFiles = files.filter(file => file.type.startsWith('image/'));
            
            if (imageFiles.length === 0) {
                showError('Please select valid image file(s).');
                return;
            }

            selectedFiles = imageFiles;
            
            // Update file info display
            if (imageFiles.length === 1) {
                fileName.textContent = `Selected: ${imageFiles[0].name}`;
                // Preview single image
                const reader = new FileReader();
                reader.onload = (e) => {
                    inputImage.src = e.target.result;
                };
                reader.readAsDataURL(imageFiles[0]);
            } else {
                fileName.textContent = `Selected: ${imageFiles.length} images`;
                // Clear preview for multiple images
                inputImage.src = '';
            }
            
            fileInfo.classList.add('show');
            processBtn.disabled = false;
            clearBtn.disabled = false;
            errorMessage.classList.remove('show');
            resultContainer.classList.remove('show');
        }

        processBtn.addEventListener('click', async () => {
            if (selectedFiles.length === 0) return;

            const formData = new FormData();
            selectedFiles.forEach(file => {
                formData.append('file', file);
            });

            loading.classList.add('show');
            loadingText.textContent = selectedFiles.length === 1 
                ? 'Processing image through VAE model...' 
                : `Processing ${selectedFiles.length} images through VAE model...`;
            errorMessage.classList.remove('show');
            resultContainer.classList.remove('show');
            processBtn.disabled = true;

            try {
                const response = await fetch('/upload', {
                    method: 'POST',
                    body: formData
                });

                if (!response.ok) {
                    const error = await response.json();
                    throw new Error(error.error || 'Processing failed');
                }

                outputBlob = await response.blob();
                const contentType = response.headers.get('content-type');
                
                if (contentType === 'application/zip' || selectedFiles.length > 1) {
                    // Multiple files - download zip
                    isZipFile = true;
                    const url = URL.createObjectURL(outputBlob);
                    const a = document.createElement('a');
                    a.href = url;
                    a.download = 'denoised_images.zip';
                    document.body.appendChild(a);
                    a.click();
                    document.body.removeChild(a);
                    URL.revokeObjectURL(url);
                    
                    // Show success message
                    resultContainer.classList.add('show');
                    outputImage.src = ''; // Clear image display
                    resultContainer.innerHTML = `
                        <h2 class="result-title">Processing Complete</h2>
                        <div style="text-align: center; padding: 20px;">
                            <p style="margin-bottom: 15px;">Successfully processed ${selectedFiles.length} image(s).</p>
                            <p style="color: #7f8c8d; font-size: 0.9em;">The ZIP file has been downloaded automatically.</p>
                        </div>
                    `;
                } else {
                    // Single file - show preview
                    isZipFile = false;
                    const imageUrl = URL.createObjectURL(outputBlob);
                    outputImage.src = imageUrl;
                    resultContainer.classList.add('show');
                }
            } catch (error) {
                showError(error.message);
            } finally {
                loading.classList.remove('show');
                processBtn.disabled = false;
            }
        });

        clearBtn.addEventListener('click', () => {
            selectedFiles = [];
            fileInput.value = '';
            fileInfo.classList.remove('show');
            resultContainer.classList.remove('show');
            errorMessage.classList.remove('show');
            processBtn.disabled = true;
            clearBtn.disabled = true;
            inputImage.src = '';
            outputImage.src = '';
            if (outputBlob) {
                URL.revokeObjectURL(URL.createObjectURL(outputBlob));
                outputBlob = null;
            }
            // Reset result container to original HTML
            resultContainer.innerHTML = `
                <h2 class="result-title">Processing Results</h2>
                <div class="image-comparison">
                    <div class="image-box">
                        <div class="image-label">Input Image</div>
                        <img id="inputImage" class="image-preview" alt="Input">
                    </div>
                    <div class="image-box">
                        <div class="image-label">Denoised Output</div>
                        <img id="outputImage" class="image-preview" alt="Output">
                    </div>
                </div>
                <div class="download-btn">
                    <button class="btn-primary" id="downloadBtn">Download Result</button>
                </div>
            `;
            // Re-get references after innerHTML reset
            const newInputImage = document.getElementById('inputImage');
            const newOutputImage = document.getElementById('outputImage');
            const newDownloadBtn = document.getElementById('downloadBtn');
            if (newInputImage) inputImage = newInputImage;
            if (newOutputImage) outputImage = newOutputImage;
            if (newDownloadBtn) {
                downloadBtn = newDownloadBtn;
                downloadBtn.addEventListener('click', downloadHandler);
            }
        });

        function downloadHandler() {
            if (outputBlob) {
                const url = URL.createObjectURL(outputBlob);
                const a = document.createElement('a');
                a.href = url;
                if (isZipFile) {
                    a.download = 'denoised_images.zip';
                } else {
                    a.download = 'denoised_output.png';
                }
                document.body.appendChild(a);
                a.click();
                document.body.removeChild(a);
                URL.revokeObjectURL(url);
            }
        }

        downloadBtn.addEventListener('click', downloadHandler);

        function showError(message) {
            errorMessage.textContent = `Error: ${message}`;
            errorMessage.classList.add('show');
        }
    </script>
</body>
</html>
