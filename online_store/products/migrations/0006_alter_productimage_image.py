# Generated by Django 5.0.3 on 2024-04-07 14:46

import online_store.products.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0005_alter_product_options_alter_product_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productimage',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='media/product_photos', validators=[online_store.products.validators.validate_image_size_less_than_5mb]),
        ),
    ]
