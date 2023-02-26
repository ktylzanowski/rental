from django.urls import path
from . import views

urlpatterns = [
    path('adminpanel/', views.AdminPanel.as_view(), name='AdminPanel'),
    path('adminpanel/orders', views.OrderListView.as_view(), name='OrdersListView'),
]
