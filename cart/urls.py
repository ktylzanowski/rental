from django.urls import path
from . import views


urlpatterns = [
    path('cart/', views.CartView.as_view(), name="Cart"),
    path('cart/add/<int:product_id>', views.AddToCart.as_view(), name='AddToCart'),
    path('cart/del/<int:product_id>', views.RemoveFromCart.as_view(), name="DeleteItemFromCart"),
]
