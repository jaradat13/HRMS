from core.models import Company


def company_context(request):
    company_instance = Company.objects.first()  # Retrieve the company instance
    return {'company_instance': company_instance,
            'company_name': company_instance.name if company_instance else None,
            'company_logo': company_instance.logo.url if company_instance and company_instance.logo else None, }
