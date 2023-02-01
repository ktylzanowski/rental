from django.views.generic import View
from .models import CartItem
from products.models import Order, OrderItem
from django.shortcuts import redirect, render
from django.utils import timezone
from django.contrib.auth.mixins import LoginRequiredMixin


class CartListView(LoginRequiredMixin, View):

    def get(self, request):
        items = CartItem.objects.filter(cart=request.user.id)
        context = {"item_list": items}
        return render(request, "cart/cart.html", context)


class CheckoutView(LoginRequiredMixin, View):

    def post(self, request):
        items = CartItem.objects.filter(cart=request.user.id)
        order = Order.objects.create(
            user=request.user,
            order_date=timezone.now(),
        )
        order.save()
        for item in items:
            orderitem = OrderItem.objects.create(
                product=item.product,
                order=order,
                user=request.user,
            )
            orderitem.save()
        CartItem.objects.filter(cart=request.user.id).delete()
        return redirect("home")
