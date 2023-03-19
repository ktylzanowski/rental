from django.urls import path
from . import views


urlpatterns = [
    path('', views.CartView.as_view(), name="Cart"),
    path('add/<int:product_id>', views.AddToCart.as_view(), name='AddToCart'),
    path('del/<int:product_id>', views.RemoveFromCart.as_view(), name="DeleteItemFromCart"),
]
