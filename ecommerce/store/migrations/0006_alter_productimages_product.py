# Generated by Django 3.2.18 on 2023-04-17 13:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0005_alter_vendor_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productimages',
            name='product',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='p_image', to='store.product'),
        ),
    ]
