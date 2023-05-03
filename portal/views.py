from django.shortcuts import render
from erp.models import Vehicle

def home(request):
    minimum_price = request.GET.get('minPrice')
    maximum_price = request.GET.get('maxPrice')
    
    filter_args = {}

    if minimum_price is not None:
        filter_args['sale_value__gte'] = minimum_price

    if maximum_price is not None:
        filter_args['sale_value__lte'] = maximum_price    
        
    vehicles = Vehicle.objects.filter(**filter_args)
    
    possible_vehicle_years  = Vehicle.objects.values_list('year', flat=True).distinct().order_by('year')
    
    return render(request, 'stock.html', {"vehicles":vehicles, "possible_vehicle_years":possible_vehicle_years})

def vehiclesPanel(request):
    minimum_price = request.GET.get('minPrice')
    maximum_price = request.GET.get('maxPrice')
    
    filter_args = {}

    if minimum_price is not None:
        filter_args['sale_value__gte'] = minimum_price

    if maximum_price is not None:
        filter_args['sale_value__lte'] = maximum_price    
        
    vehicles = Vehicle.objects.filter(**filter_args)
    
    return render(request, 'vehiclesPanel.html', {"vehicles":vehicles})