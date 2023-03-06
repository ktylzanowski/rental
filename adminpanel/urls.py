from django.urls import path
from . import views

urlpatterns = [
    path('adminpanel/', views.AdminPanel.as_view(), name='AdminPanel'),
    path('adminpanel/orders', views.OrderListView.as_view(), name='OrdersListView'),
    path('adminpanel/carts', views.CartListView.as_view(), name='CartListView'),
    path('adminpanel/order/<int:pk>', views.OrderDetailView.as_view(), name='OrderDetailView'),
    path('adminpanel/carts/<int:pk>', views.CartDetailView.as_view(), name='CartDetailView'),
]
