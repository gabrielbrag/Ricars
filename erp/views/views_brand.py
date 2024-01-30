from .views_base import BaseView, DataTableListView
from django.views.generic import UpdateView, CreateView, DeleteView
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

class BrandBaseView(BaseView):
    model = Brand
    fields = ['brand_name']
    template_name = 'erp/forms/brand_edit.html'
    success_url = reverse_lazy('brand_list')

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