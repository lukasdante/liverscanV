const dropArea = document.querySelector(".upload-image-main");
const dropText = document.querySelector(".upload-image-text");
const input = document.querySelector(".input-files");
const dateField = document.querySelector(".date-now");
const noSelectedBanner = document.querySelector(".assigned-reports-report-details");
const selectedBanner = document.querySelector(".doctor-results-main");
const patientIDDiv = document.querySelector(".patient-id-value");
const statusDiv = document.querySelector(".status-value");
const initialDiagnosisDiv = document.querySelector(".diagnosis-value");
const diagnosisDateDiv = document.querySelector(".date-value");
const areaDiv = document.querySelector(".area-value");
const today = new Date();
const year = today.getFullYear();
const month = String(today.getMonth() + 1).padStart(2, '0'); // Months are 0-indexed
const day = String(today.getDate()).padStart(2, '0');
const formattedDate = `${year}-${month}-${day}`;
dateField.value = formattedDate;

async function fetchData(link) {
    try {
        const response = await fetch(`/api/${link}/`);
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        const data = await response.json();
        return data;
    } catch (error) {
        console.error('Error fetching data:', error);
    }
}

async function fetchDiagnosisDetails(diagnosisId) {
    let diagnosis_data = await fetchData(`diagnoses/${diagnosisId}`);
    
    if (diagnosis_data) {
        noSelectedBanner.style.display = "none";
        selectedBanner.style.display = "block";
        
        patientIDDiv.textContent = diagnosis_data.patient_id

        switch(diagnosis_data.status) {
            case 1:
                statusDiv.textContent = `Waiting for predictions`
            case 2:
                statusDiv.textContent = `Waiting for validation`
            case 3:
                statusDiv.textContent = `Finished`
            default:
                statusDiv.textContent = `Waiting for predictions`

        }
        
        
        
        initialDiagnosisDiv.textContent = diagnosis_data.initial_diagnosis
        diagnosisDateDiv.textContent = diagnosis_data.diagnosis_date

        if (diagnosis_data.initial_diagnosis == 'normal' || diagnosis_data.initial_diagnosis == null) {
            areaDiv.textContent = `0 cm\u00B2`;
        } else {
            areaDiv.textContent = `${diagnosis_data.area} cm\u00B2`;
        }
        
        console.log(diagnosis_data);

    } else {
        console.error('No data found for the given diagnosis ID.');
        noSelectedBanner.style.display = "block"; // Show no selected banner if no data
        selectedBanner.style.display = "none"; // Hide the selected banner
    }
}



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

// Handle form submission
form.addEventListener('submit', function (event) {
    event.preventDefault(); // Prevent the default form submission

    // Create a FormData object
    let formData = new FormData();

    // Append the description (or other form fields)
    formData.append('description', descriptionInput.value);

    // Append images (files) to the FormData object
    files.forEach((file, index) => {
        formData.append(`image${index + 1}`, file);
    });

    // Send the form data to the backend via fetch API
    fetch('/your-django-endpoint/', {
        method: 'POST',
        body: formData,
        headers: {
            // You don't need to add the content-type header for FormData, 
            // the browser automatically sets the correct content-type including boundary.
            'X-CSRFToken': getCookie('csrftoken') // Add CSRF token for Django
        }
    })
    .then(response => response.json())
    .then(data => {
        console.log("Success:", data); // Handle success (for example, displaying prediction results)
    })
    .catch((error) => {
        console.error("Error:", error); // Handle errors
    });
});

// CSRF Token helper function for Django (use this if your Django app uses CSRF protection)
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}