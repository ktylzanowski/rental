from django.urls import path
from . import views

urlpatterns = [
    path('adminpanel/', views.AdminPanel.as_view(), name='AdminPanel'),
    path('adminpanel/orders', views.OrderListView.as_view(), name='OrdersListView'),
    path('adminpanel/order/<int:pk>', views.OrderDetailView.as_view(), name='OrderDetailView'),
    path('adminpanel/users', views.UsersListView.as_view(), name='UsersListView'),
    path('adminpanel/products', views.ProductsListView.as_view(), name='ProductsListView'),
    path('adminpanel/products/addBook', views.BookCreateView.as_view(), name='BookCreateView'),
    path('adminpanel/products/addCD', views.CDCreateView.as_view(), name='CDCreateView'),
    path('adminpanel/products/addFilm', views.FilmCreateView.as_view(), name='FilmCreateView'),
    path('adminpanel/products/deleteProduct/<int:pk>', views.ProductDeleteView.as_view(), name='ProductDeleteView'),
    path('adminpanel/products/bookUpdate/<int:pk>', views.BookUpdateView.as_view(), name='BookUpdateView'),
    path('adminpanel/products/cdUpdate/<int:pk>', views.CDUpdateView.as_view(), name='CDUpdateView'),
    path('adminpanel/products/filmUpdate/<int:pk>', views.FilmUpdateView.as_view(), name='FilmUpdateView'),
    path('adminpanel/users/userDelete/<int:pk>', views.UserDeleteView.as_view(), name='UserDeleteView'),
    path('adminpanel/users/userUpdate/<int:pk>', views.UserUpdateView.as_view(), name='UserUpdateView'),
    path('adminpanel/order/changestatus/<int:pk>', views.ChangeOrderStatus.as_view(), name='ChangeOrderStatus'),
]
