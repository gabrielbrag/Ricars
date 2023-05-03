from django.shortcuts import render
from django.views.generic import ListView, TemplateView
from .models import Vehicle, Brand

class VehicleListView(ListView):
    model = Vehicle
    template_name = 'vehicle_list.html'

class BrandListView(ListView):
    model = Brand
    template_name = 'brand_list.html'
    context_object_name = 'brands'