from orders.models import OrderItem, Order, Payment
from django.shortcuts import redirect
from django.views.generic import View, DetailView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages import success
from products.models import Rental
from django.db.models import Prefetch
import datetime
import json


class OrdersView(LoginRequiredMixin, ListView):
    model = Order
    template_name = "orders/orders.html"

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.prefetch_related(
            Prefetch('orderitem_set', OrderItem.objects.select_related('product'))
        ).filter(user=self.request.user).exclude(status='Returned')
        return qs

    def get_context_data(self, *, object_list=None, **kwargs):
        data = super().get_context_data(**kwargs)
        orders_items_extended = OrderItem.objects.filter(user=self.request.user, order__status='Extended')
        price = 0
        for item in orders_items_extended:
            price += item.debt
        data['price'] = price
        return data


class OrdersArchiveView(ListView):
    model = Order
    template_name = "orders/ordersarchive.html"

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.prefetch_related(
            Prefetch('orderitem_set', OrderItem.objects.select_related('product'))
        ).filter(user=self.request.user, status='Returned')
        return qs


class PayDebt(View):
    def get(self, request):
        success(request, "Your debt was paid!")
        return redirect('Orders')

    def post(self, request):
        orders = Order.objects.filter(user=request.user, status='Extended')
        orders_items_extended = OrderItem.objects.filter(user=request.user, order__status='Extended')

        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)

        payment = Payment.objects.create(
            user=request.user,
            payment_id=body['transID'],
            payment_method=body['payment_method'],
            amount_paid=15,
            status='payment',
        )
        payment.save()

        for item in orders_items_extended:
            item.debt = 0
            item.save()

        for order in orders:
            order.status = 'Delivered'
            order.save()

        return redirect("home")


class ReturnView(DetailView):
    model = Order
    template_name = 'orders/returntorental.html'

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        rental = Rental.objects.all()
        data['object_list'] = rental
        return data


class MakeReturn(View):
    def post(self, request, pk):
        order = Order.objects.get(pk=pk)
        order.status = 'Returned'
        order.return_date = datetime.datetime.now()
        order.save()
        success(request, "Order returned")
        return redirect('home')
