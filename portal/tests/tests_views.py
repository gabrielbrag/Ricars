from django.test import Client, TestCase
from django.urls import reverse
from erp.models import Brand, Color, Vehicle, Vehicle_model, Vehicle_model_variant

class TestViews(TestCase):
    def setUp(self):
        self.client = Client()
        self.brand1 = Brand.objects.create(brand_name='Toyota')
        self.brand2 = Brand.objects.create(brand_name='Honda')
        self.color1 = Color.objects.create(name='Red')
        self.color2 = Color.objects.create(name='Blue')
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
            year=2021
        )
        self.vehicle2 = Vehicle.objects.create(
            vehicle_variant=self.variant2,
            transmission='A',
            fuel_type='E',
            color=self.color2,
            purchase_price=30000,
            sale_value=35000,
            mileage=5000,
            year=2022
        )
    
    def test_home_view(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'stock.html')
        self.assertEqual(len(response.context['vehicles']), 2)
        self.assertEqual(response.context['vehicles'][0].sale_value, 25000)
        self.assertEqual(list(response.context['possible_vehicle_years']), [2021, 2022])
    
    def test_vehiclesPanel_view_with_one_filter(self):
        response = self.client.get(reverse('vehiclesPanel'), {'maxPrice': '26000'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.vehicle1.vehicle_variant.vehicle_model.model_name)
        self.assertNotContains(response, self.vehicle2.vehicle_variant.vehicle_model.model_name)
        
    def test_vehiclesPanel_view_with_multiple_filters(self):
        response = self.client.get(reverse('vehiclesPanel'), {'minPrice': '25000', 'maxPrice': '35000', 'years': '2021,2022'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.vehicle1.vehicle_variant.vehicle_model.model_name)
        self.assertContains(response, self.vehicle2.vehicle_variant.vehicle_model.model_name)
        
    def test_vehiclesPanel_view_with_no_filters(self):
        response = self.client.get(reverse('vehiclesPanel'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.vehicle1.vehicle_variant.vehicle_model.model_name)
        self.assertContains(response, self.vehicle2.vehicle_variant.vehicle_model.model_name)
        
    def test_vehiclesPanel_view_with_invalid_filters(self):
        response = self.client.get(reverse('vehiclesPanel'), {'minPrice': '50000', 'maxPrice': '60000'})
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, self.vehicle1.vehicle_variant.vehicle_model.model_name)
        self.assertNotContains(response, self.vehicle2.vehicle_variant.vehicle_model.model_name)
        
    def test_vehiclesPanel_view_with_invalid_year_filter(self):
        response = self.client.get(reverse('vehiclesPanel'), {'years': '2020,2023'})
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, self.vehicle1.vehicle_variant.vehicle_model.model_name)
        self.assertNotContains(response, self.vehicle2.vehicle_variant.vehicle_model.model_name)
