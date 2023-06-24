from .views_base import DataTableListView
from django.views.generic import ListView, UpdateView, CreateView
from django.core.serializers import serialize
from django.http import JsonResponse
from erp.models import Brand
from django.utils.translation import gettext as _
from django.urls import reverse_lazy

class BrandListView(DataTableListView):
    model = Brand
    columns = ['brand_name']
    insert_view_route_name = 'brand_create'
    edit_view_route_name = 'brand_edit'

class BrandBaseView():
    model = Brand
    fields = ['brand_name']
    template_name = 'forms/brand_edit.html'
    success_url = reverse_lazy('brand_list')

class BrandCreateView(BrandBaseView, CreateView):
    pass

class BrandUpdateView(BrandBaseView, UpdateView):
    pass

def brandJSON(request):
    brands = Brand.objects.all()
    serialized_data = serialize('json', brands)
    return JsonResponse(serialized_data, safe=False)  
