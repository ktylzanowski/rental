from django.views.generic import View
from django.shortcuts import redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages import success
from cart.cart import Cart
from django.contrib import messages
from django.shortcuts import get_object_or_404, render
from products.models import Product


class CartView(LoginRequiredMixin, View):
    def get(self, request):
        cart = Cart(request)
        return render(request, 'cart/cart.html', {'cart': cart})


class AddToCart(LoginRequiredMixin, View):

    def post(self, request, product_id):
        if not request.user.is_authenticated:
            messages.success(request, "You must be logged in")
            return redirect('Login')
        cart = Cart(request)
        product = get_object_or_404(Product, id=product_id)
        if cart.add(product):
            messages.success(request, "Add to cart")
            return redirect('home')
        else:
            messages.success(request, "Already in basket")
            return redirect('home')


class RemoveFromCart(LoginRequiredMixin, View):

    def post(self, request, product_id):
        cart = Cart(request)
        product = get_object_or_404(Product, id=product_id)

        cart.remove(product)
        success(self.request, "Item Deleted")
        return redirect("Cart")


