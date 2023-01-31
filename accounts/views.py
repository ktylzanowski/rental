from .forms import UserCreationForm, AddressForm
from django.views.generic import (
    CreateView, UpdateView, View, DetailView
        )
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import MyUser
from products.models import OrderItem, Order
from django.shortcuts import render


class RegisterCreateView(CreateView):
    form_class = UserCreationForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('home')


class MyLoginView(LoginView):
    def get_success_url(self):
        return reverse_lazy('home')


class AccountView(LoginRequiredMixin, UpdateView):
    model = MyUser
    form_class = AddressForm
    template_name = 'registration/account.html'

    def get_success_url(self):
        return self.request.path

    def form_valid(self, form):
        return super().form_valid(form)

    def get_queryset(self):
        return MyUser.objects.filter(pk=self.request.user.pk)


class OrdersView(LoginRequiredMixin, View):
    model = OrderItem
    template_name = "registration/orders.html"

    def get(self, request):
        obj = OrderItem.objects.filter(user=request.user)
        context = {'object_list': obj}
        return render(request, "registration/orders.html", context)


