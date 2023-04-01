from decimal import Decimal
from django.conf import settings
from products.models import ProductIndex, Product, Rental
from orders.models import OrderItem


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
        rental_id = []
        for rental in self.cart.values():
            rental_id.append(int(rental['rental']))

        rental = Rental.objects.get(pk__in=rental_id)
        index = ProductIndex.objects.filter(product=product, is_available=True, rental=rental).first()
        return index

    def add(self, product, user):
        product_already_ordered = OrderItem.objects.filter(product=product, order__user=user)\
            .exclude(order__status="Returned")
        exceeds_max_in_basket = self.__len__() > 4

        if product_already_ordered is None or exceeds_max_in_basket:
            return False

        product_id = str(product.id)

        if product_id not in self.cart:
            if not self.cart:
                index = ProductIndex.objects.filter(product=product, is_available=True).first()
            else:
                index = self.check_if_in_the_same_rental(product)
                if index is None:
                    index = ProductIndex.objects.filter(product=product, is_available=True).first()

            self.cart[product_id] = {'price': str(product.price), 'index': index.pk, 'rental': index.rental.pk}

            index.is_available = False
            index.save()
            product.quantity -= 1

            if product.quantity == 0:
                product.is_available = False
            product.save()
            self.save()
            return True
        else:
            return False

    def remove(self, product):
        product_id = str(product.id)
        if product_id in self.cart:
            product_index = ProductIndex.objects.get(pk=self.cart[product_id]['index'])
            del self.cart[product_id]
            product_index.is_available = True
            product_index.save()
            product.quantity += 1
            product.save()
        self.save()

    def save(self):
        self.session.modified = True

    def clear(self):
        del self.session[settings.CART_SESSION_ID]
        self.save()
