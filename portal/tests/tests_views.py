from baseTestCase import baseTestCase
from django.urls import reverse
from erp.models import Brand, Color, Vehicle, Vehicle_model, Vehicle_model_variant

class TestViews(baseTestCase):   
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
        response = self.client.get(reverse('vehiclesPanel'), {'minPrice': '25000', 'maxPrice': '35000', 'model_years': '2021,2022'})
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
        
    def test_vehiclesPanel_view_with_invalid_model_year_filter(self):
        response = self.client.get(reverse('vehiclesPanel'), {'years': '2020,2023'})
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, self.vehicle1.vehicle_variant.vehicle_model.model_name)
        self.assertNotContains(response, self.vehicle2.vehicle_variant.vehicle_model.model_name)
