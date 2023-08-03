from .views_base import DataTableListView
from django.views.generic import ListView, UpdateView, CreateView, DeleteView
from django.core.serializers import serialize
from django.http import JsonResponse
from erp.models import Brand
from django.utils.translation import gettext as _
from django.urls import reverse_lazy
from django.forms.widgets import CheckboxInput

class BrandListView(DataTableListView):
    model = Brand
    columns = ['brand_name']
    insert_view_route_name = 'brand_create'
    edit_view_route_name = 'brand_edit'
    delete_view_route_name = 'brand_delete'

class BrandBaseView():
    model = Brand
    fields = ['brand_name']
    template_name = 'erp/forms/brand_edit.html'
    success_url = reverse_lazy('brand_list')

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

class BrandCreateView(BrandBaseView, CreateView):
    pass

class BrandUpdateView(BrandBaseView, UpdateView):
    pass

class BrandDeleteView(BrandBaseView, DeleteView):
    def post(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)

def brandJSON(request):
    brands_data = get_model_json_response(Brand)
    print(brands_data)
    return JsonResponse(brands_data, safe=False)