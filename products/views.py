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
        obj, created = Cart.objects.get_or_create(
            user=request.user,
        )
        obj.save()

        item_product = Product.objects.get(id=pk)
        item = CartItem.objects.create(
            product=item_product,
            cart=obj,
        )
        item.save()
        messages.success(request, "Add to cart")
        return redirect('home')


class ProductsByCategoryView(View):
    def get(self, request, cats):
        cat = Product.objects.filter(category__name=cats)
        context = {'object_list': cat}
        return render(request, "products/home.html", context)
