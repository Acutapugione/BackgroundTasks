async function sendFile(filePath) {
  const formData = new FormData();
  formData.append('file', document.getElementById('fileInput').files[0]);

  const response = await fetch('http://localhost:8000/uploadfile_with_progress/', {
    method: 'POST',
    
    body: formData
  }).then(response => {
      console.log(response)
      const reader = response.body?.getReader();
  
      const intervalId = setInterval(async () => {
        const { done, value } = await reader.read();
        if (done) {
          clearInterval(intervalId);
          console.log('File upload complete!');
        } else {
          const textDecoder = new TextDecoder('utf-8');
          const chunk = textDecoder.decode(value);
          if (chunk.includes('100% complete')) {
            clearInterval(intervalId);
            console.log('File processing complete!');
          }
        }
      }, 1000); // Check every 1 second
    
  })
}
