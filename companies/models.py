from django.db import models
import re

class Company(models.Model):
    name            = models.CharField(max_length=30, blank=True)
    document        = models.CharField(max_length=30, blank=True)
    instagram_link  = models.URLField(null=True, blank=True) 
    facebook_link   = models.URLField(null=True, blank=True)
    whatsapp_number = models.CharField(max_length=13, blank=True)
    about_text      = models.TextField()

    def __str__(self):
        return self.name

    @property
    def whatsapp_number_international(self):
        #TO DO Implement other countries
        return "55" + self.whatsapp_number

    @property 
    def masked_whatsapp_number(self):
        numeric_phone = re.sub(r'\D', '', self.whatsapp_number)
        
        if len(numeric_phone) < 10:
            return self.whatsapp_number
        
        # Format the phone number with DDD and mask all but the last 4 digits
        masked_phone = '({}) {}-{}'.format(numeric_phone[:2], numeric_phone[2:6], numeric_phone[-4:])
        
        return masked_phone
    
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
        return '%s - %s' % (self.address_zipcode[:5], self.address_zipcode[5:])
    
    @property
    def shopAddress(self):
        return '%s, %s %s, %s - %s, %s' % (self.address_street, 
                                            self.address_number, 
                                            self.address_neighborhood, 
                                            self.address_city, 
                                            self.address_state,
                                            self.address_zipcodeFormatted)
    