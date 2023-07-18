from .views_base import DataTableListView
from django.views.generic import TemplateView, UpdateView, CreateView, DeleteView
from erp.models import Color
from django.utils.translation import gettext as _
from django.urls import reverse, reverse_lazy

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

class ColorCreateView(ColorBaseView, CreateView):
    pass

class ColorUpdateView(ColorBaseView, UpdateView):
    pass

class ColorDeleteView(ColorBaseView, DeleteView):
    def post(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)