from orders.models import OrderItem, Order
from django.shortcuts import render, redirect
from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages import success


class OrdersView(LoginRequiredMixin, View):
    model = OrderItem
    template_name = "registration/orders.html"

    def get(self, request):
        orders_items = OrderItem.objects.filter(user=request.user)
        orders_items_extended = OrderItem.objects.filter(user=request.user, order__status='Extended')

        price = 0
        for item in orders_items_extended:
            price += item.debt

        context = {'object_list': orders_items, 'price': price}
        return render(request, "orders/orders.html", context)


class PayDebt(View):
    def get(self, request):
        success(request, "Your debt was paid!")
        return redirect('Orders')

    def post(self, request):
        orders = Order.objects.filter(user=request.user, status='Extended')
        orders_items_extended = OrderItem.objects.filter(user=request.user, order__status='Extended')
        
        for item in orders_items_extended:
            item.debt = 0
            item.save()

        for order in orders:
            order.status = 'Delivered'
            order.save()

        return redirect("home")
