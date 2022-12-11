from django.contrib import admin

from .models import *

admin.site.register(Producto)
admin.site.register(Seccion)
admin.site.register(Fabricante)
admin.site.register(Genero)
admin.site.register(Compra)
admin.site.register(ComprasProductos)
admin.site.register(EstadoPedido)
