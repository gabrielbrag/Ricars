const endpoints = {"brandURL":"", "modelURL":"","variantURL":""};

function setUpEndpoints(brandURL, modelURL, variantURL, vehicle_listURL){
  endpoints.brandURL          = brandURL;
  endpoints.modelURL          = modelURL;
  endpoints.variantURL        = variantURL;
  endpoints.vehicle_listURL   = vehicle_listURL;
}

function loadOptions(url, selectId, defaultValue) {
  fetch(url)
    .then(response => response.json())
    .then(options => {
      console.log(options);
      console.log(Array.isArray(options));
      let select = document.getElementById(selectId);
      let optionsHTML = "<option value=''>---------</option>";
      options.forEach(option => {
        console.log(option);
        optionsHTML += "<option value='" + option.id + "'>" + option.contextual_title + "</option>";
      });
      select.innerHTML = optionsHTML;

      if (defaultValue) {
        select.value = defaultValue;
      }
    })
    .catch(error => {
      console.log(response);
      console.error("Error fetching options:", error);
    });
}

function loadBrand(defaultBrand, modelId, variantId) {
  loadOptions(endpoints.brandURL, "id_brand", defaultBrand);
  if (defaultBrand) {
    loadModel(defaultBrand, modelId, variantId);
  }
}

function loadModel(brandId, defaultModel, variantId) {
  const modelSelect = document.getElementById("id_model");
  const variantSelect = document.getElementById("id_variant");

  if (brandId) {
    modelSelect.disabled = false;
    variantSelect.disabled = true;
    variantSelect.value = "";

    const url = endpoints.modelURL + "?brand=" + brandId;
    loadOptions(url, "id_model", defaultModel);

    if (defaultModel) {
      loadVariant(defaultModel, variantId);
    }
  } else {
    modelSelect.disabled = true;
    variantSelect.disabled = true;
    modelSelect.value = "";
    variantSelect.value = "";
  }
}

function loadVariant(modelId, defaultVariant) {
  const variantSelect = document.getElementById("id_variant");

  if (modelId) {
    variantSelect.disabled = false;

    const url = endpoints.variantURL + "?vehicle_model=" + modelId;
    loadOptions(url, "id_variant", defaultVariant);
  } else {
    variantSelect.disabled = true;
    variantSelect.value = "";
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