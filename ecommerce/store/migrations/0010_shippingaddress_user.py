# Generated by Django 3.2.18 on 2023-04-19 14:59

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0009_alter_product_stock_count'),
    ]

    operations = [
        migrations.AddField(
            model_name='shippingaddress',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
    ]
