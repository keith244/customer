# Generated by Django 5.0.7 on 2024-11-20 09:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('customers', '0002_order_alter_customer_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='order',
            options={'verbose_name_plural': 'Orders'},
        ),
    ]
