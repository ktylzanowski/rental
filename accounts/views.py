from .forms import UserCreationForm, AddressForm
from django.views.generic import (
    CreateView, UpdateView,
        )
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import MyUser
from django.contrib.messages import success


class RegisterCreateView(CreateView):
    form_class = UserCreationForm
    template_name = 'registration/register.html'

    def get_success_url(self):
        success(self.request, "Registered")
        return reverse_lazy('Home')


class MyLoginView(LoginView):
    def get_success_url(self):
        success(self.request, "Log in")
        return reverse_lazy('Home')


class MyLogoutView(LogoutView):
    def get_success_url(self):
        success(self.request, "Log out")
        return reverse_lazy('Home')


class AccountView(LoginRequiredMixin, UpdateView):
    model = MyUser
    form_class = AddressForm
    template_name = 'registration/account.html'

    def get_success_url(self):
        success(self.request, "Correctly change personal information")
        return self.request.path

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

    def get_queryset(self):
        return MyUser.objects.filter(pk=self.request.user.pk)
