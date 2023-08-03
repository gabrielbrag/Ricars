from .views_base import DataTableListView
from django.views.generic import TemplateView, UpdateView, CreateView, DeleteView
from erp.models import Vehicle_cost_type
from django.utils.translation import gettext as _
from django.urls import reverse, reverse_lazy
from django.forms.widgets import CheckboxInput

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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        form = self.get_form()

        fields_manually_created = ['vehicle_variant', 'salesman_observation']

        for field_name, field in form.fields.items():
            if isinstance(field.widget, CheckboxInput):
                field.widget.attrs['class'] = 'form-check'               
            else:
                field.widget.attrs['class'] = 'form-control'

        automatic_fields  = [field for field in form if field.name not in fields_manually_created]
        context['automatic_fields'] = automatic_fields

        return context

class VehicleCostTypeCreateView(VehicleCostTypeBaseView, CreateView):
    pass

class VehicleCostTypeUpdateView(VehicleCostTypeBaseView, UpdateView):
    pass

class VehicleCostTypeDeleteView(VehicleCostTypeBaseView, DeleteView):
    def post(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)