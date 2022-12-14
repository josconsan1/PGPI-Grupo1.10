from django.contrib import admin
from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('products/', views.products, name='products'),
    path('products/<int:product_id>/', views.detail, name='product_details'),
    path('cart/', views.cart, name='cart'),
    path('purchases/', views.purchases, name='purchases'),
    path('purchases/delete/<int:purchase_id>/', views.purchases_delete, name='purchases_delete'),
    path('addproduct/<int:product_id>/', views.add_product_to_cart, name='addproduct'),
    path('deleteproduct/<int:product_id>/', views.delete_product_from_cart, name='deleteproduct'),
    path('shipping_polite/', views.shipping_polite, name='shipping_polite'),
    path('return_policy/',views.return_policy, name='return_policy'),
    path('admin/', admin.site.urls),
    path('termsofservice/',views.termsofservice, name='termsofservice'),
    path('privacy_policy/', views.privacy_policy),
    path('products/payment/checkout/<int:purchase_id>/', views.checkout_page, name='checkout'),
    path('products/payment/completed/<int:purchase_id>/', views.checkout_suceed, name='succeed'),
    path('products/payment/release', views.release, name='release'),
    path('orders/', views.get_order_by_id),
    path('order_not_found/', views.order_not_found),
]