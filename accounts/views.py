from .forms import UserCreationForm, AddressForm
from django.views.generic import (
    CreateView, UpdateView,
        )
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.shortcuts import redirect, get_object_or_404
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from .models import MyUser
from django.contrib import messages


class RegisterCreateView(CreateView):
    form_class = UserCreationForm
    template_name = 'registration/register.html'

    def get_success_url(self):
        messages.success(self.request, "Registered")
        return reverse_lazy('Home')


class MyLoginView(LoginView):
    def get_success_url(self):
        messages.success(self.request, "Log in")
        return reverse_lazy('Home')


class MyLogoutView(LogoutView):
    def get_success_url(self):
        messages.success(self.request, "Log out")
        return reverse_lazy('Home')


@method_decorator(login_required, name='dispatch')
class AccountView(UpdateView):
    model = MyUser
    form_class = AddressForm
    template_name = 'registration/account.html'

    def dispatch(self, request, *args, **kwargs):
        obj = get_object_or_404(MyUser, pk=kwargs['pk'])
        if self.request.user.pk != obj.pk:
            messages.error(request, "You are not authorized to edit this user's data.")
            return redirect(reverse_lazy('Home'))
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.save(commit=False)
        messages.success(self.request, "Personal information updated.")
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('Account', kwargs={'pk': self.get_object().pk})
