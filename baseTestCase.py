from django.test import TestCase, Client
from erp.models import Brand, Color, Vehicle, Vehicle_model, Vehicle_model_variant

class baseTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.brand1 = Brand.objects.create(brand_name='Toyota')
        self.brand2 = Brand.objects.create(brand_name='Honda')
        self.color1 = Color.objects.create(color_name='Red')
        self.color2 = Color.objects.create(color_name='Blue')
        self.model1 = Vehicle_model.objects.create(
            brand=self.brand1,
            model_name='Corolla',
            model_type='C'
        )
        self.model2 = Vehicle_model.objects.create(
            brand=self.brand2,
            model_name='Accord',
            model_type='C'
        )
        self.variant1 = Vehicle_model_variant.objects.create(
            vehicle_model=self.model1,
            variant_name='LE'
        )
        self.variant2 = Vehicle_model_variant.objects.create(
            vehicle_model=self.model2,
            variant_name='EX-L'
        )
        self.vehicle1 = Vehicle.objects.create(
            vehicle_variant=self.variant1,
            transmission='M',
            fuel_type='G',
            color=self.color1,
            purchase_price=20000,
            sale_value=25000,
            mileage=10000,
            model_year=2020,
            manufacture_year = 2021
        )
        self.vehicle2 = Vehicle.objects.create(
            vehicle_variant=self.variant2,
            transmission='A',
            fuel_type='E',
            color=self.color2,
            purchase_price=30000,
            sale_value=35000,
            mileage=5000,
            model_year=2021,
            manufacture_year = 2022
        )
