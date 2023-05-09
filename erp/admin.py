from django.contrib import admin
from erp.models import Brand, Vehicle_model, Vehicle_model_variant, Color, Vehicle, Vehicle_image

admin.site.register(Brand)
admin.site.register(Color)
admin.site.register(Vehicle_model)
admin.site.register(Vehicle_model_variant)
admin.site.register(Vehicle)
admin.site.register(Vehicle_image) 