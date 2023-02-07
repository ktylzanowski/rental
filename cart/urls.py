from django.urls import path
from . import views


urlpatterns = [
    path('cart/', views.CartListView.as_view(), name="Cart"),
    path('cart/complete', views.order_complete, name="order_complete"),
    path('cart/<int:pk>', views.DeleteItemView.as_view(), name="DeleteItemFromCart"),
    path('checkout/', views.CheckoutView.as_view(), name="Checkout"),
]
