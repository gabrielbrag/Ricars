from django.shortcuts import render
from django.views.generic import ListView, TemplateView, UpdateView, CreateView
from django.core.serializers import serialize
from django.http import JsonResponse
from erp.models import Vehicle, Brand, Color, Vehicle_model, Vehicle_model_variant
from django.utils.translation import gettext as _
from django.utils.safestring import mark_safe
from django.urls import reverse, reverse_lazy
from django.forms.models import model_to_dict
from django.db import models
import json

class DataTableMixin:
    def get_data_table(self):
        # Implement this method in each ListView to generate the data for the dataTable
        raise NotImplementedError("Subclasses must implement get_data_table() method.")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        data_table = self.get_data_table()
        context['dataTable'] = data_table
        return context

    def mountEditIcon(self, viewURL):
        return mark_safe('<a href="' + viewURL + '"><i class="fas fa-lg fa-edit actionButton"></i></a>')

    def mountDeleteIcon(self, deleteURL):
        return mark_safe('<span class="clickableAwesomeFont"><i class="fas fa-lg fa-trash actionButton" onClick="callDelete(\'' + deleteURL + '''\')"></i>
                        <style>
                            .clickableAwesomeFont {
                                cursor: pointer;
                                color:#007bff;
                            }
                        </style>'''
        )

class DataTableListView(DataTableMixin, TemplateView):
    template_name = 'erp/default_list.html'
    model = None
    columns = []
    insert_view_route_name = None
    edit_view_route_name = None
    delete_view_route_name = None
    json = False
    loaded_instances = None

    def get_data_table(self):
        rows = []
        columns_with_verbose_name = []

        for column in self.columns:
            field = self.model._meta.get_field(column)
            verbose_name = field.verbose_name
            columns_with_verbose_name.append(verbose_name)

        for item in self.model.objects.all():
            item_values = []
            for column in self.columns:
                item_values.append(getattr(item, column))
                
            if self.edit_view_route_name != None:
                item_values.append(self.mountEditIcon(reverse(self.edit_view_route_name, kwargs={'pk': item.pk})))
            
            if self.delete_view_route_name != None:
                item_values.append(self.mountDeleteIcon(reverse(self.delete_view_route_name, kwargs={'pk': item.pk})))
            
            rows_value = {"values": item_values}
            rows.append(rows_value)

        data_table = {
            'columns': columns_with_verbose_name,
            'rows': rows,
            'insertViewURL': reverse(self.insert_view_route_name) if self.insert_view_route_name else None,
            'editViewURL': self.edit_view_route_name,
            'deleteViewURL': self.delete_view_route_name
        }
        return data_table
    
    def get_json_list(self):
        if self.loaded_instances == None:
            self.loaded_instances = self.model.objects.all()

        serialized_data = self.serialize_instances()

        return JsonResponse(serialized_data, safe=False)

    def serialize_instances(self):
        serialized_data = []

        for instance in self.loaded_instances:
            data = model_to_dict(instance)
            if hasattr(instance, 'contextual_title'):
                data['contextual_title'] = instance.contextual_title
            serialized_data.append(data)

        return serialized_data

    def get(self, request, *args, **kwargs):
        if self.json:
            return self.get_json_list()
        return super().get(request, *args, **kwargs)