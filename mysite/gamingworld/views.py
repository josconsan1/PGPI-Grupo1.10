from django.shortcuts import render
from django.http import HttpResponse
from .models import *


def index(request):
    return render(request, 'gamingworld/index.html')

def products(request):
    productos = Producto.objects.all()
    genero_buscado = request.GET.get("producttype")
    lista_tuplas_productos = []
    for i in range(0, len(productos), 3):
        lista_tuplas_productos.append(tuple(productos[i:i+3]))
    modelmap = {'trios_productos':lista_tuplas_productos}
    return render(request, 'gamingworld/products.html', modelmap)

def detail(request, product_id):
    producto = Producto.objects.get(id__exact=product_id)
    modelmap = {'producto':producto}
    return render(request, 'gamingworld/product_details.html', modelmap)

def termsofservice(request):
    return render(request, 'gamingworld/termsofservice.html')