from .views_base import DataTableListView
from django.views.generic import ListView, TemplateView, UpdateView, CreateView
from django.core.serializers import serialize
from django.http import JsonResponse
from erp.models import Brand, Vehicle_model, Vehicle_model_variant
from django.utils.translation import gettext as _
from django.urls import reverse, reverse_lazy

class VehicleModelListView(DataTableListView):
    model = Vehicle_model
    columns = ["brand", "model_name", "model_type"]
    insert_view_route_name = 'vehicle_model_create'
    edit_view_route_name = 'vehicle_model_edit'

class VehicleModelBaseView():
    model = Vehicle_model
    fields = ['brand', 'model_name', 'model_type']
    template_name = 'forms/vehicle_model_edit.html'
    success_url = reverse_lazy('vehicle_model_list')

class VehicleModelCreateView(VehicleModelBaseView, CreateView):
    pass

class VehicleModelUpdateView(VehicleModelBaseView, UpdateView):
    pass

def VehicleModelJSON(request):
    brand_id = request.GET.get('brand')
   
    if (brand_id != None):
        vehicle_models = Vehicle_model.objects.filter(brand=brand_id)
    else:
        vehicle_models = Vehicle_model.objects.all()

    serialized_data = serialize('json', vehicle_models)
    return JsonResponse(serialized_data, safe=False)

def VehicleModelVariantJSON(request):
    model_id = request.GET.get('vehicle_model')
   
    if (model_id != None):
        vehicle_variants = Vehicle_model_variant.objects.filter(vehicle_model=model_id)
    else:
        vehicle_variants = Vehicle_model_variant.objects.all()

    serialized_data = serialize('json', vehicle_variants)
    return JsonResponse(serialized_data, safe=False)