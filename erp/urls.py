from django.urls import path
from .views import BrandListView
from .views import VehicleListView
from .views import VehicleUpdateView
from .views import VehicleCreateView
from .views import VehicleModelJSON
from .views import VehicleModelVariantJSON

urlpatterns = [
    path('brands/', BrandListView.as_view(), name='brand_list'),

    path('vehicle_model/JSON', VehicleModelJSON, name='vehicle_model_json'),

    path('vehicle_model_variant/JSON', VehicleModelVariantJSON, name='vehicle_model_variant_json'),

    path('vehicles', VehicleListView.as_view(), name="vehicle_list"),
    path('vehicles/<int:pk>/edit/', VehicleUpdateView.as_view(), name='vehicle_edit'),
    path('vehicles/insert/', VehicleCreateView.as_view(), name='vehicle_create')
]