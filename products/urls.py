from django.urls import path
from . import views

urlpatterns = [
    path('', views.Home.as_view(), name='home'),
    path('category/<str:cats>/', views.ProductsByCategoryView.as_view(), name='ByCategory'),
    path('product/<int:pk>', views.ProductDetailView.as_view(), name='ProductDetail'),

]
