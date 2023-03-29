from decimal import Decimal
from django.conf import settings
from products.models import Product


class Cart(object):
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def __iter__(self):
        product_ids = self.cart.keys()
        products = Product.objects.filter(pk__in=product_ids)
        cart = self.cart.copy()
        for product in products:
            cart[str(product.id)]['product'] = product
        for item in cart.values():
            item['price'] = Decimal(item['price'])
            yield item

    def __len__(self):
        return sum(item['quantity'] for item in self.cart.values())

    def get_total_quantity(self):
        return sum(item for item in self.cart.values())

    def get_total_price(self):
        return sum(Decimal(item['price']) for item in self.cart.values())
    
    def add(self, product):
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {'quantity': 1, 'price': str(product.price)}
            product.quantity -= 1
            product.save()
            self.save()
            return True
        else:
            return False

    def remove(self, product):
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            product.quantity += 1
            product.save()
        self.save()

    def save(self):
        self.session.modified = True

    def clear(self):
        del self.session[settings.CART_SESSION_ID]
        self.save()
