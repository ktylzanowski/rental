from django.urls import path
from .views import RegisterCreateView, MyLoginView, MyLogoutView, AccountView

urlpatterns = [
    path('register/', RegisterCreateView.as_view(), name='Register'),
    path('login/', MyLoginView.as_view(), name='Login'),
    path('logout/', MyLogoutView.as_view(), name='Logout'),
    path('account/<int:pk>/', AccountView.as_view(), name='Account'),
]
