from datetime import *
from random import sample

import stripe
from django.core.mail import send_mail
from django.http import HttpResponse
from django.shortcuts import redirect, render

from mysite.settings import STRIPE_KEY

from .models import *

stripe.api_key = STRIPE_KEY


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
            productos_amounts.append(tuple((producto, int(cookies[cookie]))))
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

def get_products_quantities_from_purchase(purchase_id):
    cp_list = ComprasProductos.objects.filter(compra = Compra.objects.get(id__exact = purchase_id))
    res = []
    for cp in cp_list:
        res.append(tuple([cp.producto, cp.cantidad]))
    return res
    
def release(request):
    precio_carrito = get_cart_price(request)

    if request.method == "POST":
        nombre = request.POST["nombre_"]
        apellidos = request.POST["apellidos_"]
        identificacion = request.POST["identificacion_"]
        direccion= request.POST["direccion_"]
        piso = request.POST["piso_"]
        codigo_postal = request.POST["codigo_postal_"]
        email = request.POST["email_"]
         
        compra = Compra(nombre_dir=nombre, apellidos_dir = apellidos, dni = identificacion, cp = codigo_postal, piso = piso, dir = direccion, precio = precio_carrito, email = str(email))
        compra.save()
        productos_cantidades = get_products_from_cookies(request)
        for producto_cantidad in productos_cantidades:
            producto = producto_cantidad[0]
            cantidad = producto_cantidad[1]
            if cantidad > producto.stock:
                return render(request, 'gamingworld/cart.html', {"error_message": "En tu carrito hay más unidades de {} que su stock".format(producto.nombre)})
            else:
                producto.stock = producto.stock - cantidad
                producto.save()
            cp = ComprasProductos(compra = compra, producto = producto_cantidad[0], cantidad = producto_cantidad[1])
            cp.save()
            res = redirect("/products/payment/checkout/"+str(compra.id))
            for cookie in request.COOKIES.keys():
                if cookie[:-1] == 'product_id_':
                    res.delete_cookie(cookie)
        return res
    modelmap = {"products_price" : precio_carrito, "precio_envio" : 1.99, "precio_total" : precio_carrito + 1.99}
    
    return render(request, 'gamingworld/release.html', modelmap)

def checkout_page(request, purchase_id):
    if Compra.objects.get(id__exact = purchase_id).paid:
        return render(request, 'gamingworld/index.html', {"error_message":"Esta compra ya ha finalizado"})
    total_amount = 1.99 # Gastos de envio
    for p, a in get_products_quantities_from_purchase(purchase_id):
        total_amount += float(p.precio) * int(a)
    intent = stripe.PaymentIntent.create(
        amount=int(total_amount * 100),
        currency='eur',
        automatic_payment_methods={
            'enabled': True,
        }
    )
    return render(request, 'gamingworld/checkout.html', {'clientSecret': intent['client_secret'], 'total_amount': total_amount, 'purchase_id':purchase_id})

def checkout_suceed(request, purchase_id):
    if Compra.objects.get(id__exact = purchase_id).paid:
        return render(request, 'gamingworld/index.html', {"error_message":"Esta compra ya ha finalizado"})
    payment_intent = request.GET.get('payment_intent', None)
    status = 'Algo fue mal durante el pago'

    if payment_intent:
        paymentIntent = stripe.PaymentIntent.retrieve(payment_intent)
        if paymentIntent['status'] == 'succeeded':
            send_mail(
                'Recibo de pago GamingWorld',
                'Gracias por comprar en nuestra tienda. Tu identificador de pedido es %s' % (payment_intent),
                'josconsan1@alum.us.es',
                [paymentIntent['receipt_email']],
                fail_silently=True,
            )
            status = 'Completado'
            compra = Compra.objects.get(id__exact = purchase_id)
            compra.paid = True
            compra.save()
        elif paymentIntent['status'] == 'processing':
            status = 'Procesando el pago'

    res = render(request, 'gamingworld/succeed.html', {'status': status})

    return res

    
def purchases(request):
    requested_email = request.GET.get("email")
    requested_dni = request.GET.get("dni")
    compras = None
    comprasproductos = []
    if requested_email is not None and requested_dni is not None:
        compras = Compra.objects.filter(email = requested_email, dni = requested_dni)
        for compra in compras:
            compraproducto = ComprasProductos.objects.filter(compra = compra)
            comprasproductos.extend(compraproducto)
    modelmap = {'compras': compras, 'comprasproductos':comprasproductos}
    return render(request, 'gamingworld/purchases.html', modelmap)

def purchases_delete(request, purchase_id):
    requested_email = request.GET.get("email")
    requested_dni = request.GET.get("dni")
    purchase = Compra.objects.get(id__exact = purchase_id)
    if purchase.dni == requested_dni and purchase.email == requested_email:
        if not purchase.paid:
            for compraproducto in ComprasProductos.objects.filter(compra = purchase):
                producto = Producto.objects.get(id__exact = compraproducto.producto.id)
                producto.stock = producto.stock + compraproducto.cantidad
                producto.save()
        purchase.delete()
    return purchases(request)
