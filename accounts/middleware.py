from django.shortcuts import redirect
from django.urls import reverse
from django.conf import settings

class AuthRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        if not request.path.startswith('/erp/') or request.user.is_authenticated or request.path == settings.LOGIN_URL:
            return self.get_response(request)
        else:
            return redirect(reverse('login'))
