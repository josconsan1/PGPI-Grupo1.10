from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import *
from datetime import *
from random import sample



def index(request):
    return render(request, 'gamingworld/index.html', {"slider": enumerate(sample(list(Producto.objects.all()), 3))})

def products(request):
    
    print(request.COOKIES.items())
    generos = Genero.objects.all()
    secciones = Seccion.objects.all()
    fabricantes = Fabricante.objects.all()

    nombre_de_producto_buscado = request.GET.get("name")
    genero_buscado = request.GET.get("producttype")
    seccion_buscada = request.GET.get("section")
    fabricante_buscado = request.GET.get("manufacturer")

    lista_tuplas_productos = get_products_by_tuples(nombre_de_producto_buscado, genero_buscado, seccion_buscada, fabricante_buscado)
    modelmap = {'trios_productos':lista_tuplas_productos, 
                'generos':generos,
                'secciones':secciones,
                'fabricantes':fabricantes}
    return render(request, 'gamingworld/products.html', modelmap)

def detail(request, product_id):
    producto = Producto.objects.get(id__exact=product_id)
    modelmap = {'producto':producto}
    response = render(request, 'gamingworld/product_details.html', modelmap)
    return response

def cart(request):
    productos_amounts = get_products_from_cookies(request)
    modelmap = {"products_amounts" : productos_amounts}
    response = render(request, 'gamingworld/cart.html', modelmap)
    return response

def add_product_to_cart(request, product_id):
    productos_amounts = get_products_from_cookies(request)
    modelmap = {'trios_productos':get_products_by_tuples(), "products_amounts" : productos_amounts}
    amount = request.GET.get("amount")
    if amount == '':
        modelmap["message"] = "No has añadido ningún artículo"
        response = render(request, 'gamingworld/cart.html', modelmap)
        return response
    key = "product_id_"+str(product_id)
    value = request.COOKIES.get(key)
    if value is None:
        value = 0
    
    if int(amount) + int(value) <= Producto.objects.get(id__exact=product_id).stock:
        modelmap["message"] = str(int(amount) + int(value)) + " artículos añadidos"
        response = render(request, 'gamingworld/products.html', modelmap)
        response.set_cookie(key, str(int(amount) + int(value)))
        return response
    else:
        modelmap["error_message"] = "Ha sobrepasado la cantidad de unidades disponibles de este artículo"
        response = render(request, 'gamingworld/cart.html', modelmap)
        return response

    

def delete_product_from_cart(request, product_id):
    key = "product_id_"+str(product_id)
    productos_amounts = get_products_from_cookies(request)
    modelmap = {'trios_productos':get_products_by_tuples(), "products_amounts" : productos_amounts}
    response = render(request, 'gamingworld/products.html',modelmap)
    response.delete_cookie(key)

    
    return response


def get_products_from_cookies(request):
    productos_amounts = []
    cookies = request.COOKIES
    for cookie in cookies.keys():
        if cookie[0:-1] == "product_id_":
            producto = Producto.objects.get(id__exact=cookie[-1])
            productos_amounts.append(tuple((producto, cookies[cookie])))
    print(productos_amounts)
    return productos_amounts


def get_products_by_tuples(nombre_de_producto_buscado=None, genero_buscado=None, seccion_buscada=None, fabricante_buscado=None):
    productos = []
    productos_todos = Producto.objects.all()
    for producto in productos_todos:
        genero_valido = True
        seccion_valida = True
        fabricante_valido = True
        nombre_de_producto_buscado_valido = True

        if nombre_de_producto_buscado is not None:
            nombre_de_producto_buscado_valido = producto.nombre.lower() == nombre_de_producto_buscado.replace("+"," ").lower()
        if genero_buscado is not None:
            genero_valido = producto.genero == Genero.objects.get(id__exact = genero_buscado)
        if seccion_buscada is not None:
            seccion_valida = producto.seccion == Seccion.objects.get(id__exact = seccion_buscada)
        if fabricante_buscado is not None:
            fabricante_valido = producto.fabricante == Fabricante.objects.get(id__exact = fabricante_buscado)
        if genero_valido and seccion_valida and fabricante_valido and nombre_de_producto_buscado_valido:
            productos.append(producto)
            
    
    lista_tuplas_productos = []
    for i in range(0, len(productos), 3):
        lista_tuplas_productos.append(tuple(productos[i:i+3]))
    return lista_tuplas_productos

def detail(request, product_id):
    producto = Producto.objects.get(id__exact=product_id)
    modelmap = {'producto':producto}
    return render(request, 'gamingworld/product_details.html', modelmap)
    
def termsofservice(request):
    return render(request, 'gamingworld/termsofservice.html')
    
def shipping_polite(request):
    return render(request, 'gamingworld/shipping_polite.html')

def return_policy(request):
    return render(request, 'gamingworld/return_policy.html')

def privacy_policy(request):
    return render(request, 'gamingworld/privacy_policy.html')


def get_cart_price(request):
    productos_amounts = []
    precio_total = 0
    cookies = request.COOKIES
    for cookie in cookies.keys():
        if cookie[0:-1] == "product_id_":
            producto = Producto.objects.get(id__exact=cookie[-1])
            precio_total += float(producto.precio) * float(cookies[cookie])
            
    
    return precio_total

    
def get_cart_name(request):
    productos_amounts = []
    nombres = ""
    cookies = request.COOKIES
    for cookie in cookies.keys():
        if cookie[0:-1] == "product_id_":
            producto = Producto.objects.get(id__exact=cookie[-1])
            nombres += producto.nombre + ", "
            
    
    return nombres
    
def release(request):
     productos_price = get_cart_price(request)
     precio_total = get_cart_price(request)

     nombre = request.GET.get("nombre_")
     apellidos = request.GET.get("apellidos_")
     identificacion = request.GET.get("identificacion_")
     movil = request.GET.get("movil_")
     direccion= request.GET.get("direccion_")
     piso = request.GET.get("piso_")
     observaciones = request.GET.get("observaciones_")
     pais = request.GET.get("pais_")
     codigo_postal = request.GET.get("codigo_postal_")
     poblacion = request.GET.get("poblacion_")
     provincia = request.GET.get("provincia_")
    
     release_price = float(1.99)
     total_price = release_price + productos_price
     
     productovendido =  Compra()
     productovendido.productos = get_cart_name(request)
     productovendido.dir=direccion
     productovendido.dni=identificacion
     productovendido.piso=piso
     productovendido.cp=codigo_postal
     productovendido.apellidos_dir=apellidos
     productovendido.nombre_dir=nombre
     productovendido.precio= total_price
     if(productovendido.dir != None):
      productovendido.save()     
     
     modelmap = {"products_price" : productos_price, "precio_envio" : release_price, "precio_total" : total_price }
    
     return render(request, 'gamingworld/release.html', modelmap)
