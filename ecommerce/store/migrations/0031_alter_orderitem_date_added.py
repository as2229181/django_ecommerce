# Generated by Django 3.2.18 on 2023-06-15 15:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0030_auto_20230615_2328'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderitem',
            name='date_added',
            field=models.DateTimeField(),
        ),
    ]
