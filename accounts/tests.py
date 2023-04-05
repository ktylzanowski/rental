from django.test import TestCase, Client
from django.urls import reverse
from .models import MyUser
from accounts.forms import AddressForm


class RegisterCreateViewTest(TestCase):
    def test_register_form(self):
        response = self.client.get(reverse('Register'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/register.html')
        self.assertContains(response, 'Register')

        data = {
            'email': 'testuser@example.com',
            'password1': 'testpassword123',
            'password2': 'testpassword123',
        }
        response = self.client.post(reverse('Register'), data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('Home'))

        self.assertTrue(MyUser.objects.filter(email='testuser@example.com').exists())


class MyLoginViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = MyUser.objects.create_user(
            email='testuser@test.com',
            password='testpass123'
        )
        self.url = reverse('Login')
        self.home_url = reverse('Home')

    def test_login_success(self):
        response = self.client.post(self.url, {'username': 'testuser@test.com', 'password': 'testpass123'})
        self.assertRedirects(response, self.home_url)

    def test_login_failure(self):
        response = self.client.post(self.url, {'username': 'testuser', 'password': 'wrongpass'})
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.wsgi_request.user.is_authenticated)


class AccountViewTestCase(TestCase):
    def setUp(self):
        self.user = MyUser.objects.create_user(
            email='testuser@example.com',
            password='testpass123'
        )
        self.client.login(username='testuser@example.com', password='testpass123')

    def test_account_view_returns_200(self):
        response = self.client.get(reverse('Account', kwargs={'pk': self.user.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.context['form'], AddressForm)


class MyLogoutViewTestCase(TestCase):
    def setUp(self):
        self.user = MyUser.objects.create_user(
            email='testuser@example.com',
            password='testpassword123',
        )

    def test_logout(self):
        self.client.login(username=self.user.email, password=self.user.password)
        response = self.client.post(reverse('Logout'))
        self.assertRedirects(response, reverse('Home'))
