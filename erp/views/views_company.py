from companies.models import Company, Shop
from django.shortcuts import redirect, render
from django.views import View
from django.utils.translation import gettext as _

class CompanyView(View):
    def get(self, request):
        company_data = {}
        default_company = Company.objects.first()
        company_data["name"] = default_company.name
        company_data["document"] = default_company.document
        company_data["instagram_link"] = default_company.instagram_link
        company_data["facebook_link"] = default_company.facebook_link
        company_data["whatsapp_number"] = default_company.whatsapp_number
        company_data["about_text"] = default_company.about_text
        
        default_shop = Shop.objects.first()
        company_data["address_street"]          = default_shop.address_street
        company_data["address_zipcode"]         = default_shop.address_zipcode
        company_data["address_number"]          = default_shop.address_number
        company_data["address_complement"]      = default_shop.address_complement
        company_data["address_neighborhood"]    = default_shop.address_neighborhood
        company_data["address_city"]            = default_shop.address_city
        company_data["address_state"]           = default_shop.address_street
        
        return render(request, 'erp/forms/company_edit.html', {"company_data":company_data})
    
    def post(self, request):
        try:
            company = Company.objects.first()
            
            company.name = company_name = request.POST.get('company_name')
            company.document = request.POST.get('cnpj')
            company.instagram_link = request.POST.get('instagram')
            company.facebook_link = request.POST.get('facebook')
            company.whatsapp_number = request.POST.get('whatsapp')
            company.about_text = request.POST.get('about')
            company.save()
            
            default_shop = Shop.objects.first()
            
            default_shop.address_zipcode = request.POST.get('zipcode')
            default_shop.address_street = request.POST.get('street')
            default_shop.address_number = request.POST.get('number')
            default_shop.address_state = request.POST.get('state')
            default_shop.address_city = request.POST.get('city')
            default_shop.address_neighborhood = request.POST.get('neighborhood')
            default_shop.address_complement = request.POST.get('complement')
        
            default_shop.save()

            return redirect(request.META['HTTP_REFERER'])

        except Exception as e:
            # Handle any exceptions or validation errors
            error_message = _('An error occurred while processing the form.')
            return redirect(request.META['HTTP_REFERER'])