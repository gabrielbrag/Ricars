from django.urls                    import path
from .views.views_brand             import BrandListView, BrandCreateView, BrandUpdateView, BrandDeleteView, brandJSON
from .views.views_color             import ColorListView, ColorCreateView, ColorUpdateView, ColorDeleteView
from .views.views_vehicle_model     import VehicleModelListView, VehicleModelCreateView, VehicleModelUpdateView, VehicleModelDeleteView, VehicleModelJSON, VehicleModelVariantJSON
from .views.views_vehicle           import VehicleListView, VehicleCreateView, VehicleUpdateView, VehicleDeleteView
from django.contrib.auth            import views as auth_views

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    path('brands/', BrandListView.as_view(), name='brand_list'),
    path('brands/<int:pk>/edit/', BrandUpdateView.as_view(), name='brand_edit'),
    path('brands/insert/', BrandCreateView.as_view(), name='brand_create'),    
    path('brands/<int:pk>/delete/', BrandDeleteView.as_view(http_method_names=['post']), name='brand_delete'),
    path('brands/JSON', brandJSON, name='brand_json'),

    path('colors/', ColorListView.as_view(), name="color_list"),
    path('colors/<int:pk>/edit/', ColorUpdateView.as_view(), name='color_edit'),
    path('colors/<int:pk>/delete/', ColorDeleteView.as_view(http_method_names=['post']), name='color_delete'),
    path('colors/insert/', ColorCreateView.as_view(), name='color_create'),    

    path('vehicle_models', VehicleModelListView.as_view(), name="vehicle_model_list"),
    path('vehicle_models/<int:pk>/edit/', VehicleModelUpdateView.as_view(), name='vehicle_model_edit'),
    path('vehicle_models/<int:pk>/delete/', VehicleModelDeleteView.as_view(http_method_names=['post']), name='vehicle_model_delete'),
    path('vehicle_models/insert/', VehicleModelCreateView.as_view(), name='vehicle_model_create'),    
    path('vehicle_model/JSON', VehicleModelJSON, name='vehicle_model_json'),

    path('vehicle_model_variant/JSON', VehicleModelVariantJSON, name='vehicle_model_variant_json'),

    path('vehicles', VehicleListView.as_view(), name="vehicle_list"),
    path('vehicles/<int:pk>/edit/', VehicleUpdateView.as_view(), name='vehicle_edit'),
    path('vehicles/insert/', VehicleCreateView.as_view(), name='vehicle_create'),
    path('vehicle_models/<int:pk>/delete/', VehicleDeleteView.as_view(http_method_names=['post']), name='vehicle_delete'),
]