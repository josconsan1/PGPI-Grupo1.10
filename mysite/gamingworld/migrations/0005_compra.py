# Generated by Django 4.1.3 on 2022-12-05 10:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gamingworld', '0004_producto_fabricante_producto_genero_producto_seccion'),
    ]

    operations = [
        migrations.CreateModel(
            name='Compra',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('productos', models.CharField(max_length=400, null=True)),
                ('nombre_dir', models.CharField(max_length=200, null=True)),
                ('apellidos_dir', models.CharField(max_length=200, null=True)),
                ('dni', models.CharField(max_length=200, null=True)),
                ('cp', models.CharField(max_length=200, null=True)),
                ('piso', models.CharField(max_length=200, null=True)),
                ('dir', models.CharField(max_length=200, null=True)),
                ('precio', models.FloatField(max_length=200, null=True)),
            ],
        ),
    ]
