# Generated by Django 3.0.7 on 2020-08-24 17:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_product_brand'),
    ]

    operations = [
        migrations.DeleteModel(
            name='PurchaseItem',
        ),
        migrations.DeleteModel(
            name='PurchaseOrder',
        ),
    ]
