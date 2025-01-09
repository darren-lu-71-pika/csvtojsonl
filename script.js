document.getElementById('upload-form').addEventListener('submit', function (event) {
  event.preventDefault();

  const fileInput = document.getElementById('csv-file');
  if (fileInput.files.length === 0) {
    alert('Please select a CSV file to upload.');
    return;
  }

  const formData = new FormData();
  formData.append('file', fileInput.files[0]);

  fetch('/convert', {
    method: 'POST',
    body: formData,
  })
    .then(response => response.json())
    .then(data => {
      const resultDiv = document.getElementById('result');
      if (data.success) {
        resultDiv.innerHTML = `<p>File converted successfully! <a href="${data.download_url}" target="_blank">Download JSONL</a></p>`;
      } else {
        resultDiv.textContent = 'Error converting file: ' + data.error;
      }
    })
    .catch(error => {
      console.error('Error:', error);
      document.getElementById('result').textContent = 'An unexpected error occurred.';
    });
});
