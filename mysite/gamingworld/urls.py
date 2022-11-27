from django.urls import path
from django.contrib import admin
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('products/', views.products, name='products'),
    path('products/<int:product_id>/', views.detail, name='product_details'),
    path('cart/', views.cart, name='cart'),
    path('addproduct/<int:product_id>/', views.add_product_to_cart, name='addproduct'),
    path('deleteproduct/<int:product_id>/', views.delete_product_from_cart, name='deleteproduct'),
    path('admin/', admin.site.urls),
]