from .forms import UserCreationForm
from django.views.generic import CreateView
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy


class RegisterCreateView(CreateView):
    form_class = UserCreationForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('home')


class MyLoginView(LoginView):
    def get_success_url(self):
        return reverse_lazy('home')
