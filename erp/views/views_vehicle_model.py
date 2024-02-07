from .views_base import BaseView, DataTableListView
from django.views.generic import ListView, TemplateView, UpdateView, CreateView, DeleteView
from django.core.serializers import serialize
from django.http import JsonResponse
from erp.models import Brand, Vehicle_model
from django.utils.translation import gettext as _
from django.urls import reverse, reverse_lazy
from django.forms.widgets import CheckboxInput
import json

class VehicleModelListView(DataTableListView):
    model = Vehicle_model
    columns = ["brand", "model_name", "model_type"]
    insert_view_route_name = 'vehicle_model_create'
    edit_view_route_name = 'vehicle_model_edit'
    delete_view_route_name = 'vehicle_model_delete'
    loaded_instances = None

    def get(self, request, *args, **kwargs):
        brand_id = request.GET.get('brand')
   
        if (brand_id != None):
            self.loaded_instances = Vehicle_model.objects.filter(brand=brand_id)

        return super().get(self, request, *args, **kwargs)

class VehicleModelBaseView(BaseView):
    model = Vehicle_model
    fields = ['brand', 'model_name', 'model_type']
    template_name = 'erp/forms/vehicle_model_edit.html'
    success_url = reverse_lazy('vehicle_model_list')

class VehicleModelCreateView(VehicleModelBaseView, CreateView):
    def form_valid(self, form):
        # Save the main model
        response = super().form_valid(form)

        vehicle_model = self.object  # Access the created VehicleModel object

        return response

class VehicleModelUpdateView(VehicleModelBaseView, UpdateView):
    def form_valid(self, form):
        # Save the main model
        response = super().form_valid(form)

        return response

class VehicleModelDeleteView(VehicleModelBaseView, DeleteView):
    def post(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)