from django.views.generic import ListView, View
from products.models import Product
from django.shortcuts import redirect, render
from cart.models import Cart, CartItem
from django.contrib import messages


class Home(ListView):
    model = Product
    template_name = 'products/home.html'
    ordering = ['-pk']


class ProductDetailView(View):

    def get(self, request, pk):
        product = Product.objects.get(id=pk)
        context = {'object': product}
        return render(request, "products/detailview.html", context)

    def post(self, request, pk):

        if not request.user.is_authenticated:
            messages.success(request, "You must be logged in")
            return redirect('Login')

        cart, created = Cart.objects.get_or_create(
            user=request.user,
        )
        cart.save()

        added_item = Product.objects.get(id=pk)

        item_in_cart = CartItem.objects.filter(cart=cart)
        for item in item_in_cart:
            if item.product.title == added_item.title:
                messages.success(request, "It's already in the basket")
                return redirect('ProductDetail', pk=pk)

        new_item_in_cart = CartItem.objects.create(
            product=added_item,
            cart=cart,
        )
        new_item_in_cart.save()

        added_item.quantity -= 1
        if added_item.quantity == 0:
            added_item.is_available = False
        added_item.save()

        messages.success(request, "Add to cart")
        return redirect('home')


class ProductsByCategoryView(View):
    def get(self, request, cats):
        cat = Product.objects.filter(category__name=cats)
        context = {'object_list': cat}
        return render(request, "products/home.html", context)
