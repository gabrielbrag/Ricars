import datetime
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.translation import gettext as _
import locale

date_validator = [
    MinValueValidator(1900),
    MaxValueValidator(9999)
]

class Brand(models.Model):
    brand_name = models.CharField(verbose_name=_('Brand'), max_length=30)
    
    def __str__(self) -> str:
        return self.brand_name

    @property
    def contextual_title(self):
        # Customize the name based on your desired logic
        return self.brand_name
    
class Vehicle_model(models.Model):
    MODEL_TYPE_CHOICES = [
        ('M', _('Motorcycle')),
        ('C', _('Car')),
        ('T', _('Truck')),
    ]   
    
    brand       = models.ForeignKey(Brand, verbose_name=_('Brand'), on_delete=models.CASCADE, related_name='brand')
    model_name  = models.CharField(verbose_name=_('Model'), max_length=30)
    model_type  = models.CharField(verbose_name=_('Type'), max_length=1, choices=MODEL_TYPE_CHOICES)
    
    def __str__(self) -> str:
        return self.brand.brand_name + ' ' + self.model_name

    @property
    def model_type_formatted(self):
        for choice in self.MODEL_TYPE_CHOICES:
            if choice[0] == self.model_type:
                return choice[1]
        return ''  
    
    @property
    def contextual_title(self):
        return self.model_name

class Vehicle_model_variant(models.Model):
    vehicle_model   = models.ForeignKey(Vehicle_model, on_delete=models.CASCADE, related_name='variants')
    variant_name    = models.CharField(max_length=30)
    
    def __str__(self) -> str:
        return str(self.vehicle_model) + ' ' + self.variant_name

    @property
    def contextual_title(self):
        return self.variant_name

class Color(models.Model):
    color_name = models.CharField(max_length=30, verbose_name=_('color name'))
    
    def __str__(self) -> str:
        return self.color_name
    
class Vehicle(models.Model):
    TRANSMISSION_CHOICES = [
        ('A', _('Automatic')),
        ('M', _('Manual')),
    ]
    FUEL_TYPE_CHOICES = [
        ('GAS', _('Gasoline')),
        ('ETH', _('Ethanol')),
        ('FLE', _('Flex')),
        ('DIE', _('Diesel')),
        ('ELE', _('Eletric'))
    ]    
        
    vehicle_variant = models.ForeignKey(Vehicle_model_variant, on_delete=models.CASCADE, related_name="variant", null=True, default=None)
    transmission    = models.CharField(verbose_name=_('transmission'), max_length=1, choices=TRANSMISSION_CHOICES)
    fuel_type       = models.CharField(verbose_name=_('fuel type'), max_length=3, choices=FUEL_TYPE_CHOICES)
    color           = models.ForeignKey(Color, verbose_name=_('color'), on_delete=models.CASCADE)
    purchase_price  = models.FloatField(verbose_name=_('purchase price'), default=0)
    sale_value      = models.FloatField(verbose_name=_('sale value'), null=True, blank=True, default=0)
    mileage         = models.IntegerField(verbose_name=_('mileage'), default=0)
    number_of_doors = models.IntegerField(verbose_name=_('number of doors'), default=4, null=True)
    license_plate   = models.CharField(verbose_name=_('license plate'), max_length=7, null=True)   
    model_year      = models.IntegerField(
        verbose_name=_('model year'),
        default=datetime.date.today().year,
        validators=date_validator
    )
    manufacture_year = models.IntegerField(
        verbose_name=_('manufacture year'),
        default=datetime.date.today().year,
        validators=date_validator
    )      
    sold = models.BooleanField(_('sold'), default=False)
    salesman_observation = models.TextField(verbose_name=_('observations'), default='')
    
    @property
    def in_stock(self):
        return self.sale_value is None

    def __str__(self) -> str:
        return '%s - %s' % (str(self.vehicle_variant), self.manufacture_year)

    @property
    def purchase_price_formatted(self):
        if self.purchase_price is not None:
            return locale.format_string('%.2f', self.purchase_price, grouping=True)
        return None

    @property
    def sale_value_formatted(self):
        if self.sale_value is not None:
            return locale.format_string('%.2f', self.sale_value, grouping=True)
        return None
    
    @property   
    def mileage_formatted(self):
        if self.mileage is not None:
            return locale.format_string('%d', self.mileage, grouping=True)
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
    def sold_as_checkbox(self):
        return '<input type="checkbox" readonly disabled ' + ('checked' if self.sold else '') + '>'

    @property
    def frontImageURL(self):
        front_image = Vehicle_image.objects.filter(vehicle=self, index=1).first()
        if front_image:
            return front_image.file.url
        return ''
    
    @property
    def maskedLicensePlate(self):
        first_char      = self.license_plate[0]
        last_char       = self.license_plate[-1]
        hidden_chars    = '*' * (len(self.license_plate) - 2)
        
        return first_char + hidden_chars + last_char        

class Vehicle_image(models.Model):
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, related_name="images")
    file    = models.ImageField(upload_to='images/')
    index   = models.IntegerField(null=True)
    
    @property
    def fileURL(self):
        return self.file.url

class Vehicle_cost_type(models.Model):
    cost_type_name = models.CharField(max_length=30, verbose_name=_("Name"))

    def __str__(self):
        return self.cost_type_name
    
class Vehicle_cost(models.Model):
    vehicle         = models.ForeignKey(Vehicle, on_delete=models.CASCADE, related_name="costs")
    cost_type       = models.ForeignKey(Vehicle_cost_type, on_delete=models.CASCADE)
    cost_name       = models.CharField(max_length=30)
    expense_date    = models.DateField() 
    value           = models.FloatField(null=True, blank=True)