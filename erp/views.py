from django.shortcuts import render
from django.views.generic import ListView, TemplateView, UpdateView, CreateView
from django.core.serializers import serialize
from django.http import JsonResponse
from .models import Vehicle, Brand, Vehicle_model, Vehicle_model_variant
from django.utils.translation import gettext as _
from django.utils.safestring import mark_safe
from django.urls import reverse, reverse_lazy

class DataTableMixin:
    def get_data_table(self):
        # Implement this method in each ListView to generate the data for the dataTable
        raise NotImplementedError("Subclasses must implement get_data_table() method.")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        data_table = self.get_data_table()
        context['dataTable'] = data_table
        return context

    def mountEditIcon(self, viewURL):
        return mark_safe('<a href="' + viewURL + '"><i class="fas fa-lg fa-edit"></i></a>')


class VehicleListView(DataTableMixin, TemplateView):
    template_name = 'datatable.html'

    def get_data_table(self):
        dataTableColumns = [_("Vehicle"), _("Year"), _("Color"), _("Purchase price"), _("Sale price")]
        rows = []
        for vehicle in Vehicle.objects.all():
            vehicleValues = []
            vehicleValues.append(vehicle.vehicle_variant)
            vehicleValues.append(vehicle.model_year)
            vehicleValues.append(vehicle.color)
            vehicleValues.append(vehicle.purchase_price_formatted)
            vehicleValues.append(vehicle.sale_value_formatted)
            vehicleValues.append(self.mountEditIcon(reverse('vehicle_edit', kwargs={'pk': vehicle.pk})))
            rowsValue = {"values":vehicleValues}
            rows.append(rowsValue)

        data_table = {
            'columns': dataTableColumns,
            'rows': rows,
            'insertViewURL':reverse_lazy('vehicle_create')
        }
        return data_table

class VehicleUpdateView(UpdateView):
    model = Vehicle
    fields = ['vehicle_variant', 'model_year', 'color', 'purchase_price', 'sale_value']
    template_name = 'vehicle_edit.html'
    success_url = reverse_lazy('vehicle_list')

class VehicleCreateView(CreateView):
    model = Vehicle
    fields = ['vehicle_variant', 'model_year', 'color', 'purchase_price', 'sale_value']
    template_name = 'vehicle_edit.html'
    success_url = reverse_lazy('vehicle_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['brands'] = Brand.objects.all()
        return context

class BrandListView(ListView):
    model = Brand
    template_name = 'brand_list.html'
    context_object_name = 'brands'

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