from django.shortcuts import render
from erp.models import Vehicle, Vehicle_image
from companies.models import Company, Shop

def home(request):        
    vehicles = Vehicle.objects.all()
    
    company = Company.objects.first()
    shop    = Company.objects.first()
    
    possible_vehicle_years  = Vehicle.objects.values_list('manufacture_year', flat=True).distinct().order_by('manufacture_year')
    
    return render(request, 'stock.html', {"vehicles":vehicles, 
                                            "possible_vehicle_years":possible_vehicle_years,
                                            "company":company,
                                            "shop":shop})

def vehiclesPanel(request):
    url_to_model = {
        'minPrice': 'sale_value__gte',
        'maxPrice': 'sale_value__lte',
        'minMileage': 'mileage__gte',
        'maxMileage': 'mileage__lte',
        'modelType': 'vehicle_variant__vehicle_model__model_type',
        'years': 'year__in'
    }
    
    filter_args = {}
    for url_param, model_field in url_to_model.items():
        value = request.GET.get(url_param)
        if value is not None:
            if url_param == 'years':
                year_list = value.split(',')
                filter_args['year__in'] = year_list
            else:
                filter_args[model_field] = value
        
    vehicles = Vehicle.objects.filter(**filter_args)
    
    return render(request, 'vehiclesPanel.html', {"vehicles":vehicles})

def vehicleView(request):
    vehicle = Vehicle.objects.get(id=request.GET.get('id'))
    vehicle_images = Vehicle_image.objects.filter(vehicle=vehicle).order_by("index")
    return render(request, 'vehicleView.html', {'vehicle':vehicle, 'vehicle_images':vehicle_images})

def aboutView(request):
    return render(request, 'about.html')