# Generated by Django 3.2.18 on 2023-06-06 13:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0023_alter_order_customer'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='contact',
            field=models.CharField(default='+886 0912768057', max_length=100),
        ),
    ]
