# Generated by Django 5.1.3 on 2024-11-05 12:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0013_alter_cart_buyer'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cartitem',
            name='cart',
        ),
        migrations.RemoveField(
            model_name='cartitem',
            name='product',
        ),
        migrations.DeleteModel(
            name='Cart',
        ),
        migrations.DeleteModel(
            name='CartItem',
        ),
    ]
