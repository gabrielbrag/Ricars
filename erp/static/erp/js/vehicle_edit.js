const endpoints = {"brandURL":"", "modelURL":""};

function setUpEndpoints(brandURL, modelURL, vehicle_listURL){
  endpoints.brandURL          = brandURL;
  endpoints.modelURL          = modelURL;
  endpoints.vehicle_listURL   = vehicle_listURL;
}

function loadOptions(url, selectId, defaultValue) {
  fetch(url)
    .then(response => response.json())
    .then(options => {
      let select = document.getElementById(selectId);
      let optionsHTML = "<option value=''>---------</option>";
      options.forEach(option => {
        optionsHTML += "<option value='" + option.id + "'>" + option.contextual_title + "</option>";
      });
      select.innerHTML = optionsHTML;

      if (defaultValue) {
        select.value = defaultValue;
      }
    })
    .catch(error => {
      console.error("Error fetching options:", error);
    });
}

function loadBrand(defaultBrand, modelId) {
  console.log("Valores " + defaultBrand + " modelId")
  loadOptions(endpoints.brandURL, "id_brand", defaultBrand);
  if (defaultBrand) {
    loadModel(defaultBrand, modelId);
  }
}

function loadModel(brandId, defaultModel) {
  const modelSelect = document.getElementById("id_model");

  if (brandId) {
    modelSelect.disabled = false;

    const url = endpoints.modelURL + "?brand=" + brandId;
    loadOptions(url, "id_model", defaultModel);
  } else {
    modelSelect.disabled = true;
    modelSelect.value = "";
  }
}


function handleFileSelect(event) {
  const files = event.target.files;
  const thumbnailContainer = document.getElementById('thumbnail-container');

  for (let i = 0; i < files.length; i++) {
      const file = files[i];
      const reader = new FileReader();

      reader.onload = function (e) {
          const thumbnail = document.createElement('div');
          thumbnail.className = 'thumbnail';
          thumbnail.innerHTML = `
              <img src="${e.target.result}" alt="Thumbnail">
              <span class="delete-button" data-file="${file.name}">
                  <i class="fas fa-trash"></i>
              </span>
          `;
          thumbnailContainer.appendChild(thumbnail);

          const deleteButton = thumbnail.querySelector('.delete-button');
          deleteButton.addEventListener('click', function () {
              handleDeleteImage(0, thumbnail, file.name);
          });
      };

      reader.readAsDataURL(file);
      insertedFiles.push(file);
  }
}

function handleDeleteImage(file_id, thumbnail, fileName) {
  if (file_id){
    for (let i = 0; i < existingFilesIDs.length; i++){
      if (file_id == existingFilesIDs[i]){
        existingFilesIDs.splice(i, 1);
      };
    };
  }else{
    for (let i = 0; i < insertedFiles.length; i++){
      if (fileName == insertedFiles[i].name){
        insertedFiles.splice(i, 1);
      };
    };
  };

  const thumbnailContainer = document.getElementById('thumbnail-container');
  thumbnailContainer.removeChild(thumbnail);
}

function submitWithFiles(form){
  convertTableToJSON();

  const formData = new FormData(form);
  const xhr = new XMLHttpRequest();
 
  insertedFiles.forEach((file, index) => {
    formData.append('inserted_files', file, 'file_' + index);
  });

  var existingIDsString = existingFilesIDs.join(',');
  formData.append('existing_files_ids', existingIDsString);
 
  xhr.onreadystatechange = function () {
    if (xhr.readyState === XMLHttpRequest.DONE) {
      if (xhr.status === 200) {
        // Handle success, e.g., show a success message
        window.location = endpoints.vehicle_listURL;
      } else {
        // Handle error, e.g., show an error message
        alert("Form submission failed. " + xhr.response);
      }
    }
  };

  xhr.open(form.method, form.action);
  xhr.send(formData);
}