# Generated by Django 4.1.3 on 2022-12-11 01:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gamingworld', '0009_comprasproductos_compra_productos'),
    ]

    operations = [
        migrations.AddField(
            model_name='compra',
            name='paid',
            field=models.BooleanField(default=False),
        ),
    ]
