from django.db import models

class Company(models.Model):
    name            = models.CharField(max_length=30, null=True, blank=True)
    document        = models.CharField(max_length=30, null=True, blank=True)
    instagram_link  = models.URLField(null=True, blank=True) 
    facebook_link   = models.URLField(null=True, blank=True)
    whatsapp_number = models.CharField(max_length=13, null=True, blank=True)
    
    def __str__(self):
        return self.name
    
class Shop(models.Model):
    name                    = models.CharField(max_length=30, default="")
    company                 = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='shops')
    address_street          = models.CharField(max_length=50, null=True, blank=True)
    address_zipcode         = models.CharField(max_length=8, null=True, blank=True)
    address_number          = models.IntegerField(null=True, blank=True)
    address_complement      = models.CharField(max_length=50, null=True, blank=True)
    address_neighborhood    = models.CharField(max_length=50, null=True, blank=True)    
    address_city            = models.CharField(max_length=50, null=True, blank=True)
    address_state           = models.CharField(max_length=2, null=True, blank=True)
    
    def __str__(self):
        return self.name
    
    @property
    def address_zipcodeFormatted(self):
        return '%s - %s' % (self.address_zipcode[0:1], self.address_zipcode[2:])
    
    @property
    def shopAddress(self):
        return '%s, %s - %s, %s - %s, %s' % (self.address_street, 
                                            self.address_number, 
                                            self.address_neighborhood, 
                                            self.address_city, 
                                            self.address_state,
                                            self.address_zipcodeFormatted)
    