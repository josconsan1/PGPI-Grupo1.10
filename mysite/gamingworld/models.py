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