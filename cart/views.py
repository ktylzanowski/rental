from django.views.generic import View
from django.shortcuts import redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from cart.cart import Cart
from django.contrib import messages
from django.shortcuts import render
from products.models import Product


class CartView(LoginRequiredMixin, View):
    def get(self, request):
        cart = Cart(request)
        return render(request, 'cart/cart.html', {'cart': cart})


class AddToCart(LoginRequiredMixin, View):

    def post(self, request, product_id):
        if not request.user.is_authenticated:
            messages.error(request, "You must be logged in")
            return redirect('Login')

        cart = Cart(request)

        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            messages.error(request, "Invalid product ID")
            return redirect('Home')

        if cart.add(product, request.user):
            messages.success(request, "Add to cart")
        else:
            messages.error(request, "Already in basket or already ordered or the number of items in the cart a"
                                    "maximum of 5")

        return redirect('Home')


class RemoveFromCart(LoginRequiredMixin, View):

    def post(self, request, product_id):
        cart = Cart(request)

        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            messages.error(request, "Invalid product ID")
            return redirect('Home')

        cart.remove(product)
        messages.success(request, "Item Deleted")
        return redirect("Cart")
