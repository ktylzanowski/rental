from django.views.generic import View
from .models import CartItem, Cart
from products.models import Order, OrderItem, Product, Payment
from django.shortcuts import redirect, render
from django.utils import timezone
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages import success
from django.contrib.auth.decorators import login_required
import json
from django.core.mail import EmailMessage
from django.conf import settings
from django.template.loader import render_to_string
from datetime import timedelta


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


@login_required()
def order_complete(request):
    success(request, "Your order was successful!")
    return redirect('home')


class CheckoutView(LoginRequiredMixin, View):

    def post(self, request):
        user_cart = Cart.objects.get(user=request.user)
        items_in_cart = CartItem.objects.filter(cart=user_cart)

        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)

        payment = Payment.objects.create(
            user=request.user,
            payment_id=body['transID'],
            payment_method=body['payment_method'],
            amount_paid=user_cart.total(request),
            status=body['status'],
        )
        payment.save()

        order = Order.objects.create(
            user=request.user,
            order_date=timezone.now(),
            return_date=timezone.now()+timedelta(days=7),
            status="Ordered",
            total=user_cart.total(request),
            payment=payment,
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

        email_template = render_to_string('cart/email_payment_success.html', {})
        email = EmailMessage(
            'TEST',
            email_template,
            settings.EMAIL_HOST_USER,
            ['ktylzanowski@gmail.com'],
        )
        email.fail_silently = False
        email.send()

        return redirect('Cart')


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


