
const vehiclePanelMethodURL = (window.location.origin + '/vehiclesPanel');

var queryFilters = {
    "modelType": "",
    "minPrice": "",
    "maxPrice": "",
    "minMileage": "",
    "maxMileage": "",
    "years": []
}

$(document).ready(function () {
    $('#input_minPrice').focusout(function () {
        queryFilters["minPrice"] = $('#input_minPrice').val();
        mountVehiclesPanel(queryFilters);
    });

    $('#input_maxPrice').focusout(function () {
        queryFilters["maxPrice"] = $('#input_maxPrice').val();
        mountVehiclesPanel(queryFilters);
    });

    $('#input_minMileage').focusout(function () {
        queryFilters["minMileage"] = $('#input_minMileage').val();
        mountVehiclesPanel(queryFilters);
    });

    $('#input_maxMileage').focusout(function () {
        queryFilters["maxMileage"] = $('#input_maxMileage').val();
        mountVehiclesPanel(queryFilters);
    });

    let lastChecked = null

    $('input[type="radio"][name="categoryRadio"]').on('click', function () {
        var currentValue = $(this).val();
        console.log(lastChecked);
        if (currentValue === lastChecked) {
            $(this).prop('checked', false);
            lastChecked = null;
        } else {
            lastChecked = currentValue;            
        }

        setTimeout(function () {
            queryFilters["modelType"] = $('input[name="categoryRadio"]:checked').val();
            mountVehiclesPanel(queryFilters);
        }, 10);
    });

    $('input[type="checkbox"][name="checkboxYear"]').on('change', function () {
        let selectedYears = getSelectedYears();

        queryFilters["years"] = selectedYears;
        mountVehiclesPanel(queryFilters);
    });
});

function getSelectedYears() {
    var selectedYears = [];
    $('input[name="checkboxYear"]:checked').each(function() {
      selectedYears.push($(this).val());
    });
    return selectedYears;
}

function mountVehiclesPanel(parametersDict) {
    const xhr = new XMLHttpRequest();

    queryParams = "";

    for (param in parametersDict) {
        var paramValue = parametersDict[param];
        if (paramValue) {
            if (Array.isArray(paramValue)) {
                if (parametersDict[param].length > 0) {
                    queryParams += (param + "=" + paramValue.join(",") + "&");
                }
            } else {
                queryParams += (param + "=" + paramValue + "&");
            }
        }
    };

    xhr.open('GET', vehiclePanelMethodURL + "?" + queryParams);

    xhr.onload = function () {
        if (xhr.status === 200) {
            var responseData = xhr.responseText;
            $('#vehiclesPanel').html(responseData);
        }
    };
    
    xhr.send();
}