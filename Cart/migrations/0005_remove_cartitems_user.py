# Generated by Django 4.1.1 on 2022-10-03 00:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Cart', '0004_cartitems_user_alter_cartitems_cart'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cartitems',
            name='user',
        ),
    ]
