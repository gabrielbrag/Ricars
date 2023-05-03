import datetime
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

class Brand(models.Model):
    brand_name = models.CharField(max_length=30)
    
    def __str__(self) -> str:
        return self.brand_name
    
class Vehicle_model(models.Model):
    MODEL_TYPE_CHOICES = [
        ('M', 'Motorcycle'),
        ('C', 'Car'),
        ('T', 'Truck'),
    ]   
    
    brand       = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name='brand')
    model_name  = models.CharField(max_length=30)
    model_type  = models.CharField(max_length=1, choices=MODEL_TYPE_CHOICES)
    
    def __str__(self) -> str:
        return self.brand.brand_name + ' ' + self.model_name

class Vehicle_model_variant(models.Model):
    vehicle_model   = models.ForeignKey(Vehicle_model, on_delete=models.CASCADE, related_name='model')
    variant_name    = models.CharField(max_length=30)
    
    def __str__(self) -> str:
        return str(self.vehicle_model) + ' ' + self.variant_name

class Color(models.Model):
    name = models.CharField(max_length=30)
    
    def __str__(self) -> str:
        return self.name
    
class Vehicle(models.Model):
    TRANSMISSION_CHOICES = [
        ('A', 'Automatic'),
        ('M', 'Manual'),
    ]
    FUEL_TYPE_CHOICES = [
        ('G', 'Gasoline'),
        ('E', 'Ethanol'),
        ('F', 'Flex'),
        ('D', 'Diesel'),
    ]    
    
    vehicle_variant = models.ForeignKey(Vehicle_model_variant, on_delete=models.CASCADE, related_name="variant", null=True, default=None)
    transmission    = models.CharField(max_length=1, choices=TRANSMISSION_CHOICES)
    fuel_type       = models.CharField(max_length=1, choices=FUEL_TYPE_CHOICES)
    color           = models.ForeignKey(Color, on_delete=models.CASCADE)
    purchase_price  = models.FloatField(default=0)
    sale_value      = models.FloatField(null=True, blank=True)
    mileage         = models.IntegerField(default=0)
    number_of_doors = models.IntegerField(default=2, null=True)
    license_plate   = models.CharField(max_length=7, null=True)   
    year            = models.IntegerField(
        default=datetime.date.today().year,
        validators=[
            MinValueValidator(1900),
            MaxValueValidator(9999)
        ]
    )
        
    @property
    def in_stock(self):
        return self.sale_value is None

    def __str__(self) -> str:
        return '%s - %s' % (str(self.vehicle_variant), self.year)

    @property
    def sale_value_formatted(self):
        if self.sale_value is not None:
            return f'{self.sale_value:.2f}'
        return None
    
    @property   
    def mileage_formatted(self):
        if self.mileage is not None:
            return f'{self.mileage} KM'
        return None    
    
    @property
    def transmission_formatted(self):
        for choice in self.TRANSMISSION_CHOICES:
            if choice[0] == self.transmission:
                return choice[1]
        return '' 
    
    @property
    def fuel_type_formatted(self):
        for choice in self.FUEL_TYPE_CHOICES:
            if choice[0] == self.fuel_type:
                return choice[1]
        return ''    
    
    @property
    def frontImageURL(self):
        front_image = Vehicle_image.objects.filter(vehicle=self, index=1).first()
        if front_image:
            return front_image.file.url
        return ''

class Vehicle_image(models.Model):
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, related_name="vehicle")
    file    = models.ImageField(upload_to='images/')
    index   = models.IntegerField(null=True)

class Vehicle_cost_type(models.Model):
    cost_name = models.CharField(max_length=30)

class Vehicle_cost(models.Model):
    cost_type       = models.ForeignKey(Vehicle_cost_type, on_delete=models.CASCADE)
    cost_name       = models.CharField(max_length=30)
    expense_date    = models.DateField() 
    value           = models.FloatField(null=True, blank=True)