from django.views.generic import View
from .models import CartItem, Cart
from products.models import Order, OrderItem
from django.shortcuts import redirect, render
from django.utils import timezone
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages import success


class CartListView(LoginRequiredMixin, View):

    def get(self, request):
        user_cart = Cart.objects.get(user=request.user)
        items = CartItem.objects.filter(cart=user_cart)
        context = {"item_list": items}
        return render(request, "cart/cart.html", context)


class CheckoutView(LoginRequiredMixin, View):

    def post(self, request):
        user_cart = Cart.objects.get(user=request.user)
        items = CartItem.objects.filter(cart=user_cart)
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
        CartItem.objects.filter(cart=user_cart).delete()
        success(self.request, "Order placed")
        return redirect("home")
