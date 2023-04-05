from django.contrib.auth.signals import user_logged_out
from .cart import Cart
from django.dispatch import receiver
from django.db.models import F
from products.models import Product, ProductIndex


@receiver(user_logged_out)
def handle_user_logout(sender, request, user, **kwargs):
    cart = Cart(request)
    for item in cart:
        product = item['product']
        Product.objects.filter(pk=product.pk).update(quantity=F('quantity') + 1, is_available=True)
        ProductIndex.objects.filter(pk=item['index']).update(is_available=True)
