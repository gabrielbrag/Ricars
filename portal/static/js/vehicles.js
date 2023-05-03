 
var queryFilters = {
    "category":"",
    "minPrice":"",
    "maxPrice":"",
    "minMileage":"",
    "maxMileage":"",
    "years":[]
}

function mountVehiclesPanel(url, parametersDict){
    // Create new XMLHttpRequest object
    const xhr = new XMLHttpRequest();

    queryParams = "";

    for (param in parametersDict) {
        queryParams += (param + "=" + parametersDict[param]);
    };
    
    console.log(url + "?" + queryParams);
    // Set the HTTP method to GET and the URL with query parameters
    xhr.open('GET', url + "?" + queryParams);

    // Define what happens on a successful response
    xhr.onload = function() {
    // If the response was successful (status code 200)
    if (xhr.status === 200) {
        // Get the response data
        var responseData = xhr.responseText;
        // Find the element to update
        $('#vehiclesPanel').html(responseData);
    }
    };

    // Send the request
    xhr.send();
}