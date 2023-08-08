from django.urls                    import path
from .views.views_brand             import BrandListView, BrandCreateView, BrandUpdateView, BrandDeleteView, brandJSON
from .views.views_color             import ColorListView, ColorCreateView, ColorUpdateView, ColorDeleteView
from .views.views_vehicle_model     import VehicleModelListView, VehicleModelCreateView, VehicleModelUpdateView, VehicleModelDeleteView, VehicleModelVariantJSON
from .views.views_cost_type         import VehicleCostTypeListView, VehicleCostTypeCreateView, VehicleCostTypeUpdateView,VehicleCostTypeDeleteView
from .views.views_vehicle           import VehicleListView, VehicleCreateView, VehicleUpdateView, VehicleDeleteView
from .views.views_auth              import logout_view, CustomLoginView

urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', logout_view, name='logout'),

    path('brands/', BrandListView.as_view(), name='brand_list'),
    path('brands/JSON', BrandListView.as_view(json=True), name='brand_json'),
    path('brands/<int:pk>/edit/', BrandUpdateView.as_view(), name='brand_edit'),
    path('brands/insert/', BrandCreateView.as_view(), name='brand_create'),    
    path('brands/<int:pk>/delete/', BrandDeleteView.as_view(http_method_names=['post']), name='brand_delete'),

    path('colors/', ColorListView.as_view(), name="color_list"),
    path('colors/<int:pk>/edit/', ColorUpdateView.as_view(), name='color_edit'),
    path('colors/<int:pk>/delete/', ColorDeleteView.as_view(http_method_names=['post']), name='color_delete'),
    path('colors/insert/', ColorCreateView.as_view(), name='color_create'),    

    path('vehicle_models', VehicleModelListView.as_view(), name="vehicle_model_list"),
    path('vehicle_models/JSON', VehicleModelListView.as_view(json=True), name='vehicle_model_json'),
    path('vehicle_models/<int:pk>/edit/', VehicleModelUpdateView.as_view(), name='vehicle_model_edit'),
    path('vehicle_models/<int:pk>/delete/', VehicleModelDeleteView.as_view(http_method_names=['post']), name='vehicle_model_delete'),
    path('vehicle_models/insert/', VehicleModelCreateView.as_view(), name='vehicle_model_create'),    

    path('vehicle_model_variants/JSON', VehicleModelVariantJSON, name='vehicle_model_variant_json'),

    path('cost_type', VehicleCostTypeListView.as_view(), name="vehicle_cost_type_list"),
    path('cost_type/JSON', VehicleCostTypeListView.as_view(json=True), name='vehicle_cost_type_json'),
    path('cost_type/<int:pk>/edit/', VehicleCostTypeUpdateView.as_view(), name='vehicle_cost_type_edit'),
    path('cost_type/<int:pk>/delete/', VehicleCostTypeDeleteView.as_view(http_method_names=['post']), name='vehicle_cost_type__delete'),
    path('cost_type/insert/', VehicleCostTypeCreateView.as_view(), name='vehicle_cost_type_create'),    

    path('vehicles', VehicleListView.as_view(), name="vehicle_list"),
    path('vehicles/<int:pk>/edit/', VehicleUpdateView.as_view(), name='vehicle_edit'),
    path('vehicles/insert/', VehicleCreateView.as_view(), name='vehicle_create'),
    path('vehicle_models/<int:pk>/delete/', VehicleDeleteView.as_view(http_method_names=['post']), name='vehicle_delete'),
]