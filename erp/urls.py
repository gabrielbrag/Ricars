from django.urls import path
from .views import BrandListView, VehicleListView

urlpatterns = [
    path('brands/', BrandListView.as_view(), name='brand_list'),
    path('vehicles', VehicleListView.as_view(), name="vehicle_view")
]