# Generated by Django 3.2.18 on 2023-06-17 16:43

from django.db import migrations, models
import store.models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0034_alter_profile_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='iamge',
            field=models.ImageField(default='user.jpg', upload_to=store.models.user_directory_path),
        ),
        migrations.AlterField(
            model_name='profile',
            name='image',
            field=models.ImageField(default='product.png', upload_to=store.models.user_directory_path),
        ),
    ]
