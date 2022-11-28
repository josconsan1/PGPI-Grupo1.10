from django.urls import path
from django.contrib import admin

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('products/', views.products, name='products'),
    path('products/<int:product_id>/', views.detail, name='product_details'),
    path('shipping_polite/', views.shipping_polite, name='shipping_polite'),
    path('return_policy/',views.return_policy, name='return_policy'),
    path('admin/', admin.site.urls),
    path('privacy_policy', views.privacy_policy)
]