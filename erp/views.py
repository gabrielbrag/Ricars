from django.shortcuts import render
from django.views.generic import ListView, TemplateView
from .models import Vehicle, Brand
from django.utils.translation import gettext as _

class DataTableMixin:
    def get_data_table(self):
        # Implement this method in each ListView to generate the data for the dataTable
        raise NotImplementedError("Subclasses must implement get_data_table() method.")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        data_table = self.get_data_table()
        print(data_table)
        context['dataTable'] = data_table
        return context


class VehicleListView(DataTableMixin, ListView):
    model = Vehicle
    template_name = 'datatable.html'
    
    def get_data_table(self):
        dataTableColumns = [_("Vehicle"), _("Year"), _("Color"), _("Purchase price"), _("Sale price")]
        rows = []
        for vehicle in Vehicle.objects.all():
            vehicleValues = []
            vehicleValues.append(vehicle.vehicle_variant)
            vehicleValues.append(vehicle.model_year)
            vehicleValues.append(vehicle.color)
            vehicleValues.append(vehicle.purchase_price)
            vehicleValues.append(vehicle.sale_value_formatted)
            rowsValue = {"values":vehicleValues}
            rows.append(rowsValue)

        data_table = {
            'columns': dataTableColumns,
            'rows': rows
        }
        return data_table

class BrandListView(ListView):
    model = Brand
    template_name = 'brand_list.html'
    context_object_name = 'brands'