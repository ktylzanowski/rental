from django.urls import path
from . import views


urlpatterns = [
    path('cart/', views.CartListView.as_view(), name="Cart"),
    path('checkout/', views.CheckoutView.as_view(), name="Checkout"),
]
