from django.urls import path
from portal.views import home, vehiclesPanel

urlpatterns = [
    path('', home, name='home'),
    path('vehiclesPanel', vehiclesPanel, name='vehiclesPanel')
]