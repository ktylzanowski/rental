from django.urls import path
from . import views

urlpatterns = [
    path('adminpanel/', views.AdminPanel.as_view(), name='AdminPanel'),
    path('adminpanel/orders', views.OrderListView.as_view(), name='OrdersListView'),
    path('adminpanel/carts', views.CartListView.as_view(), name='CartListView'),
    path('adminpanel/order/<int:pk>', views.OrderDetailView.as_view(), name='OrderDetailView'),
    path('adminpanel/carts/<int:pk>', views.CartDetailView.as_view(), name='CartDetailView'),
    path('adminpanel/users', views.UsersListView.as_view(), name='UsersListView'),
    path('adminpanel/products', views.ProductsListView.as_view(), name='ProductsListView'),
    path('adminpanel/products/addBook', views.BookCreateView.as_view(), name='BookCreateView'),
]
