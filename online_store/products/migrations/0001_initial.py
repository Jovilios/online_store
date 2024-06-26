# Generated by Django 5.0.3 on 2024-03-12 22:06

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounts', '0002_userprofile'),
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('description', models.TextField(blank=True, max_length=500, null=True)),
                ('category', models.CharField(choices=[('home_garden', 'Home And Garden'), ('collectables_antiques', 'Collectables And Antiques'), ('electronics', 'Electronics'), ('sport_and_hobbies', 'Sport and Hobbies'), ('fashion', 'Fashion'), ('cars_motorcycle', 'Cars And Motorcycle'), ('properties', 'Properties'), ('others', 'Others')])),
                ('date_published', models.DateTimeField(auto_now_add=True)),
                ('user_profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='products', to='accounts.userprofile')),
            ],
        ),
        migrations.CreateModel(
            name='ProductImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='product_photos')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='photos', to='products.product')),
            ],
        ),
    ]
