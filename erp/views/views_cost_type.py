from .views_base import DataTableListView
from django.views.generic import TemplateView, UpdateView, CreateView, DeleteView
from erp.models import Vehicle_cost_type
from django.utils.translation import gettext as _
from django.urls import reverse, reverse_lazy

class VehicleCostTypeListView(DataTableListView):
    model = Vehicle_cost_type
    columns = ['cost_type_name']
    insert_view_route_name = 'vehicle_cost_type_create'
    edit_view_route_name = 'vehicle_cost_type_edit'
    delete_view_route_name = 'vehicle_cost_type__delete'

class VehicleCostTypeBaseView():
    model = Vehicle_cost_type
    fields = ['cost_type_name']
    template_name = 'erp/forms/vehicle_cost_type_edit.html'
    success_url = reverse_lazy('vehicle_cost_type_list')

class VehicleCostTypeCreateView(VehicleCostTypeBaseView, CreateView):
    pass

class VehicleCostTypeUpdateView(VehicleCostTypeBaseView, UpdateView):
    pass

class VehicleCostTypeDeleteView(VehicleCostTypeBaseView, DeleteView):
    def post(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)