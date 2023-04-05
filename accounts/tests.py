from django.test import TestCase
from django.urls import reverse
from .models import MyUser


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


class MyLogoutViewTestCase(TestCase):
    def setUp(self):
        self.user = MyUser.objects.create_user(
            email='testuser@example.com',
            password='testpassword123',
        )

    def test_logout(self):
        self.client.login(email=self.user.email, password=self.user.password)
        response = self.client.post(reverse('Logout'))
        self.assertRedirects(response, reverse('Home'))
