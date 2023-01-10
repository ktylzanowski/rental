from django.urls import path
from .views import RegisterCreateView, MyLoginView
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('register/', RegisterCreateView.as_view(), name='Register'),
    path('login/', MyLoginView.as_view(), name='Login'),
    path('logout', auth_views.LogoutView.as_view(), name='Logout'),
]
