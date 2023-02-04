from django.views.generic import View
from .models import CartItem, Cart
from products.models import Order, OrderItem, Product
from django.shortcuts import redirect, render
from django.utils import timezone
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages import success


class CartListView(LoginRequiredMixin, View):

    def get(self, request):
        user_cart, created = Cart.objects.get_or_create(
            user=request.user,
        )
        user_cart.save()
        items = CartItem.objects.filter(cart=user_cart)
        price = 0
        for item in items:
            price += item.product.price
        context = {"item_list": items, "price": price}
        return render(request, "cart/cart.html", context)


class CheckoutView(LoginRequiredMixin, View):

    def post(self, request):
        user_cart = Cart.objects.get(user=request.user)
        items_in_cart = CartItem.objects.filter(cart=user_cart)
        if len(items_in_cart) == 0:
            success(self.request, "The cart is empty")
            return redirect('home')

        if request.user.if_address():
            success(self.request, "You need to fill in the data")
            return redirect("Account", pk=request.user.pk)

        order = Order.objects.create(
            user=request.user,
            order_date=timezone.now(),
            status="Ordered",
            total=user_cart.total(request),
            first_name=request.user.first_name,
            last_name=request.user.last_name,
            phone=request.user.phone,
            city=request.user.city,
            zip_code=request.user.zip_code,
            street=request.user.street,
            building_number=request.user.building_number,
            apartment_number=request.user.apartment_number,
        )
        order.save()

        for item in items_in_cart:
            orderitem = OrderItem.objects.create(
                product=item.product,
                order=order,
                user=request.user,
            )
            orderitem.save()

        CartItem.objects.filter(cart=user_cart).delete()
        Cart.objects.get(user=request.user).delete()
        success(self.request, "Order placed")
        return redirect("home")


class DeleteItemView(LoginRequiredMixin, View):
    def post(self, request, pk):
        item_to_removed = CartItem.objects.get(pk=pk)

        item = Product.objects.get(pk=item_to_removed.product.pk)
        item.quantity += 1

        if not item.is_available:
            item.is_available = True
        item.save()
        item_to_removed.delete()
        success(self.request, "Item Deleted")
        return redirect("Cart")
