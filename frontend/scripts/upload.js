function uploadFile() {
    let fileInput = document.getElementById("fileInput");
    let file = fileInput.files[0];

    if (!file) {
        document.getElementById("uploadStatus").innerText = "❌ No file selected!";
        return;
    }

    // Check allowed file types
    let allowedExtensions = [".csv", ".xls", ".xlsx"];
    let fileExt = file.name.substring(file.name.lastIndexOf(".")).toLowerCase();
    
    if (!allowedExtensions.includes(fileExt)) {
        document.getElementById("uploadStatus").innerText = "❌ Invalid file type! Please upload a CSV or Excel file.";
        return;
    }

    let formData = new FormData();
    formData.append("file", file);

    document.getElementById("uploadStatus").innerText = "⏳ Uploading file...";

    fetch("http://127.0.0.1:5000/upload", {
        method: "POST",
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            document.getElementById("uploadStatus").innerText = `❌ Error: ${data.error}`;
        } else {
            document.getElementById("uploadStatus").innerText = `✅ ${data.message}`;
        }
    })
    .catch(error => {
        document.getElementById("uploadStatus").innerText = "❌ Upload failed! Server error.";
        console.error("Upload Error:", error);
    });
}
