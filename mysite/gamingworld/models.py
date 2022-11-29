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

class Pedido(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, null=True)
    status = models.ForeignKey(EstadoPedido, on_delete=models.CASCADE, null=True)
    direccion = models.CharField(max_length=400)
    telefono = models.CharField(max_length=15)
    nombre = models.CharField(max_length=200)
    apellido = models.CharField(max_length=300)
    correo = models.EmailField(max_length=254)
    tarjeta = models.CharField(max_length=30)
    order_id = models.PositiveBigIntegerField(default=0, unique=True)