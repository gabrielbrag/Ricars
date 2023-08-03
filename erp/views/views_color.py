from .views_base import DataTableListView
from django.views.generic import TemplateView, UpdateView, CreateView, DeleteView
from erp.models import Color
from django.utils.translation import gettext as _
from django.urls import reverse, reverse_lazy
from django.forms.widgets import CheckboxInput

class ColorListView(DataTableListView):
    model = Color
    columns = ['color_name']
    insert_view_route_name = 'color_create'
    edit_view_route_name = 'color_edit'
    delete_view_route_name = 'color_delete'

class ColorBaseView():
    model = Color
    fields = ['color_name']
    template_name = 'erp/forms/color_edit.html'
    success_url = reverse_lazy('color_list')

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

class ColorCreateView(ColorBaseView, CreateView):
    pass

class ColorUpdateView(ColorBaseView, UpdateView):
    pass

class ColorDeleteView(ColorBaseView, DeleteView):
    def post(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)