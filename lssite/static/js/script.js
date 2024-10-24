const dropArea = document.querySelector(".upload-image-main");
const dropText = document.querySelector(".upload-image-text");
const input = document.querySelector(".input-files");

let files = [];

dropArea.onclick = () => {
    input.click();
};

input.addEventListener("change", function() {
    file = Array.from(this.files);
    showImages();
});

dropArea.addEventListener("dragover", (event)=>{
    event.preventDefault();
    dropArea.classList.add("active-image");
    dropText.textContent = "Release to Upload files";
});

dropArea.addEventListener("dragleave", ()=>{
    dropArea.classList.remove("active-image");
    dropText.textContent = "Drag and drop images or click to upload";
});


dropArea.addEventListener("drop", (event)=>{
    event.preventDefault();
    dropArea.classList.remove("active-image");
    files = Array.from(event.dataTransfer.files);
    showImages();

});

function showImages() {
    let validTypes = ["image/jpeg", "image/jpg", "image/png"];
    dropArea.innerHTML = "";

    if (files.length > 3) {
        alert("You can only upload to 3 images.");
        return;
    }

    for (let file of files) {
        if (validTypes.includes(file.type)) {
            let fileReader = new FileReader();
            fileReader.onload = () => {
                let fileURL = fileReader.result;
                console.log(fileURL);
                let imgTag = `<img src="${fileURL}" alt="">`;
                dropArea.innerHTML += imgTag;
            }
            fileReader.readAsDataURL(file);
        } else {
            alert("It must be an image file.");
            dropArea.classList.remove("active-image");
            dropText.textContent = "Drag and drop images or click to upload";
            return
        }
    }
}