from django.contrib.auth import logout
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView

def logout_view(request):
    print("Session before logout:", request.session.items())
    logout(request)
    print("Session after logout:", request.session.items())
    return redirect('login')  # Redirect to the login page

class CustomLoginView(LoginView):
    template_name = 'registration/login.html'  # Replace with your actual login template path
    success_url = reverse_lazy('home')  # Replace 'home' with the name of your home view URL
