from django.urls import path
from portal.views import home, vehiclesPanel, vehicleView, aboutView

urlpatterns = [
    path('', home, name='home'),
    path('vehiclesPanel', vehiclesPanel, name='vehiclesPanel'),
    path('vehicle', vehicleView, name='vehicleView'),
    path('about', aboutView, name="aboutView")
]