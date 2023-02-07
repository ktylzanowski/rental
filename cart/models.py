from django.db import models
from django.conf import settings
from products.models import Product


class Cart(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def total(self, request):
        user_cart = Cart.objects.get(user=request.user)
        items_in_cart = CartItem.objects.filter(cart=user_cart)
        total_price = 0
        for item in items_in_cart:
            total_price += item.product.price
        return total_price


class CartItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)



