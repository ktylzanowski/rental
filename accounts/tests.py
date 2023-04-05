from django.test import TestCase, Client
from django.urls import reverse
from .models import MyUser
from accounts.forms import AddressForm
from .forms import UserCreationForm


class MyUserModelTestCase(TestCase):
    def setUp(self):
        self.user = MyUser.objects.create(email='test@example.com')
        self.user.set_password('testpassword')
        self.user.save()

    def test_user_can_be_authenticated(self):
        self.assertTrue(self.user.check_password('testpassword'))
        self.assertFalse(self.user.check_password('wrongpassword'))

    def test_user_is_active_by_default(self):
        self.assertTrue(self.user.is_active)

    def test_user_is_not_staff_by_default(self):
        self.assertFalse(self.user.is_staff)

    def test_user_is_not_admin_by_default(self):
        self.assertFalse(self.user.is_admin)


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
        self.client = Client()
        self.user = MyUser.objects.create_user(email='testuser@example.com', password='testpass')
        self.other_user = MyUser.objects.create_user(email='otheruser@example.com', password='otherpass')
        self.url = reverse('Account', kwargs={'pk': self.user.pk})

    def test_redirects_if_not_logged_in(self):
        response = self.client.get(self.url)
        self.assertRedirects(response, '/login/?next=/account/1')

    def test_redirects_if_not_authorized_to_edit_user_data(self):
        self.client.force_login(self.other_user)
        response = self.client.get(self.url)
        self.assertRedirects(response, reverse('Home'))

    def test_renders_form_for_logged_in_user(self):
        self.client.force_login(self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/account.html')
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


class UserCreationFormTest(TestCase):
    def test_form_with_valid_data_should_be_valid(self):
        form_data = {
            'email': 'test@example.com',
            'password1': 'test_password',
            'password2': 'test_password'
        }
        form = UserCreationForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_form_with_invalid_email_should_raise_validation_error(self):
        form_data = {
            'email': 'invalid_email',
            'password1': 'test_password',
            'password2': 'test_password'
        }
        form = UserCreationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['email'], ['Enter a valid email address.'])

    def test_form_with_existing_email_should_raise_validation_error(self):
        MyUser.objects.create_user(email='test@example.com', password='test_password')
        form_data = {
            'email': 'test@example.com',
            'password1': 'test_password',
            'password2': 'test_password'
        }
        form = UserCreationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['email'], ['The email is registered'])

    def test_form_with_different_passwords_should_raise_validation_error(self):
        form_data = {
            'email': 'test@example.com',
            'password1': 'test_password',
            'password2': 'different_password'
        }
        form = UserCreationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['password2'], ["Passwords don't match"])

    def test_form_save_should_create_user_with_provided_data(self):
        form_data = {
            'email': 'test@example.com',
            'password1': 'test_password',
            'password2': 'test_password'
        }
        form = UserCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        user = form.save()
        self.assertEqual(user.email, 'test@example.com')
        self.assertTrue(user.check_password('test_password'))
