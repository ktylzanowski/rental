from django.test import TestCase, Client
from django.urls import reverse
from django.utils import timezone
from accounts.models import MyUser
from .models import Payment, Shipping, Order, OrderItem
from products.models import ProductIndex, Rental, Book, Genre
from datetime import datetime
from decimal import Decimal


class OrderModelTest(TestCase):
    def setUp(self):
        self.user = MyUser.objects.create_user(
            email='testuser@test.com', password='testpass')
        self.payment = Payment.objects.create(
            user=self.user, payment_id='123456789', payment_method='Credit Card', amount_paid=100.00, status='Paid')
        self.shipping = Shipping.objects.create(
            user=self.user, shipping_method='UPS', is_paid=False, postage=10.00, quantity_of_items=2)

        self.genre = Genre.objects.create(name='Genre 1', category='book')
        self.rental = Rental.objects.create(name='Rental 1', city='City 1', zip_code='12345',
                                            street='Street 1', building_number='1')
        self.product = Book.objects.create(pk=1, title='Book 1', image='image.jpg', genre=self.genre, author='Author 1',
                                           isbn='1234567890')
        self.index = ProductIndex.objects.create(inventory_number='INV-001', product=self.product, rental=self.rental)

        self.order = Order.objects.create(
            user=self.user, order_date=timezone.now(), deadline=timezone.now(), return_date=timezone.now(),
            status='Ordered', total=110.00, debt=0.00, payment=self.payment, shipping=self.shipping,
            first_name='Test', last_name='User', phone='123-456-789',
            city='Test City', zip_code='12345', street='Test Street',
            building_number='123', apartment_number='1', if_extended=False, number_of_extensions=0)
        self.order_item = OrderItem.objects.create(
            product=self.product, product_index=self.index, order=self.order, user=self.user, price=50.00)

    def test_order_model(self):
        self.assertEqual(str(self.order), str(self.order.pk))
        self.assertEqual(self.order.total_cost(), 110.00)

    def test_order_item_model(self):
        self.assertEqual(str(self.order_item), f"{self.product} {self.order}")
        self.assertEqual(self.order_item.price, 50.00)

    def test_payment_model(self):
        self.assertEqual(str(self.payment), '123456789')
        self.assertEqual(self.payment.status, 'Paid')


class OrdersViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = MyUser.objects.create_user(email='testuser', password='testpass')
        self.genre = Genre.objects.create(name='Test Genre', category='book')
        self.rental = Rental.objects.create(name='Test Rental', city='Test City', zip_code='12345', street='Test Street', building_number='10')
        self.book = Book.objects.create(pk=1, title='Test Book', image='test.jpg', genre=self.genre, author='Test Author', isbn='123456789')
        self.product_index = ProductIndex.objects.create(inventory_number='001', product=self.book, rental=self.rental, is_available=True)
        self.payment = Payment.objects.create(
            user=self.user,
            payment_id='123456789',
            payment_method='Credit Card',
            amount_paid=Decimal('19.99'),
            status='Paid'
        )
        self.shipping = Shipping.objects.create(
            user=self.user,
            shipping_method='Standard',
            is_paid=True,
            postage=Decimal('2.50'),
            quantity_of_items=1
        )
        self.order = Order.objects.create(
            user=self.user,
            order_date=datetime.now(),
            deadline=datetime.now(),
            status='Ordered',
            total=Decimal('12.99'),
            debt=None,
            payment=self.payment,
            shipping=self.shipping,
            first_name='John',
            last_name='Doe',
            phone='123-456-7890',
            city='Test City',
            zip_code='12345',
            street='Test Street',
            building_number='123',
            apartment_number=None,
            if_extended=False,
            number_of_extensions=0
        )
        self.order_item = OrderItem.objects.create(
            product=self.book,
            product_index=self.product_index,
            order=self.order,
            user=self.user,
            price=Decimal('9.99')
        )

    def test_orders_view_redirects_when_not_logged_in(self):
        response = self.client.get(reverse('Orders'))
        self.assertEqual(response.status_code, 302)  # redirect
        self.assertRedirects(response, f'{reverse("Login")}?next={reverse("Orders")}')

    def test_orders_view_returns_orders_for_logged_in_user(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.get(reverse('Orders'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Book')

    def test_orders_view_excludes_returned_orders(self):
        self.client.login(username='testuser', password='testpass')
        self.order.status = 'Returned'
        self.order.save()
        response = self.client.get(reverse('Orders'))
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, 'Test Book')
