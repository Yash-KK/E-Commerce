# Generated by Django 4.1.1 on 2022-10-06 12:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Orders', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orderproduct',
            name='color',
        ),
        migrations.RemoveField(
            model_name='orderproduct',
            name='size',
        ),
    ]
