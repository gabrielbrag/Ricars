from django.urls import path
from portal.views import home, vehiclesPanel

urlpatterns = [
    path('', home),
    path('vehiclesPanel', vehiclesPanel)
]