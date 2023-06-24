from .views_base import DataTableMixin
from django.views.generic import ListView, TemplateView, UpdateView, CreateView
from django.core.serializers import serialize
from django.http import JsonResponse
from erp.models import Vehicle, Brand, Vehicle_model, Vehicle_model_variant
from django.utils.translation import gettext as _
from django.urls import reverse, reverse_lazy

class VehicleListView(DataTableMixin, TemplateView):
    template_name = 'default_list.html'

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

class VehicleBaseView:
    model = Vehicle
    fields = ['vehicle_variant', 'model_year', 'color', 'purchase_price', 'sale_value']
    template_name = 'vehicle_edit.html'
    success_url = reverse_lazy('vehicle_list')

class VehicleCreateView(VehicleBaseView, CreateView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['brands'] = Brand.objects.all()
        return context

class VehicleUpdateView(VehicleBaseView, UpdateView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        vehicle = self.get_object()  # Get the current vehicle object
        vehicle_brand = vehicle.vehicle_variant.vehicle_model.brand  # Access the brand through the relationships
        context['vehicle_brand'] = vehicle_brand  # Pass the brand to the template context
        return context
