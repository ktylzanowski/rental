from decimal import Decimal
from django.conf import settings
from products.models import ProductIndex, Product
from orders.models import OrderItem
from django.db.models import F


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
        return len(self.cart)

    def get_total_price(self):
        return sum(Decimal(item['price']) for item in self.cart.values())

    def check_if_in_the_same_rental(self, product):
        rental_ids = [int(rental['rental']) for rental in self.cart.values()] if self.cart else []
        index = ProductIndex.objects.filter(product=product, is_available=True, rental__in=rental_ids).first()
        if not index:
            index = ProductIndex.objects.filter(product=product, is_available=True).first()
        return index

    def add(self, product, user):
        product_already_ordered = OrderItem.objects.filter(product=product, order__user=user)\
            .exclude(order__status="Returned")

        if product_already_ordered.exists() or self.__len__() > 4:
            return False

        product_id = str(product.id)

        if product_id not in self.cart:
            index = self.check_if_in_the_same_rental(product)
            self.cart[product_id] = {'price': str(product.price), 'index': index.pk, 'rental': index.rental.pk}

            ProductIndex.objects.filter(pk=index.pk).update(is_available=False)

            product.quantity -= 1
            product.save()

            self.save()
            return True
        else:
            return False

    def remove(self, product):
        product_id = str(product.id)
        if product_id in self.cart:

            product_index = ProductIndex.objects.get(pk=self.cart[product_id]['index'])
            ProductIndex.objects.filter(pk=product_index.pk).update(is_available=True)
            Product.objects.filter(pk=product.id).update(quantity=F('quantity') + 1)
            del self.cart[product_id]
            self.save()

            return True
        return False

    def save(self):
        self.session.modified = True

    def clear(self):
        del self.session[settings.CART_SESSION_ID]
        self.save()
