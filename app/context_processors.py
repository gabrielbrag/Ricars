from companies.models import Company, Shop

def company_context(request):
    company = Company.objects.first()
    shop = Shop.objects.first()
    
    return {'context_company': company, 'context_shop': shop}