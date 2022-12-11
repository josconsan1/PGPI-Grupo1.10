from django.db import models

class Genero(models.Model):
    nombre = models.CharField(max_length=200)
class Seccion(models.Model):
    nombre = models.CharField(max_length=200)
class Fabricante(models.Model):
    nombre = models.CharField(max_length=200)

class Producto(models.Model):
    nombre = models.CharField(max_length=200)
    descripcion = models.TextField(default="Vacío")
    genero = models.ForeignKey(Genero, on_delete=models.CASCADE, null=True)
    seccion = models.ForeignKey(Seccion, on_delete=models.CASCADE, null=True)
    fabricante = models.ForeignKey(Fabricante, on_delete=models.CASCADE, null=True)
    precio = models.DecimalField(max_digits=9, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)
    imagen = models.CharField(max_length=200)

class EstadoPedido(models.Model):
    nombre = models.CharField(max_length=200)

class Compra(models.Model):
    productos = models.ManyToManyField(Producto, through='ComprasProductos')
    nombre_dir =  models.CharField(max_length=200,null=True)
    apellidos_dir = models.CharField(max_length=200,null=True)
    dni = models.CharField(max_length=200, null=True)
    cp = models.CharField(max_length=200, null=True)
    piso = models.CharField(max_length=200, null=True)
    dir =models.CharField(max_length=200, null=True)
    precio = models.FloatField(max_length=200, null=True)
    email = models.CharField(max_length=200, null=True)
    paid = models.BooleanField(default=False) 
    status = models.ForeignKey(EstadoPedido, on_delete=models.CASCADE, null=True)
    order_id = models.CharField(max_length=200, unique=True)
    
class ComprasProductos(models.Model):
    compra = models.ForeignKey(Compra, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=1)