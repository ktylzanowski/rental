from orders.models import OrderItem
from django.shortcuts import render, redirect
from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages import success


class OrdersView(LoginRequiredMixin, View):
    model = OrderItem
    template_name = "registration/orders.html"

    def get(self, request):
        obj = OrderItem.objects.filter(user=request.user)
        context = {'object_list': obj}
        return render(request, "orders/orders.html", context)


def order_complete(request):
    success(request, "Your debt was paid!")
    return redirect('Orders')


class PayDebt(View):
    def post(self, request):
        print(request.POST)
        return redirect("home")
