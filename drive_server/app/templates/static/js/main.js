let traceId;

function start() {
    const fileUploadForm = document.getElementById('file-upload-form');
    const fileUploadButton = document.getElementById('file-upload-button');

    fileUploadForm.addEventListener('change', onFileUpload);
    fileUploadButton.addEventListener('click', () => {
        fileUploadForm.click();
    });
    showLogin(() => {
        coreConnect({});
        listFiles();
    });

}

start();
