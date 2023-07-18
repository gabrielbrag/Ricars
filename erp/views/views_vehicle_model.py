from .views_base import DataTableListView
from django.views.generic import ListView, TemplateView, UpdateView, CreateView, DeleteView
from django.core.serializers import serialize
from django.http import JsonResponse
from erp.models import Brand, Vehicle_model, Vehicle_model_variant
from django.utils.translation import gettext as _
from django.urls import reverse, reverse_lazy
import json

class VehicleModelListView(DataTableListView):
    model = Vehicle_model
    columns = ["brand", "model_name", "model_type"]
    insert_view_route_name = 'vehicle_model_create'
    edit_view_route_name = 'vehicle_model_edit'
    delete_view_route_name = 'vehicle_model_delete'

class VehicleModelBaseView():
    model = Vehicle_model
    fields = ['brand', 'model_name', 'model_type']
    template_name = 'erp/forms/vehicle_model_edit.html'
    success_url = reverse_lazy('vehicle_model_list')

class VehicleModelCreateView(VehicleModelBaseView, CreateView):
    def form_valid(self, form):
        # Save the main model
        response = super().form_valid(form)

        variant_data = json.loads(self.request.POST.get('variant_data'))
        vehicle_model = self.object  # Access the created VehicleModel object

        # Create and save new variants
        for variant_name in variant_data:
            variant = Vehicle_model_variant(vehicle_model=vehicle_model, variant_name=variant_name)
            variant.save()

        return response

        return response

class VehicleModelUpdateView(VehicleModelBaseView, UpdateView):
    removeVariantHTML = '<button class="removeButton"><i class="fas fa-trash"></i></button>'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        variantsList = []
        variantsQuerySet = Vehicle_model_variant.objects.filter(vehicle_model=self.kwargs.get('pk'))
        for variant in variantsQuerySet:
            dataTableDict = {}
            dataTableDict["variant"]    = variant.variant_name
            dataTableDict["remove"]     = self.removeVariantHTML
            variantsList.append(dataTableDict)

        context["removeVariantHTML"] = self.removeVariantHTML
        context["variants_JSON"] = str(json.dumps(variantsList)).replace("\\", "\\\\")
        return context

    def form_valid(self, form):
        # Save the main model
        response = super().form_valid(form)

        HandleVariants(self)

        return response

class VehicleModelDeleteView(VehicleModelBaseView, DeleteView):
    def post(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)

def HandleVariants(self):
    variant_data = json.loads(self.request.POST.get('variant_data'))
    vehicle_model = self.get_object()  # Retrieve the current VehicleModel object

    # Delete existing variants
    vehicle_model.variants.all().delete()

    # Create and save new variants
    for variant_name in variant_data:
        variant = Vehicle_model_variant(vehicle_model=vehicle_model, variant_name=variant_name)
        variant.save()

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